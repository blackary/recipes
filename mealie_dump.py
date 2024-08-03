import json
import os

# Load the JSON data from the file
with open("mealie_backup.json", "r") as file:
    data = json.load(file)

# Extract recipes data, instructions, and ingredients
recipes = data["recipes"]
instructions_data = data["recipe_instructions"]
ingredients_data = data["recipes_ingredients"]  # Correct key for ingredients

# Ensure the _recipes directory exists
os.makedirs("_recipes", exist_ok=True)


# Function to create Markdown content for each recipe
def create_markdown(recipe, instructions, ingredients):
    # YAML front matter
    markdown_content = "---\n"
    markdown_content += "layout: recipe\n"
    markdown_content += f"title: \"{recipe['name']}\"\n"
    if (
        "image" in recipe
        and recipe["image"] is not None
        and recipe["image"].startswith("http")
    ):
        markdown_content += f"photo: {recipe.get('image')}\n"
    markdown_content += "ingredients:\n"
    # Extract ingredients for this recipe
    for ingredient in ingredients:
        if ingredient["recipe_id"] == recipe["id"]:
            markdown_content += f"  - {ingredient['note']}\n"
    markdown_content += "instructions:\n"
    # Extract instructions for this recipe
    for instruction in instructions:
        if instruction["recipe_id"] == recipe["id"]:
            markdown_content += f"  - {instruction['text']}\n"
    markdown_content += f"servings: {recipe.get('recipe_yield', 'N/A')}\n"
    markdown_content += "---\n\n"
    # Description
    markdown_content += f"{recipe.get('description', 'No description available.')}\n\n"
    return markdown_content


# Create a Markdown file for each recipe
for recipe in recipes:
    # Filter instructions and ingredients for the current recipe
    recipe_instructions = [
        inst for inst in instructions_data if inst["recipe_id"] == recipe["id"]
    ]
    recipe_ingredients = [
        ing for ing in ingredients_data if ing["recipe_id"] == recipe["id"]
    ]
    filename = f"_recipes/{recipe['slug']}.md"
    content = create_markdown(recipe, recipe_instructions, recipe_ingredients)
    with open(filename, "w") as md_file:
        md_file.write(content)
    print(f"Markdown file created: {filename}")
