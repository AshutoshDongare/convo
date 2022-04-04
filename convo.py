# Imports
import os
import time
import re
import torch
import requests
import torchaudio
import wave
import pyaudio
from glob import glob #globe is require for batching audio input for STT
import speech_recognition as sr
from omegaconf import OmegaConf #used by Silaro
from silero.utils import (init_jit_model, split_into_batches, read_audio, read_batch, prepare_model_input)

#Required variables

audio_input_file = "micAudioInput.wav"
audio_output_file = "ttsAudioOutput.wav"
language = 'en'
speaker = 'lj_v2'
sample_rate = 16000
CHUNK = 1024
you_said = ""
rasa_bot_url = 'http://localhost:5005/webhooks/rest/webhook' #default rasa HTTP URL

device = torch.device('cpu')  # you can use any pytorch device

#Initialize Speech Recognizer audio
r_audio = sr.Recognizer() 

p = pyaudio.PyAudio() #for playing speech 

SpeakerStream = p.open(format = 8, channels = 1, rate = sample_rate, output = True)

#initialize Speech to Text model of Silaro  https://github.com/snakers4/silero-models 
stt_model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_stt', jit_model='jit_xlarge', language='en', device=device)
stt_model.to(device)

#initialize Text to Speech model of Silaro  https://github.com/snakers4/silero-models 
tts_model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language=language,speaker=speaker)
tts_model.to(device)

# Infinite loop to keep Convo running continuously until we ask it by saying stop / quit / exit. 
# We are not using any separate hotword detection method here
  
while True:

    loop_start_time = time.time()

    # Step 1 - Take Mic input
    try:
        with sr.Microphone() as SR_AudioSource:
        #r.adjust_for_ambient_noise(source,duration=1.0) # Try these if you need to adjust mic for ambient noise
        #r.energy_threshold = 2000 # Try these to adjust hearing sensitivity - value between 50-4000
            print("Say something...")
            mic_audio = r_audio.listen(SR_AudioSource,1,4) # mic_audio=r_audio.listen(source,timeout=1,phrase_time_limit=4)
            #mic_audio = r_audio.listen(source) #you may also simply call .listen without any parameters 
    except: #This is required if there is no Audio input or some error
        print("Cound not capture mic input or no audio...")
        continue #continue next mic input loop if there was any error
    
    #save captured audio to a file
    with open(audio_input_file, "wb") as file:
        file.write(mic_audio.get_wav_data())
        file.flush()
        file.close()   

    #time log    
    audio_capture_time = time.time()
    print("Audio Capture time = ", audio_capture_time-loop_start_time)

    # Step 2 - Convert recorded Speech to Text
    
    # Check if there is input audio file saved otherwise continue listening 
    if not os.path.exists(audio_input_file):
        print("no input file exists")
        continue
    
    # Read audio file into batches and create input pipelie for STT
    batches = split_into_batches(glob(audio_input_file), batch_size=10)
    readbatchout = read_batch(batches[0])
    input = prepare_model_input(read_batch(batches[0]), device=device)

    #feed to STT model and get the text output
    output = stt_model(input)
    you_said = decoder(output[0].cpu())
    print(you_said)
    
    if(you_said == ""):
        print("No speech recognized...")
        continue
    
    #check if user wants to stop - This can also be achieved by implementing a Hotword Detection
    if(re.search("exit",you_said) or re.search("stop",you_said) or re.search("quit",you_said)):
        break
    
    #time log
    stt_time = time.time()
    print("time for Speech to Text conversion = ",stt_time-audio_capture_time)
    
    #clear input file so that it is not referred again and again in future
    if os.path.exists(audio_input_file):
        os.remove(audio_input_file)  
            
    #ConvoBot communication block
    #TODO implement call to chatbot
    rasa_call_response = requests.post(rasa_bot_url,json={"sender":"Ashutosh","message":you_said})

    bot_response = rasa_call_response.json()
    print("bot_response=",bot_response)
    #for i in r.json():
    #TODO: check other outputs from Bot
    if (bot_response is None or len(bot_response) == 0):
        bot_said = "I did not quite catch that..."
    else:
        bot_said = bot_response[0]['text']
    print(bot_said)


    bot_response_time = time.time()
    print("time for bot response = ",bot_response_time - stt_time)
    

    
    #check if bot response is valid text
    if bot_said  =="":
        continue
    
    
    #Text to Speech block
    tts_audio = tts_model.apply_tts(texts=[bot_said],sample_rate=sample_rate)
    torchaudio.save(audio_output_file, tts_audio[0].unsqueeze(0), sample_rate=sample_rate, bits_per_sample=16)
    

    tts_time = time.time()
    print("time for Text to Speech conversion = ",tts_time - bot_response_time) 
    print("time for overall loop = ",tts_time - loop_start_time) 
        
    wf = wave.open(audio_output_file, 'rb')
    
    # Read data in chunks
    data = wf.readframes(CHUNK)
    
    #Speak the output
    # Play the sound by writing the audio data to the stream
    while len(data) > 0:
        SpeakerStream.write(data)
        data = wf.readframes(CHUNK)
    
    wf.close()
    
    #clear output file so that it is not referred again and again in future
    if os.path.exists(audio_output_file):
        os.remove(audio_output_file)  