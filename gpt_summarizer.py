from openai import OpenAI
import os

client = OpenAI(
    api_key="YOUR_API_KEY",
)

def summarize(text, max_tokens=1000):
    """
        GPT API로 요약 요청
        """
    # 2) 새로운 패턴: client.chat.completions.create()
    response = client.chat.completions.create(
        model="YOUR_MODEL",
        messages=[
            {"role": "system", "content": "아래 유튜브 자막을 4000자 이내로 자세히 요약해줘."},
            {"role": "user", "content": text},
        ],
        max_tokens=max_tokens,
    )
    # 3) 결과 반환
    return response.choices[0].message.content
