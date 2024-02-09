# pylint: disable=no-member
"""
This is a module-level docstring.

You can provide a brief description of what the module does, its purpose,
and any other relevant information.

Example:
    How to use this module:
    ```
    import my_module

    my_module.some_function()
    ```
"""
# pylint: disable=C0116
# pylint: disable=C0412
# pylint: disable=C0301
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Enable CORS (Cross-Origin Resource Sharing)
# Allow all origins during development (update this for production)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Set up OpenAI API key
openai.api_key = "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"  # Replace with your actual API key

# Debugging statement
logging.debug("API Key: %s", openai.api_key)

# Root route
@app.get("/")
def read_root():
    """Root route returning a simple message."""
    return {"Hello": "World"}

class TextPrompt(BaseModel):
    """Model defining the structure of the text prompt."""
    prompt: str

@app.post("/generate-text")
def generate_text(prompt_obj: TextPrompt) -> dict:
    """
    Generate text based on the given prompt.

    Args:
        prompt_obj (TextPrompt): The input prompt for text generation.

    Returns:
        dict: A dictionary containing the generated text.
    """
    try:
        # Logging the start of the text generation process
        logging.debug("Generating text for prompt: %s", prompt_obj.prompt)

        # Make a request to OpenAI with the correct chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_obj.prompt},
            ],
            max_tokens=500
        )

        # Logging the OpenAI response
        logging.debug("OpenAI response: %s", response)

        # Extract the generated text from the response
        generated_text = response['choices'][0]['message']['content'].strip()

        # Logging the generated text
        logging.debug("Generated text: %s", generated_text)

        return {"generated_text": generated_text}

    except Exception as e:
        # Logging any exceptions that occur during the process
        logging.error("An error occurred: %s", e)
        return {"error": "An error occurred during text generation."}
