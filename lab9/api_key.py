import os
from dotenv import load_dotenv, find_dotenv, set_key

def load_key():
    """Loads the OpenRouter API key.

    Checks the environment variable OPENROUTER_API_KEY first.
    Then checks the .env file.
    If not found, prompts the user to enter it and saves it to .env.

    Returns:
        str: The OpenRouter API key.
    """
    # 1. Check environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return api_key

    # 2. Check .env file
    # find_dotenv() will search for .env in parent directories
    dotenv_path = find_dotenv()
    # load_dotenv() loads the environment variables from the .env file
    load_dotenv(dotenv_path)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        return api_key

    # 3. Ask user and write to .env
    print("OpenRouter API Key not found in environment variables or .env file.")
    api_key = input("Please enter your OpenRouter API Key: ").strip()

    if not dotenv_path:
        dotenv_path = os.path.join(os.getcwd(), ".env")
        with open(dotenv_path, "w") as f:
            f.write("# .env file created by load_key.py\n")
        print(f".env file created at {dotenv_path}")

    set_key(dotenv_path, "OPENROUTER_API_KEY", api_key)
    print("API Key saved to .env file.")

    return api_key

if __name__ == "__main__":
    key = load_key()
    print(f"Loaded Key: {key}") 