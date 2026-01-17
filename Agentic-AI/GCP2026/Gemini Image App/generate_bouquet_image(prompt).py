import argparse

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google import genai
from google.genai.types import HttpOptions, Part

def generate_image(
    project_id: str, location: str, output_file: str, prompt: str
) -> vertexai.preview.vision_models.ImageGenerationResponse:
    """Generate an image using a text prompt.
    Args:
      project_id: Google Cloud project ID, used to initialize Vertex AI.
      location: Google Cloud region, used to initialize Vertex AI.
      output_file: Local path to the output image file.
      prompt: The text prompt describing what you want to see."""

    vertexai.init(project=project_id, location=location)

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

    images = model.generate_images(
        prompt=prompt,
        # Optional parameters
        number_of_images=1,
        seed=1,
        add_watermark=False,
    )

    images[0].save(location=output_file)

    return images

generate_image(
    project_id='qwiklabs-gcp-01-63d8a26e026b',
    location='europe-west4',
    output_file='image.jpeg',
    prompt='Create an image containing a bouquet of 2 sunflowers and 3 roses',
    )


def analyze_bouquet_image(image_path: str):
    """
    Analyze a bouquet image and generate birthday wishes based on the image
    using Gemini 2.5 Flash with streaming enabled.
    """

    # Initialize GenAI client
    client = genai.Client(
        vertexai=True,
        project='qwiklabs-gcp-01-63d8a26e026b',
        location='europe-west4',
        http_options=HttpOptions(api_version="v1"),
    )

    # Create chat session
    chat = client.chats.create(model="gemini-2.5-flash")

    # Read image as bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Create image Part (FIX)
    image_part = Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg"
    )

    prompt = (
        "Based on the bouquet in this image, write a warm, cheerful, and creative "
        "birthday wish. Mention the flowers if relevant."
    )

    response_text = ""

    # Stream response
    for chunk in chat.send_message_stream([prompt, image_part]):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            response_text += chunk.text

    return response_text

analyze_bouquet_image("image.jpeg")
