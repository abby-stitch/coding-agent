# llm.py
import os
from openai import OpenAI

def get_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as f:
        return f.read().strip()

client = OpenAI(
    api_key=get_api_key(),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout=30
)

def call_llm(prompt):
    try:
        completion = client.chat.completions.create(
            model="qwen-turbo",  # 或 qwen-max（如果你有额度）
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"调用出错：{e}")
        return None

def save_file(filepath: str, content: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def read_project_plan():
    plan_path = "outputs/project_plan.txt"
    if not os.path.exists(plan_path):
        raise FileNotFoundError("❌ project_plan.txt 不存在，请先运行 Planning Agent")
    with open(plan_path, "r", encoding="utf-8") as f:
        return f.read().strip()