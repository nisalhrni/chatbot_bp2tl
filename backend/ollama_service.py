import requests
import config
from typing import List

class OllamaService:
    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.LLM_MODEL

    def generate(self, query: str, contexts: List[str]) -> str:
        context_text = "\n\n".join([f"Konteks {i+1}:\n{ctx}" for i, ctx in enumerate(contexts)])

        prompt = f"""
Konteks yang tersedia:
{context_text}

Pertanyaan: {query}

Jawaban:"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "top_p": 0.9,
                    }
                },
                timeout=180
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"Mohon maaf kak, sistem sedang mengalami gangguan. Silakan coba lagi atau cek: https://linktr.ee/bpptljkt"

        except requests.exceptions.ConnectionError:
            return "Mohon maaf kak, layanan AI sedang offline."
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Mohon maaf kak, terjadi kesalahan. Silakan coba lagi atau cek: https://linktr.ee/bpptljkt"

ollama_service = OllamaService()
