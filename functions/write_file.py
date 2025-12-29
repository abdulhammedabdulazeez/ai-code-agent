import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_path = (
            os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        )

        if not valid_target_path:
            raise Exception(
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )

        # Ensure parent directories exist
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # If target exists and is a directory, refuse to write
        if os.path.exists(target_path) and os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Write content (creates the file if it doesn't exist)# Write content (creates the file if it doesn't exist)
        with open(target_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return e


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Write text content to a file inside the working directory. Parent directories will be "
        "created as needed. Writing outside the working directory is rejected. If the target path "
        "exists and is a directory the write is refused."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path (from working_directory) where the content will be written. Parent directories will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)
