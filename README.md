# ai-code-agent project

Lightweight AI coding assistant that can inspect and modify a project workspace by calling a small set of safe file-system functions. The agent uses Google GenAI (Gemini) to decide actions and then performs those actions via a guarded set of functions.

## Features
- List directory contents (get_files_info)
- Read file contents (get_file_content) with truncation control
- Execute Python files under the working directory (run_python_file)
- Write files and automatically create parent directories (write_file)
- Conversation loop that runs function calls until the model returns a final response

## How it works - (high level)
1. Your prompt is sent to the model along with a system prompt that constrains behavior.
2. The model returns either:
   - A final textual response, or
   - A function call indicating which safe operation to run.
3. The application executes the function, collects the result, appends it to the conversation, and calls the model again.
4. Loop continues until the model returns a textual answer (no function calls) or a maximum number of iterations is reached.

All filesystem operations are resolved relative to a provided `working_directory` and are explicitly rejected if they would access outside that tree.

## Requirements
- Python 3.10+
- Google GenAI client (Gemini) and other dependencies listed in `requirements.txt`
- A Gemini API key (set as `GEMINI_API_KEY`)

## Quick start (macOS / VS Code terminal)
```bash
# create & activate virtualenv
python -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# set API key (example)
export GEMINI_API_KEY="sk-..."

# run the agent with a prompt
python main.py "Explain how the calculator renders the result to the console"

# (alternate command used in repository examples)
uv run main.py "how does the calculator render results to the console?"
```

## Available functions (brief)
- get_files_info(working_directory, directory=".")
  - Lists entries in a directory relative to `working_directory`. Returns name, size and is_dir status.
- get_file_content(working_directory, file_path)
  - Reads file content up to the configured MAX_CHARS and appends a truncation notice if necessary.
- write_file(working_directory, file_path, content)
  - Writes text to a file; creates parent directories as needed; refuses writes outside `working_directory`.
- run_python_file(working_directory, file_path, args=None)
  - Executes a `.py` file under `working_directory` with optional args; enforces timeout and path restrictions.

Schemas for these functions are exposed via `call_function.available_functions` and used to let the model plan function calls.

## Development & testing
- Run the repository's simple test drivers directly:
```bash
python test_get_files_info.py
python test_get_file_content.py
```
- The project includes a loop and retry/backoff around model calls to handle transient 429 quota errors.

## Security notes
- All paths resolved relative to the provided `working_directory` and access outside that tree is rejected.
- Do not commit API keys; store them in environment variables or a local `.env` (ignored by .gitignore).

## Contributing
- Open a feature branch, add tests, and submit a PR. Keep changes small and focused.
- Add new safe functions to `functions/` and wire their schemas into `call_function.py`.

## License
Add a LICENSE file for the repo (e.g., MIT) before publishing.
