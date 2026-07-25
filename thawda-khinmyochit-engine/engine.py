import json
import os
import sys
import requests

# ==========================================
# THAWDA SWE & KHIN MYO CHIT STYLISTIC PROMPT
# ==========================================
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
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "api_type": "openai",  # Options: openai, gemini, ollama, groq, custom
        "api_key": "YOUR_API_KEY_HERE",
        "model_name": "gpt-4o",
        "custom_url": ""
    }

def generate_content(topic_prompt, config):
    api_type = config.get("api_type", "openai").lower()
    api_key = config.get("api_key", "")
    model_name = config.get("model_name", "gpt-4o")

    headers = {"Content-Type": "application/json"}
    
    # Generic OpenAI API Compatible format (Works for OpenAI, Groq, Together, LocalLLM)
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
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"

    # Local Ollama Support for Termux / Local LLMs
    elif api_type == "ollama":
        url = config.get("custom_url") or "http://localhost:11434/api/generate"
        payload = {
            "model": model_name,
            "system": SYSTEM_PROMPT,
            "prompt": topic_prompt,
            "stream": False
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Error: {response.status_code} - {response.text}"

    else:
        return "Unsupported API Type configured."

if __name__ == "__main__":
    print("==================================================")
    print(" SSISM INTEL WIZAR HEROES ENGINE (Thawda-KhinMyoChit)")
    print("==================================================")
    
    config = load_config()
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("\nEnter Episode Title / Topic (e.g., 'Day 1: စီးချင်းထိုးပွဲ'): ")

    print(f"\nGenerating narrative using [{config.get('api_type')}] Engine...\n")
    output = generate_content(user_input, config)
    
    print("---------------- OUTPUT ----------------")
    print(output)
    print("----------------------------------------")
