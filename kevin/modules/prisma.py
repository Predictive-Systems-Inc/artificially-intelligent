import os
import re

def find_prisma(dir): 
    """
    Finds the Prisma schema file in the given directory.
    """
    # check if "prisma/schema.prisma" exists
    if os.path.exists(os.path.join(dir, "prisma/schema.prisma")):
        return os.path.join(dir, "prisma/schema.prisma")
    else: 
        # search for any file with .prisma extension
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith(".prisma"):
                    return os.path.join(root, file)
    return None

def read_prisma(file_path: str):
    """
    Reads the Prisma schema file and returns the contents in structured format.
    Structure:
    {
      "model":[{
        "name": "User",
        "fields": [
            "name": "id",
            "type": "Int",
            "annotations": ["@id", "@default(autoincrement())"]
            "required": true
        ]
      },
      {
        "model": [
        ....
        ]
      }]
    }
    """
    with open(file_path, 'r') as file:
        content = file.read()
        # use regex to look for the pattern model <Name> { <fields> }
        models_re = re.findall(r'model\s+(\w+)\s+{([^}]+)}', content)
        models = []
        for model in models_re:
            model_name = model[0]
            fields_str = model[1].split("\n")
            fields = []
            for field in fields_str:
                # ignore empty lines
                if (field.strip() == ""):
                    continue
                # ignore annotations and comments
                if (field.strip().startswith("@") or field.strip().startswith("//")):
                    continue
                # split the field into name, type and annotations
                field = field.split()
                field_name = field[0]
                field_type = field[1]
                field_annotations = " ".join(field[2:])
                fields.append({
                    "name": field_name,
                    "type": field_type,
                    "annotations": field_annotations
                })
            models.append({
                "name": model_name,
                "fields": fields
            })
        return models


# create main for testing
if __name__ == "__main__":
    read_prisma("../test/schema.prisma")