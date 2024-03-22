import os
import torch
import json
from pydub import AudioSegment

def generate_image_sequence(pipe, refiner_pipe, path):
    with open(os.path.join(path, "author.json"), "r") as file:
        author = json.load(file)

    prompt = f"portrait of {author['name']} in their hometown of {author['birthplace']}. {author['literaryPeriod']}, around {author['birthday']}. high resolution, dynamic lighting, and a sense of the author's personality."
    path = os.path.join(author["name"], "images")
    
    image = generate_initial_image(pipe, prompt, path)

    voiceover = AudioSegment.from_wav(os.path.join(author["name"], "voiceover.wav"))
    voiceover_length = len(voiceover) / 1000 # in seconds
    
    fps = 12
    strength = 0.7
    generator = torch.Generator(device="cuda").manual_seed(3523435)

    for i in range(voiceover_length / fps):
        path = os.path.join(author["name"], "images", f"image-{i}.jpg")
        image = generate_variant_image(image, path, prompt, strength, generator, refiner_pipe)
    
def generate_initial_image(pipe, prompt: str, path: str):
    pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)

    image = pipe(prompt, num_inference_steps=75, high_noise_frac=0.7).images[0]
    save_image(image, os.path.join(path, "image-init.jpg"))

    return image

def generate_variant_image(image, path, prompt, strength, generator, pipe):
    image = pipe(prompt=prompt, image=image, num_inference_steps=150, strength=strength, guidance_scale=7.5, generator=generator, num_images_per_prompt=1).images[0]
    save_image(image, path)

    return image

def save_image(image, author_path):
    if not os.path.exists("images"):
        os.makedirs("images")
        
    if not os.path.exists(author_path):
        os.mkdir(author_path)

    image.save(os.path.join(author_path, "image-init.jpg"))
