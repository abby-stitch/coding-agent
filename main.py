# main.py
import os
import shutil
from pathlib import Path
from config import CURRENT_TEST_CASE

def clear_outputs():
    output_dir = Path("outputs")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

def format_project_name(test_case_name: str) -> str:
    parts = test_case_name.split("_")
    abbreviations = {"cs", "ai", "cv", "lg", "th", "daily", "trending", "repo"}
    formatted = []
    for part in parts:
        if part in abbreviations:
            formatted.append(part.upper())
        else:
            formatted.append(part.capitalize())
    return " ".join(formatted)

def main():
    project_title = format_project_name(CURRENT_TEST_CASE)
    print("=" * 60)
    print(f"🎯 启动 Multi-Agent 系统：{project_title}")
    print("=" * 60)
    clear_outputs()
    
    # Step 1: Planning Agent
    print("\n[1/4] 🧠 运行 Planning Agent...")
    from plan_agent import run_planning_agent
    run_planning_agent()
    
    # Step 2: Data Agent（关键改动：替代原来的 data_fetcher）
    print("\n[2/4] 🕷️ 运行 Data Agent（生成并执行爬虫，获取真实数据）...")
    from data_agent import generate_paper_data
    generate_paper_data()
    
    # Step 3: HTML Agent
    print("\n[3/4] 🌐 运行 HTML Agent（生成全部页面）...")
    from html_agent import generate_all_html_pages
    generate_all_html_pages()
    
    # Step 4: Evaluation Agent
    print("\n[4/4] 👨‍💻 运行 Evaluation Agent（自动评审）...")
    from evaluation_agent import run_evaluation_agent
    run_evaluation_agent()
    
    print("\n" + "=" * 60)
    print("🎉 所有 Agent 执行完毕！")
    print("📁 输出目录: outputs/")
    print("\n💡 测试方法:")
    print("   cd outputs")
    print("   python -m http.server 8000")
    print("   访问 http://localhost:8000")
    print("=" * 60)

if __name__ == "__main__":
    main()