import os
from zipfile import Path
from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    """
    Sends the same prompt to the model multiple times to show that responses can vary.
    This is expected behavior: the model samples from probabilities rather than always
    producing the exact same output.
    """
    # Load variables from the .env file into the environment
    load_dotenv()

    # Read the API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Add it to a .env file like:\n"
            "OPENAI_API_KEY=your_api_key_here"
        )

    # Create an OpenAI client
    client = OpenAI(api_key=api_key)

    # The prompt for our experiment (keep it identical each time)
    prompt = "Explain what a large language model is in one paragraph."

    # Send the same prompt multiple times
    for i in range(3):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        print(f"\nResponse {i + 1}:\n")
        print(response.output_text)


if __name__ == "__main__":
    main()
