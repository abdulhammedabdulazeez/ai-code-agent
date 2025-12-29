import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_path = (
            os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        )

        if not valid_target_path:
            raise Exception(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_path.endswith(".py"):
            raise Exception(f'Error: "{file_path}" is not a Python file')

        command = ["python", target_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            timeout=30,
            text=True
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)

    except Exception as e:
        return e


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Execute a Python (.py) file located under the working directory. Returns combined "
        "STDOUT/STDERR and exit status information. Execution outside the working directory "
        "or non-.py files are rejected. A fixed timeout is applied by the implementation."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute (must end with .py).",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional list of additional command-line arguments to pass to the script.",
                ),
            ),
        },
        required=["file_path"],
    ),
)
