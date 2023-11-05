from backend.conf import initialise_app, get_eleven_labs_api_key

initialise_app()


from elevenlabs import generate, play, set_api_key, stream


set_api_key(get_eleven_labs_api_key())

  
audio_stream = generate("Hello world", stream=True)  
stream(audio_stream)