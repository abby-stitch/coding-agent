# plan_agent.py
from llm import call_llm, save_file
import os
from config import CURRENT_TEST_CASE

PROMPT_DIR = f"test_cases/{CURRENT_TEST_CASE}"

def run_planning_agent():
    # 读取你验证过的具体 prompt（无占位符）
    with open(f"{PROMPT_DIR}/plan_prompt.txt", "r", encoding="utf-8") as f:
        planning_prompt = f.read()

    OUTPUT_DIR = "outputs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("AI 正在拆解开发任务...")
    plan_result = call_llm(planning_prompt)
    if plan_result:
        print("=" * 50)
        print("规划结果（AI 帮你拆的任务）：")
        print(plan_result)
        save_file(f"{OUTPUT_DIR}/project_plan.txt", plan_result)
        print("=" * 50)
        print("规划结果已保存到 project_plan.txt 文件")
        return plan_result
    else:
        print("任务拆解失败，重新运行这个文件试试～")
        return None

if __name__ == "__main__":
    run_planning_agent()