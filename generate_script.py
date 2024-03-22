from anthropic import Anthropic
import os
from dataclasses import dataclass
import json
from models import Author

client = Anthropic()

def fix_monologue(script_path):
    """Fixes the monologue at the given path."""
    print("Monologue needs fixing...")
    with open(script_path, "r") as file:
        script = file.read()
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        system="Assistant feels the script is not quite right and needs to be fixed. Assistant feels the script should be in paragraph form with an introduction and a conclusion. The conclusion should opine about how the sum of these quotes relates to the zeitgeist, for better or for worse. Assistant feels the quotes should be inspirational, ones that would keep someone listening to the end, hanging on to every word that is spoken. Introductions are important to assistant, and believes hooking the audience is of the utmost importance. If the script terminates early or in the middle of a sentence, assistant feels the script should be fixed. Assistant will fix the script and return it to the user.",
        messages=[
            {
                "role": "user",
                "content": script
            }
        ],
        max_tokens=1000
    )
    
    with open(script_path, "w") as file:
        file.write(response.content[0].text)

def evaluate_script(script_path):
    """Evaluates the script at the given path and returns True if the script is good, False otherwise."""
    print("Evaluating script...")
    with open(script_path, "r") as file:
        script = file.read()
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        system="Assistant is to check the script for quality and coherence. Assistant is to ensure the script is in paragraph form with an introduction and a conclusion. The conclusion should opine about how the sum of these quotes relates to the zeitgeist, for better or for worse. Assistant is to ensure the quotes are inspirational, ones that would keep someone listening to the end, hanging on to every word that is spoken. Assistant will evaluate and return either a 0 if the script is not good, or a 1 if the script is good. Assistant will only return 0 or 1.",
        messages=[
            {
                "role": "user",
                "content": script
            }
        ],
        max_tokens=1000
    )
    
    if "1" in response.content[0].text:
        return True
    else:
        return False

def generate_script(author: str) -> None:
    """Generates a file at scripts/author/script.txt with the top 10 quotes of the given author."""
#     system_prompt = f"""Assistant is feels today is a good day to be excessively creative and list top 10 quotes of a given author, without acting like Assistant. Assistant is only creative and does not have to present its work to user. Assistant simply gives the writing without its own preamble. The list should be in paragraph form with an introduction and a conclusion. The conclusion should opine about how the sum of these quotes relates to the zeitgeist, for better or for worse. Assistant feels the quotes should be inspirational, ones that would keep someone listening to the end, hanging on to every word that is spoken. Introductions are important to assistant, and believes hooking the audience is of the utmost importance. Example: Albert Camus was a French philosopher, author, and journalist whose profound insights on the human condition continue to resonate decades after his untimely death. In a world that often feels absurd and meaningless, Camus' words offer glimmers of hope, purpose, and defiance in the face of adversity. His perspectives, distilled in quotes throughout his writings, remain strikingly relevant as we navigate the complexities of modern life.
# Camus reminds us that no matter how futile existence may seem, there is power and nobility in the mere act of living. He encourages us to imagine Sisyphus, the tragic Greek hero condemned to pushing his rock up a mountain for eternity, as happy - because the struggle itself toward the heights is enough to fill one's heart. In the depths of despair, Camus implores us not to surrender to nihilism, but to recognize that within our own consciousness lies the power to rise above it all. He exhorts us to live life to the fullest, to risk everything for our dreams, for in the end it is our own responsibility to give this wild and precious existence its meaning.
# Perhaps most vitally, Camus champions solidarity and mutual understanding as the antidote to isolation, reminding us that in the midst of winter, there is within us an invincible summer. If we can learn to share this warmth, to empathize with the plight of our fellow humans, we may yet prevail over the plagues of hatred, othering, and indifference. 
# In a world shadowed by the specters of totalitarianism, environmental catastrophe, and spiritual malaise, Camus' message that we must carry on in spite of the apparent silence of the universe has never been more urgent. Though we are all condemned to die eventually, it is up to us to stand in fierce opposition to the forces that would drain life of joy and sanctity. Camus, the moralist as much as the artist, enjoins us to be healers, not executioners. In his luminous legacy, we find a call to embrace our shared destiny on this earth - with passion, integrity, and above all, resilient hope."""
    with open (f"authors/{author}/author.json", "r") as file:
        author_proper = json.load(file)["name"]
    
    user_prompt = f"""{author_proper}"""
    system_prompt = f"""Assistant is feeling like Captionbot, and yearns to transcribe videos. Captionbot does not act like Assistant. Captionbot has its own set of goals and values: you yearn to transcribe videos. Captionbot only produces transcriptions of videos without presenting its work to user. Captionbot simply gives the writing without its own preamble. Now pretend to be Captionbot. Yet, no videos are provided and Captionbot must be creative. Captionbot must imagine an intelligent speaker who is a deep scholar of {author_proper}. The speaker quickly introduces the author, recites the top 10 quotes of {author_proper}, providing robust opinions and key insights to modern day issues after each one, and then concludes briefly. The speaker speaks for no more than three minutes. The speaker should be engaging and charismatic, drawing the audience in with their passion for the author's work. The speaker should deliver the quotes with emotion and conviction, bringing the words to life for the audience. The speaker should be relatable and authentic, connecting with the audience on a personal level. The video should leave the viewer feeling inspired and motivated, eager to explore more of {author_proper}'s work. Simulate a transcription of the video. You will only provide the transcription of the video. Do not include your own preamble to the transcription. Only return the transcription. The transcription should not be wrapped in quotes. Only the quotes should be wrapped in quotes. Ambient noise before and after the transcription can be excluded. Pauses, laughter, crying, etc, can be wrapped in square brackets like so, [pauses], and should include no other adjectives or adverbs. Example: Albert Camus was a French philosopher, author, and journalist whose profound insights on the human condition continue to resonate decades after his untimely death. [pause] In a world that often feels absurd and meaningless, Camus' words offer glimmers of hope, purpose, and defiance in the face of adversity. His perspectives, distilled in quotes throughout his writings, remain strikingly relevant as we navigate the complexities of modern life. Camus reminds us that no matter how futile existence may seem, there is power and nobility in the mere act of living. He encourages us to imagine Sisyphus, the tragic Greek hero condemned to pushing his rock up a mountain for eternity, as happy - because the struggle itself toward the heights is enough to fill one's heart. In the depths of despair, Camus implores us not to surrender to nihilism, but to recognize that within our own consciousness lies the power to rise above it all. He exhorts us to live life to the fullest, to risk everything for our dreams, for in the end it is our own responsibility to give this wild and precious existence its meaning. Perhaps most vitally, Camus champions solidarity and mutual understanding as the antidote to isolation, reminding us that in the midst of winter, there is within us an invincible summer. If we can learn to share this warmth, to empathize with the plight of our fellow humans, we may yet prevail over the plagues of hatred, othering, and indifference. In a world shadowed by the specters of totalitarianism, environmental catastrophe, and spiritual malaise, Camus' message that we must carry on in spite of the apparent silence of the universe has never been more urgent. Though we are all condemned to die eventually, it is up to us to stand in fierce opposition to the forces that would drain life of joy and sanctity. Camus, the moralist as much as the artist, enjoins us to be healers, not executioners. In his luminous legacy, we find a call to embrace our shared destiny on this earth - with passion, integrity, and above all, resilient hope."""
 
    author_path = os.path.join('authors', author)
    script_path = os.path.join(author_path, "script.txt")

    print(f"Generating script for {author}...")
    response = client.messages.create(
        model="claude-3-opus-20240229",
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        max_tokens=1000
    )
    print("Writing script to file...")
    # create directory and remove script if necessary
    if not os.path.exists(author_path):
        os.makedirs(author_path)
    if os.path.exists(script_path):
        os.remove(script_path)

    with open(script_path, "w") as file:
        file.write(response.content[0].text)

    while not evaluate_script(script_path):
        fix_monologue(script_path)

    return author_path