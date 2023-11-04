import openai
from backend.conf import (
    get_openai_model,
    initialise,
    get_openai_api_key,
    get_openai_organisation,
)

initialise()
openai.organization = get_openai_organisation()
openai.api_key = get_openai_api_key()

completion = openai.ChatCompletion.create(
  model=get_openai_model(),
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello! please reply back to me with a 10 word essay on going to church"}
  ],
  stream=True
)

full_text = []
for chunk in completion:
    delta = chunk.choices[0].delta
    finish_reason = chunk.choices[0].finish_reason
    timestamp = chunk.created
    if delta:
        full_text.append(delta.content)
        print(delta, finish_reason, timestamp)
    else:
        print("no delta")

print("full text: ","".join(full_text))