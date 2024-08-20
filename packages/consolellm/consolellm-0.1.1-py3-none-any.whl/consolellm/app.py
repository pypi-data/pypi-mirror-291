from openai import OpenAI
from os import getenv
import os
from rich.console import Console
from rich.markdown import Markdown
from rich.style import Style
import markdown2
import time
import toml
from consolellm.config import create_config

api_key, system_prompt = create_config()


def display_markdown(text):
    console = Console()
    markdown = Markdown(text)
    console.print(markdown)

def main():
    full_context = ""
    console = Console()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    while True:
        
        console.print("[green]User:[/green]")
        multi_line_prompt = ""
        while True:
            line = input()
            if line == "\\end":
                break
            multi_line_prompt += line + "\n"

        curr_prompt = multi_line_prompt.strip()
        
        if curr_prompt.lower() == "exit()":

            file_name = input("Saving conversation history. Enter a file name (eg. sample.html, leave blank if don't want to save):")
            if len(file_name)!=0:

                html_content = markdown2.markdown(full_context, extras=["fenced-code-blocks"])
                html_output = f"<html><head><title>Conversation History</title></head><body>{html_content}</body></html>"
                with open(file_name, "w") as file:
                    file.write(html_output)
            break
        
        full_context += f"**User:** {curr_prompt}\n\n"
        
        console.print("[blue]Model:[/blue] thinking...")

        completion = client.chat.completions.create(
            model="nousresearch/hermes-3-llama-3.1-405b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": full_context,
                },
            ],
        )
        
        output = completion.choices[0].message.content
        full_context += f"**Model:** {output}\n\n"
        
        display_markdown(output)
        console.print("\nEnter your next prompt. Type '\\end' on a new line to submit:")

if __name__ == "__main__":
    main()