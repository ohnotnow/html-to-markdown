import os
import argparse
from litellm import completion


def find_unconverted_files(directory):
    """
    Returns a list of files in the directory that:
    - Do not have a file extension
    - Do not have a corresponding .md file with the same basename
    """
    files = os.listdir(directory)
    basenames = set()
    md_files = set()
    for f in files:
        if os.path.isfile(os.path.join(directory, f)):
            if '.' not in f:
                basenames.add(f)
            elif f.endswith('.md'):
                md_files.add(f[:-3])
    # Only include files with no extension and no matching .md file
    result = [f for f in basenames if f not in md_files]
    return result


def convert_html_to_markdown(file_path, instructions, model="openai/gpt-4.1"):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    messages = [
        {"role": "user", "content": instructions + "\n\n" + html_content}
    ]
    response = completion(model=model, messages=messages)
    # litellm returns a dict with 'choices', get the content
    if hasattr(response, 'choices'):
        return response.choices[0].message['content']
    elif isinstance(response, dict) and 'choices' in response:
        return response['choices'][0]['message']['content']
    else:
        raise ValueError("Unexpected response format from litellm")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML files to Markdown using GPT-4.1 via LiteLLM.")
    parser.add_argument('--path', type=str, required=True, help='Directory to search')
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY environment variable must be set.")

    instructions = (
        "Could you convert all of the documents in this directory to be\n"
        "well-formatted markdown which an LLM can read to help me use this\n"
        "livewire fluxui component library?  They are all in html with a lot of\n"
        "wrapping content.  The main text of the instructions for each component\n"
        "seem to be inside the `<div class=\"[grid-area:main]` block however.  I\n"
        "want the text of the instructions and the code examples so that I can\n"
        "help guide an LLM to help me later.  Please respond with only the markdown rewrite - no other chat or commentary."
    )

    files = find_unconverted_files(args.path)
    for f in files:
        file_path = os.path.join(args.path, f)
        print(f"Processing {file_path}...")
        try:
            markdown = convert_html_to_markdown(file_path, instructions)
            md_path = file_path + ".md"
            with open(md_path, 'w', encoding='utf-8') as out_f:
                out_f.write(markdown)
            print(f"Wrote {md_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
