# agents/evaluation_agent.py
import os
from llm import call_llm, save_file, read_project_plan
from config import CURRENT_TEST_CASE

def load_prompt(template_path: str, **kwargs) -> str:
    """加载 prompt 模板并填充变量"""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(**kwargs)

def load_file_content(filepath, max_lines=200):
    if not os.path.exists(filepath):
        return f"[文件不存在: {filepath}]"
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if len(lines) > max_lines:
            return "".join(lines[:max_lines]) + f"\n...（共 {len(lines)} 行，已截断）"
        return "".join(lines)

def run_evaluation_agent():
    print("\n[4/4] 👨‍💻 运行 Evaluation Agent（LLM 评审）...")

    # 路径配置
    PROMPT_DIR = f"test_cases/{CURRENT_TEST_CASE}"
    OUTPUTS_DIR = "outputs"

    # 读取统一数据文件（关键！）
    data_json = load_file_content(f"{OUTPUTS_DIR}/data.json")
    
    # 读取其他文件
    project_plan = read_project_plan()
    index_html = load_file_content(f"{OUTPUTS_DIR}/index.html")
    list_html = load_file_content(f"{OUTPUTS_DIR}/list.html")
    detail_html = load_file_content(f"{OUTPUTS_DIR}/detail.html")

    # 加载 evaluation prompt 模板
    eval_prompt_template = f"{PROMPT_DIR}/evaluation_prompt.txt"
    if not os.path.exists(eval_prompt_template):
        raise FileNotFoundError(f"缺失 evaluation prompt: {eval_prompt_template}")

    # 统一传递 data_json 参数
    full_prompt = load_prompt(
        eval_prompt_template,
        project_plan=project_plan,
        data_json=data_json,  # ✅ 统一参数名
        index_html=index_html,
        list_html=list_html,
        detail_html=detail_html
    )

    # 调用 LLM
    report = call_llm(full_prompt)
    if report:
        save_file(f"{OUTPUTS_DIR}/evaluation_report.txt", report)
        print("\n✅ 评估完成！报告已保存至 outputs/evaluation_report.txt")
    else:
        print("❌ Evaluation Agent 调用失败")