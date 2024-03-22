from anthropic import Anthropic
import json
from os.path import join, exists
from os import makedirs

client = Anthropic()

def generate_authors():
    """Generates a file at authors.txt with the top 10 quotes of the given author."""
    system_prompt = f"Assistant knows a deep well of literary history. When prompted, assistant will return a list of the top 25 most influential authors in history. Assistant will return a list of objects containing the author's name, birthday, birthplace, and literary period in JSON format. Assistant's responses should contain nothing other than valid JSON. There should be no superfluous text. Your output should contain only JSON."

    print("Generating authors...")
    response = client.messages.create(
        model="claude-3-opus-20240229",
        messages=[
            {
                "role": "user",
                "content": system_prompt
            }
        ],
        max_tokens=4096
    )

    data = json.loads(response.content[0].text)

    for author in data:
        if not exists(join('authors', author["name"].lower().replace(" ", "-"))):
            makedirs(join('authors', author["name"].lower().replace(" ", "-")))
            
        path = join('authors', author["name"].lower().replace(" ", "-"), "author.json")
        with open(path, "w") as file:
            json.dump(author, file)

    return data
    
    