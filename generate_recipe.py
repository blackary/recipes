import os
from pathlib import Path
import re
import llm
import requests


def sanitize_filename(filename):
    return re.sub(r"[^a-z0-9-]", "-", filename.lower()).strip("-")


def generate_recipe_from_text(filename: str = "contents.txt"):
    model = llm.get_model("gpt-4o")
    model.key = os.getenv("OPENAI_API_KEY")

    local_content = Path(filename)
    if not local_content.exists():
        print(f"File {filename} does not exist.")
        return
    contents = local_content.read_text()

    generate_recipe(contents)


def generate_recipe_from_url(url: str):
    contents = requests.get(url).text
    generate_recipe(contents, url)


def generate_recipe(contents: str, url: str | None = None):
    model = llm.get_model("gpt-4o")
    model.key = os.getenv("OPENAI_API_KEY")

    prompt_template = Path("prompt_template.txt").read_text()

    recipe_prompt = prompt_template.replace("{{CONTENTS}}", contents)
    if url:
        recipe_prompt = recipe_prompt.replace("{{URL}}", url)
    recipe_content = model.prompt(recipe_prompt).text()

    # Generate filename
    filename_prompt = f"""
    Based on the following recipe content, suggest a concise (at most 3 words),
    hyphen-separated filename (without extension) that describes the recipe well:

{recipe_content}

Filename:"""
    suggested_filename = model.prompt(filename_prompt).text().strip()
    filename = sanitize_filename(suggested_filename) + ".md"

    # Save recipe content
    recipes_dir = "_recipes"
    os.makedirs(recipes_dir, exist_ok=True)
    file_path = os.path.join(recipes_dir, filename)
    with open(file_path, "w") as file:
        file.write(recipe_content)

    print(f"Generated recipe file: {file_path}")


if __name__ == "__main__":
    while True:
        url = input(
            "Enter the recipe URL, or 'txt' to use a text file, or 'q' to quit: "
        ).strip()
        if url.lower() == "txt":
            filename = input(
                "Enter the filename of the text file (default: contents.txt): "
            ).strip()
            if not filename:
                filename = "contents.txt"
            generate_recipe_from_text(filename)
        elif url.lower() == "q":
            break
        elif url:
            generate_recipe_from_url(url)
        else:
            print("Please enter a valid URL.")
