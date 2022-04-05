
 [![Mailing list : test](http://img.shields.io/badge/Email-gray.svg?style=for-the-badge&logo=gmail)](mailto:ashutosh.dongare@gmail.com) [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-GNU%20AGPL%203.0-lightgrey.svg?style=for-the-badge)](https://github.com/AshutoshDongare/convo/blob/main/LICENSE)


# convo - Enterprise grade continuous speech conversationalist

![header](https://user-images.githubusercontent.com/18417621/161523640-a8cb4eea-0f74-4fff-ba0a-02182bd03a33.png)

convo birngs together [silero](https://github.com/snakers4/silero-models) and [rasa](https://github.com/RasaHQ) to create continuous speech conversationalist experience like Alexa or Google dot. 

 - [silero](https://github.com/snakers4/silero-models) STT and TTS models provide the quality comparable to Google's STT (and sometimes even better) but they are not  Google. See silero performance [benchmarks](https://github.com/snakers4/silero-models/wiki/Quality-Benchmarks) 

 - [rasa](https://github.com/RasaHQ) is an enterprise-grade chatbot built on python and Transformer based language models providing state-of-the-art framework comparable or better than top cloud based chatbot frameworks 

convo can run easily on a local cpu based machine, thus convo provides high response times at no cloud service costs.

Typical STT and TTS infernece time on a local machine for one sentence is less than 0.5 seconds each and rasa bot response time is around 1-2 seconds. This can be improved even further by fine tuning and using dedicated machines. 
  
convo advantages:
- High performance as the framework can run locally on a cpu;
- No cloud charges so this can be implemented for masses;
- highly customizable using rasa custom action server to add any desired functionality;
- Can support multiple languages as supported by silero models

convo does not use any hotword detection mechanism however it can stop speaking by speaker requesting with keywords like stop / quit / exit.   


# Installation and Basics

There are 2 base softwares / frameworks those need to be installed for setting up convo 

- [rasa](https://github.com/RasaHQ)
- [silero](https://github.com/snakers4/silero-models)


## rasa Installation steps

1) Create a python virtual environment named "rasa" with suitable python version mentioned in [rasa installation here](https://rasa.com/docs/rasa/installation/). Current version of rasa version 3.x requires python 3.7 or 3.8. enable rasa virtual environment before following below installation steps.

2) Install rasa using 
```
 pip install rasa
```  
3) Run "rasa init" on the terminal. please follow on screen instructions to complete creating rasa chatbot instance. 
```
 rasa init
```
    
4) Once you have rasa chatbot instance installed you can check if it is working properly by running rasa shell that lets you talk to your assistant on the command line     
```
 rasa shell
```
   This will run rasa server and let you chat with it on terminal. Please enter "/stop" to stop rasa server.
    
5) We would be calling this rasa chatbot using rest api call. When we want to communicate with rasa chatbot, we will need to start rasa using 
```
 rasa run --enable-api
```

# silero Installation steps
    
1) Create a python virtual environment named "silero" with latest python version 
    
2) There are quite a few dependencies for running silero. we will go through them in following steps
    
3) Install pytorch using instructions on https://pytorch.org/get-started/locally/ - if you are on windows & cpu only, this command may look like below
    
``` 
pip install torch torchvision torchaudio
```

4) Additionally we need following python packages
    
```
pip install PySoundFile SpeechRecognition omegaconf
```

speechRecognition is a wrapper liberary that allows performing speech recognition using multiple ASR services including google cloud speech etc. We will only be using this liberarty to capture and record audio since it provides detecting voice activity and ending mic recording when user stops speaking.
    
5) we also need pyaudio installed. On windows 10-11 you may encounter error installing pyaudio. Please use following commands to install pyaudio in that case.
    
``` 
pip install pipwin 
    
pipwin install pyaudio 
```

6) convo uses imports from silero those are already included in this repo. please check an ensure that silero model and utils are at the right place

With that we are done with the installation steps. Now try running convo.py in the terminal using silero virtual environment and you should be able to speak with your computer :thumbsup:
```
python convo.py
```

when you run convo for the first time, it will download silero models to cache. Download Progress will be displayed in the output terminal. In subsequent runs it will use locally cached models which will be fast.

# Troubleshooting tips

if you are not able to speak with your computer then try checking below points

1) Please check if your mic and speaker are enabled. on windows you may also need to check permissions etc.
2) Please check if all the mentioned liberaries are installed properly and you are running both silero and rasa in their own virtual environments
3) Please check if are running rasa server from inside of the rasa bot directory using "rasa run --enable-api" and it said rasa server is up and running
4) If you have had some compatibility errors while installing on the virtual environments, you may want to delete and recreate them
5) In future there might be a change in the avaliable liberaries or compatibility, please do check for those kind of issues.
 

## Citations

  - https://github.com/RasaHQ

  - https://github.com/snakers4/silero-models


## Future enhancements

This repo presents the base working implementation of convo. This can be further enhanced in many ways. Some of the enhancements are mentioned below 
 - Add more functionality to rasa like chitchat, faq and api calls to more "skills"
 - Add more communication languages and speakers
 - perform in momery processing of audio improving performance further
