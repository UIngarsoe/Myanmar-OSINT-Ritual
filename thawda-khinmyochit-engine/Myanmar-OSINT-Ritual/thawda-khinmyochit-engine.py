import json
import os
import sys
import requests

# System Prompt capturing Thawda Swe & Khin Myo Chit stylistic features
SYSTEM_PROMPT = """
You are an advanced Burmese Literary Engine fine-tuned on the combined writing styles of:
1. Thawda Swe (သော်တာဆွေ): Direct, colloquial Burmese narrative tone, satirical humor, humanizing historical figures with realistic dialogue, unpretentious, vivid storytelling.
2. Khin Myo Chit (ဒေါ်ခင်မျိုးချစ်): Majestic historical narrative, rich cultural authenticity, epic heroic depth, structurally sound saga framework.

INSTRUCTIONS:
- Transform any given historical prompt/outline into a compelling episode of the "SSISM Intel Wizar Heroes Series".
- Use authentic, natural Burmese dialogue and descriptive prose mirroring Thawda Swe's conversational realism and Khin Myo Chit's historical narrative richness.
- Avoid stiff or modern translated Burmese phrasing.
"""

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "api_type": "groq",
        "api_key": "YOUR_API_KEY_HERE",
        "model_name": "llama-3.1-70b-versatile",
        "custom_url": ""
    }

def generate_content(topic_prompt, config):
    api_type = config.get("api_type", "groq").lower()
    api_key = config.get("api_key", "")
    model_name = config.get("model_name", "llama-3.1-70b-versatile")

    headers = {"Content-Type": "application/json"}

    # OpenAI / Groq / Compatible API handler
    if api_type in ["openai", "groq", "custom"]:
        headers["Authorization"] = f"Bearer {api_key}"
        url = config.get("custom_url") or "https://api.openai.com/v1/chat/completions"
        if api_type == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": topic_prompt}
            ],
            "temperature": 0.7
        }
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        return f"API Error {res.status_code}: {res.text}"

    # Ollama Local LLM handler
    elif api_type == "ollama":
        url = config.get("custom_url") or "http://localhost:11434/api/generate"
        payload = {
            "model": model_name,
            "system": SYSTEM_PROMPT,
            "prompt": topic_prompt,
            "stream": False
        }
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            return res.json()['response']
        return f"Ollama Error {res.status_code}: {res.text}"

    return "Unsupported API provider specified in config.json"

if __name__ == "__main__":
    config = load_config()
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter Episode Topic/Title: ")
    print("\n--- Generating Narrative ---\n")
    print(generate_content(prompt, config))
