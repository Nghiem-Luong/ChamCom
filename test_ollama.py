import ollama


response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Xin chào, hãy trả lời bằng tiếng Việt. Bạn đang làm nhiệm vụ gì?"
        }
    ]
)


print(response["message"]["content"])
