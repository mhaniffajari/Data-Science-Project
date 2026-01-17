from google import genai
from google.genai.types import HttpOptions

import logging
from google.cloud import logging as gcp_logging

# ------  Below cloud logging code is for Qwiklab's internal use, do not edit/remove it. --------
# Initialize GCP logging
gcp_logging_client = gcp_logging.Client()
gcp_logging_client.setup_logging()

client = genai.Client(
    vertexai=True,
    project='qwiklabs-gcp-02-8219d56df5a7',
    location='europe-west1',
    http_options=HttpOptions(api_version="v1")
)
chat = client.chats.create(model="gemini-2.5-flash")
response_text = ""

for chunk in chat.send_message_stream("What are all the colors in a rainbow?"):
    print(chunk.text, end="")
    response_text += chunk.text

