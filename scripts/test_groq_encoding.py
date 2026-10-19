from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": (
                "Reply with exactly this sentence and nothing else: "
                "The employee has 12 days of casual leave. "
                "Use normal ASCII punctuation."
            ),
        }
    ],
    temperature=0,
)

answer = completion.choices[0].message.content

print(repr(answer))
print(answer)