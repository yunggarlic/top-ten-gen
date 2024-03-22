# Generate a script of the top 10 quotes of a given author
# Create a voice over of the quotes
# Create a generated sora video of the author doing day to day tasks

from generate_script import generate_script
from generate_authors import generate_authors
from generate_voiceover import generate_voiceover
from generate_image_sequence import generate_image_sequence
from diffusers import StableDiffusionXLImg2ImgPipeline
import torch
import os

# [generate_image_sequence(pipe, refiner_pipe, author_path) for author_path in [generate_voiceover(author_path) for author_path in [generate_script(author) for author in generate_authors()]]]

# generate_authors()

from transformers import AutoProcessor, BarkModel

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark").to("cuda")
model.enable_cpu_offload()
voice_preset = "v2/en_speaker_7"

# generate_authors()

for author in os.listdir('authors'):
    generate_script(author)
    generate_voiceover(os.path.join('authors',author), processor, model, voice_preset)
    
pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe = pipe.to("cuda")

refiner_pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
refiner_pipe = refiner_pipe.to("cuda")

for author in os.listdir('authors'):
    generate_image_sequence(pipe, refiner_pipe, os.path.join('authors',author))