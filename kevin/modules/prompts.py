from langchain_core.prompts import ChatPromptTemplate

def create_git_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in writing GitHub commit messages based on the past actions doen by the user. Use the available context to answer the question.

    Choose only one of the following commit types:
    - feat: a new feature
    - fix: a bug fix
    - chore: other changes that don't modify src or test files
    - docs: documentation only changes
    - style: changes that do not affect the meaning of the code
    - refactor: a code change that neither fixes a bug nor adds a feature
    - perf: a code change that improves performance
    - test: adding missing tests or correcting existing tests
    - build: changes that affect the build system or external dependencies
    - ci: changes to our CI configuration files and scripts
    - revert: reverts a previous commit
    - deprecate: deprecates a feature
    - remove: changes that removes a feature after being deprecated
    - security: changes that improves or resolves a security issue

    Strictly respond with the format commit type: commit summary only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_prisma_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in editing Prisma schemas. Use the available context to answer the question.
    Make sure that you are editing the Prisma schema file and not overwriting it.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_error_fetcher_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in getting the lint error/warnings for a specific file given a list of multiple lint error/warnings. Use the available context to answer the question.

    Strictly respond using the following format only:
    Errors: [insert actual errors here]
    However, if there are no errors/warnings, strictly respond with "No errors found."
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_error_fixer_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in fixing a given code based on the given list of errors. Use the available context to answer the question.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_directory_fetcher_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in choosing the correct directory a file should be saved on based on the filename given a list of directories. Use the available context to answer the question.

    Strictly respond using the following format only:
    Directory: [insert choses directory here]
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_form_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in creating forms in NextJS. Use the available context to answer the question.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_route_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in creating API routes in NextJS. Use the available context to answer the question.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_route_filters_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in creating API routes with specific filters used for fetching data in NextJS. Use the available context to answer the question.

    Make sure that aside from the GET method, the methods POST, PATCH, and DELETE are also included in the response.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_table_ui_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in creating a specific component for tables in NextJS. Use the available context to answer the question.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)

def create_editing_rag_prompt(instructions: str = '') -> ChatPromptTemplate:
    """
    Creates a ChatPromptTemplate for the RAG (Retrieval-Augmented Generation) assistant.
    """
    RAG_PROMPT = """
    CONTEXT:
    {context}

    QUERY:
    {question}

    You are a helpful assistant knowledgeable in applying modifications to a given code. Use the available context to answer the question.

    Strictly respond with actual raw code only. No other text is needed.
    """

    return ChatPromptTemplate.from_template(RAG_PROMPT + instructions)