import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"
REQUEST_TIMEOUT = 120


def generate_with_ollama(
    prompt: str,
    temperature: float = 0.0,
) -> str:

    if not prompt or not prompt.strip():
        return ""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        print("OLLAMA HTTP STATUS:", response.status_code)

        response.raise_for_status()

        data = response.json()

        return str(
            data.get("response", "")
        ).strip()

    except requests.exceptions.RequestException as e:
        print("OLLAMA REQUEST ERROR:", e)
        return ""

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return ""