# html_agent.py
from llm import call_llm, save_file, read_project_plan
from config import CURRENT_TEST_CASE
import os
import re

PROMPT_DIR = f"test_cases/{CURRENT_TEST_CASE}"

def extract_html_from_llm_response(text: str) -> str:
    """
    从 LLM 响应中提取纯 HTML 内容。
    支持：
      - ```html ... ```
      - ``` ... ```
      - 或直接返回原文（如果无代码块）
    """
    match = re.search(r"```(?:html)?\s*\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_all_html_pages():
    plan = read_project_plan()

    # --- 首页 ---
    print(" 🏠 正在生成首页 (index.html)...")
    with open(f"{PROMPT_DIR}/html_index_prompt.txt", "r", encoding="utf-8") as f:
        base_prompt = f.read()
    full_prompt = f"项目规划：\n{plan}\n\n请根据以上规划生成首页：\n{base_prompt}"
    raw_response = call_llm(full_prompt)
    html_index = extract_html_from_llm_response(raw_response)  # ← 清洗
    save_file("outputs/index.html", html_index)

    # --- 列表页 ---
    print(" 📄 正在生成列表页 (list.html)...")
    with open(f"{PROMPT_DIR}/html_list_prompt.txt", "r", encoding="utf-8") as f:
        base_prompt = f.read()
    full_prompt = f"项目规划：\n{plan}\n\n请根据以上规划生成列表页：\n{base_prompt}"
    raw_response = call_llm(full_prompt)
    html_list = extract_html_from_llm_response(raw_response)   # ← 清洗
    save_file("outputs/list.html", html_list)

    # --- 详情页 ---
    print(" 🔍 正在生成详情页 (detail.html)...")
    with open(f"{PROMPT_DIR}/html_detail_prompt.txt", "r", encoding="utf-8") as f:
        base_prompt = f.read()
    full_prompt = f"项目规划：\n{plan}\n\n请根据以上规划生成详情页：\n{base_prompt}"
    raw_response = call_llm(full_prompt)
    html_detail = extract_html_from_llm_response(raw_response) # ← 清洗
    save_file("outputs/detail.html", html_detail)

    print(" ✅ 所有 HTML 页面生成完成！")