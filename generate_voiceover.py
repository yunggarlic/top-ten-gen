from pydub import AudioSegment
import scipy
import os
import shutil

def split_outside_quotes(transcript, delimiter='.', quote_char='"'):
    result = []
    current_chunk = []
    inside_quotes = False
    
    for char in transcript:
        if char == quote_char:
            inside_quotes = not inside_quotes
        if char == delimiter and not inside_quotes:
            result.append(''.join(current_chunk))
            current_chunk = []
        else:
            current_chunk.append(char)
    
    # Add the last chunk if it's not empty
    if current_chunk:
        result.append(''.join(current_chunk))
    
    return result

def generate_voiceover(path, processor, model, voice_preset):
    with open(os.path.join(path, 'script.txt'), "r") as file:
        transcript = file.read()

    transcript = split_outside_quotes(transcript)
    print('Transcript:', transcript)

    print('Loading synthesiser...', path)
    for i, chunk in enumerate(transcript):
        chunk = chunk.strip()
        chunk += " [pause]"
        print(f'Generating voiceover for chunk: {chunk}...')
        inputs = processor(text=chunk, voice_preset=voice_preset).to("cuda")
        audio_array = model.generate(**inputs, semantic_max_new_tokens=2000)
        audio_array = audio_array.cpu().numpy().squeeze()

        if not os.path.exists(os.path.join(path, 'voiceover-segments')):
            os.makedirs(os.path.join(path, 'voiceover-segments'))

        sample_rate = model.generation_config.sample_rate
        vo_path = os.path.join(path, 'voiceover-segments', f"voiceover-{i}.wav")
        scipy.io.wavfile.write(vo_path, sample_rate, audio_array)

    print('Combining voiceover segments...')
    voiceover = AudioSegment.empty()
    for i in range(len(transcript)):
        voiceover += AudioSegment.from_wav(os.path.join(path, 'voiceover-segments', f"voiceover-{i}.wav"))
    voiceover.export(os.path.join(path, 'voiceover.wav'), format="wav")

    shutil.rmtree(os.path.join(path, 'voiceover-segments'))

    return path