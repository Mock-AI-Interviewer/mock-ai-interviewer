from backend.conf import initialise_app, get_eleven_labs_api_key
from elevenlabs import generate, play, set_api_key, stream

initialise_app()

audio_stream = generate("Hello world", stream=True)
stream(audio_stream)
