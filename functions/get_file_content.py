import os
from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_path= os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

        if not valid_target_path:
            raise Exception(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_path):
            raise Exception(
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{target_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string

    except OSError as e:
        # catch any unforeseen errors raised by the os library and return a string
        return f"Error: {e}"
    except Exception as e:
        return e


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Read the contents of a file inside the working directory. The function reads up to "
        "the configured MAX_CHARS and appends a truncation notice if the file is larger. "
        "Access outside the working directory is rejected."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to working_directory (e.g. 'pkg/module.py' or 'README.md').",
            ),
        },
        required=["file_path"],
    ),
)
