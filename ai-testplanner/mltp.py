from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl
import base64
import re
import pandas as pd
from io import StringIO

class TestResultOutputParser(StrOutputParser):
    """
    Output parser for test results
    """
    response = ""
    def get_format_instructions(self):
        return "".join([
          "Reply in markdown format with the following columns: ",
          "Test Case ID, Test Case Description, Test Data, Expected Result, Actual Result, Status, Comments"
        ])
    def parse(self, output: str):
        self.response = self.response +  output
        return output
    
    def save_to_file(self):
        # look for string within ```markdown and ```
        
        markdown = re.findall(r"```(.*?)```", self.response, re.DOTALL)
        data = StringIO(markdown[0])
        df = pd.read_csv(data, sep="|", skiprows=1)

        # remove first and last column
        df = df.drop(df.columns[0], axis=1)
        df = df.drop(df.columns[-1], axis=1)

        # specify column names
        df.columns = ['Test Case ID', 'Test Case Description', 'Test Data', 'Expected Result', 'Actual Result', 'Status', 'Comments']

        # get the filename
        filename = re.findall(r"filename: (.*).xls", self.response)
        filename = filename[0] if filename else "test_cases"
        # save to excel
        df.to_excel(filename+".xlsx", index=False)
        return filename+".xlsx"
    
def encode_image(image_path):
    """
    Encode the image to base64
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

async def ask_upload_screen():
    """
    Ask the user to upload a screen layout
    """
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a screen layout. I will create the test cases for you.", accept=["image/*"]
        ).send()

    screen = files[0]

    image = cl.Image(path=screen.path, name="screen", display="inline")

    # Attach the image to the message
    await cl.Message(
        content="Image uploaded successfully..",
        elements=[image],
    ).send()

    return screen.path

async def analyze_image(image_path):
    """
    Process the image and return the prompt
    """
    # Let the user know that the system is ready
    await cl.Message(
        content="Please wait while I analyze the screen for you..."
    ).send()

    # encode the image to base64
    image_b64 = encode_image(image_path)
    output_parser = TestResultOutputParser()
    format_instructions = output_parser.get_format_instructions()
    cl.user_session.set("output", output_parser) 

    # prepare the prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "".join([
                  "You're software tester and you are assigned to analyze screens to create test cases. ",
                  "You will respond only to questions related to the screen layout.",
                  "If the image does not look like a screen layout, respond with ",
                  "what you think the image is and say 'Please upload a screen layout'."
                  f"Include negative and edge cases."
                ]),
            ),
            ("human", [
                {   "type": "text", 
                    "text": "".join([
                        "Create test cases for the attached image. ",
                        f"{format_instructions}",
                        "And indicate a descriptive filename for test cases ",
                        "at the end of your response in the format:",
                        "\n\nfilename: descriptive_name.xls\n\n",
                    ])
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_b64.decode('utf-8')}",
                    },
                },
            ]),
        ]
    )

    # send the prompt asynchronously
    model = cl.user_session.get("model")
    msg = cl.Message(content="")
    runnable = prompt | model | output_parser
    async for chunk in runnable.astream(
        {"question": "List down all test cases that can be performed in this screen? "},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

    return runnable

async def ask_next_action():
    """
    Ask the user for the next action
    """
    res = await cl.AskActionMessage(
        content="What do you like to do next?",
        actions=[
            cl.Action(name="more", value="more", label="🪄 Upload Another"),
            cl.Action(name="save", value="save", label="💾 Save to File"),
        ],
    ).send()

    if res and res.get("value") == "more":
        screen_path = await ask_upload_screen()
        await analyze_image(screen_path)
        await ask_next_action()
    
    if res and res.get("value") == "save":        
        output_parser = cl.user_session.get("output")
        filename = output_parser.save_to_file()
        elements = [
            cl.File(
                name=filename,
                path="./"+filename,
                display="inline",
            ),
        ]
        await cl.Message(
            content="Click to download the file", elements=elements
        ).send()

@cl.on_chat_start
async def on_chat_start():
    print ("on_start!!*********")
    model = ChatOpenAI(model="gpt-4-vision-preview",streaming=True)
    cl.user_session.set("model", model) 

    screen_path = await ask_upload_screen()
    await analyze_image(screen_path)
    await ask_next_action()

@cl.on_message
async def on_message(msg: cl.Message):
    print ("on_message!!*********")
    # check for attachment
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return
    
    images = [file for file in msg.elements if "image" in file.mime]
    screen = images[0]

    image = cl.Image(path=screen.path, name="screen", display="inline")

    # Attach the image to the message
    await cl.Message(
        content="Image uploaded successfully..",
        elements=[image],
    ).send()

    await analyze_image(screen.path)

    await ask_next_action()