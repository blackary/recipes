import os
import re
import llm


def sanitize_filename(filename):
    return re.sub(r"[^a-z0-9-]", "-", filename.lower()).strip("-")


def generate_recipe(url):
    model = llm.get_model("gpt-4o")
    model.key = os.getenv("OPENAI_API_KEY")

    # Read prompt template
    with open("prompt_template.txt", "r") as file:
        prompt_template = file.read()

    # Generate recipe content
    recipe_prompt = prompt_template.replace("{{URL}}", url)
    recipe_content = model.prompt(recipe_prompt).text()

    # Generate filename
    filename_prompt = f"""Based on the following recipe content, suggest a concise (at most 3 words), hyphen-separated filename (without extension) that describes the recipe well:

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
        url = input("Enter the recipe URL (or 'q' to quit): ").strip()
        if url.lower() == "q":
            break
        if url:
            generate_recipe(url)
        else:
            print("Please enter a valid URL.")
