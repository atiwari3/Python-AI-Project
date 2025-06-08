import os
from openai import OpenAI
import argparse
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up OpenAI client (new API)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, markdown = False):
    system_prompt = "Summarize the following text in markdown:" if markdown else "Summarize the following text clearly:"

    # Use the new v1 API structure
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or gpt-3.5-turbo if preferred
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Summarize a text file using OpenAI")
    parser.add_argument("filepath", help="Path to the text or markdown file")
    parser.add_argument("--format", choices=["plain", "markdown"], default="plain", help="Output format (default: plain)")

    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File '{args.filepath}' not found.")
        return

    with open(args.filepath, "r", encoding="utf-8") as f:
        content = f.read()

    summary = summarize_text(content, markdown=(args.format == "markdown"))
    print("\n=== Summary ===\n")
    print(summary)

if __name__ == "__main__":
    main()