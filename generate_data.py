# generate_data.py
from llm import call_llm, save_file, read_project_plan
from config import CURRENT_TEST_CASE
import os

PROMPT_DIR = f"test_cases/{CURRENT_TEST_CASE}"

def generate_paper_data():
    # 读取 plan 和 prompt
    plan = read_project_plan()
    with open(f"{PROMPT_DIR}/data_prompt.txt", "r", encoding="utf-8") as f:
        base_prompt = f.read()

    # 拼接：plan + prompt
    full_prompt = f"""
项目规划如下：
{plan}

请根据上述规划和以下要求生成数据：
{base_prompt}
"""

    print("正在生成模拟论文数据...")
    json_str = call_llm(full_prompt)

    # 清理可能的 Markdown 包裹
    if json_str.strip().startswith("```json"):
        json_str = "\n".join(json_str.strip().split("\n")[1:-1])
    elif json_str.strip().startswith("```"):
        json_str = "\n".join(json_str.strip().split("\n")[1:-1])

    save_file("outputs/papers.json", json_str)
    print("✅ 论文数据已保存: outputs/papers.json")

if __name__ == "__main__":
    generate_paper_data()