# Minimal example: call an LLM via OpenRouter's API.
import requests

API_KEY = open("lab_5_classification/auth.txt", "r").readline()

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "google/gemini-3.1-flash-lite-preview",
        "messages": [
            {
                "role": "user", 
                "content": "Vous voulez évaluer les résultats d'un moteur de recherche. Il retourne 10 résultats. 6 d'entre eux sont pertinents, mais il y aurait 10 millions de résultats pertinents dans l'ensemble de votre corpus. Calculez la précision et le rappel."
                }
            ],
    },
)

print("\n\nfull response:")
print(response.json())

print("\n\njust the text:")
print(response.json()["choices"][0]["message"]["content"])