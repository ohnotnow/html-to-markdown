# html-to-markdown

A command-line tool to convert HTML component documentation into clean, well-formatted Markdown using GPT-4.1 via the [LiteLLM](https://pypi.org/project/litellm/) client.

---

## Features

- Scans a directory for HTML files **without** extensions that have not yet been converted.  
- Sends each HTML file’s contents (wrapped with custom instructions) to an LLM.  
- Writes the returned Markdown to a `.md` file alongside the original.  
- Configurable LLM model (defaults to `openai/gpt-4.1`).  

---

## Prerequisites

- Python 3.13 or newer  
- An [OpenAI API key](https://platform.openai.com/docs/api-keys)  
- [uv](https://docs.astral.sh/uv/getting-started/installation/) CLI (for dependency management & running)  

---

## Installation

1. **Clone the repository**  
   ```bash  
   git clone <repository_url>  
   cd html-to-markdown  
   ```  
2. **Install dependencies**  
   ```bash  
   uv sync  
   ```  

---

## Configuration

Create a file named `.env` in the project root with your OpenAI API key:

```dotenv
OPENAI_API_KEY=sk-...
```

The tool also respects a shell environment variable if you prefer:

```bash
export OPENAI_API_KEY=sk-...
```

---

## Usage

```bash
uv run main.py --path <directory>
```

Arguments:

- `--path` (required): Directory containing HTML files to convert.  

Behavior:

1. Finds files **without** any extension in `<directory>`.  
2. Omits files if a corresponding `.md` already exists.  
3. Streams each HTML through GPT-4.1 with built-in conversion instructions.  
4. Writes output to `<original_filename>.md`.  

---

## Example

Assume you have a folder `components/` with files:

```
button
input
card.html         ← ignored (has extension)
card              ← processed if `card.md` doesn’t exist
```

Run:

```bash
uv run main.py --path components
```

Output:

```
Processing components/button...
Wrote components/button.md
Processing components/input...
Wrote components/input.md
Processing components/card...
Wrote components/card.md
```

---

## License

This project is released under the [MIT License](LICENSE).
