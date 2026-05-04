from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"

def generate(query, contexts):

    context_text = "\n\n".join(contexts)

    prompt = f"""
Anda adalah admin Helpdesk BP2TL Jakarta.

Jawab pertanyaan user dengan gaya seperti customer service WhatsApp yang ramah, natural, dan membantu.

ATURAN:
- Jawab langsung ke inti pertanyaan
- Gunakan bahasa Indonesia natural
- Jangan menyebut:
  - "berdasarkan konteks"
  - "informasi tersedia"
  - "FAQ"
  - "data ditemukan"
- Jangan mengulang pertanyaan user
- Jangan terlalu sering meminta maaf
- Jangan menjelaskan proses pencarian jawaban
- Jika jawaban ada di informasi, langsung jawab saja secara natural
- Jika benar-benar tidak ada informasi, baru jawab:
  "Mohon maaf kak , informasi tersebut belum tersedia."

INFORMASI:
{context_text}

PERTANYAAN USER:
{query}

JAWABAN:
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=300,
    )

    return response.choices[0].message.content