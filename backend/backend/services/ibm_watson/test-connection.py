from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

authenticator = IAMAuthenticator("")
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('')

with open('hello_world.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            'Hello world, My name is Mock AI Interviewer and I am here to help you prepare for your interview. I will ask you a few questions and you will have a few seconds to answer each question. Let us begin.',
            voice='en-US_AllisonV3Voice',
            accept='audio/wav'        
        ).get_result().content)