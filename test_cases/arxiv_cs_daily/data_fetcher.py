# data_fetcher.py —— 真实 arXiv 数据抓取器（Data Agent）
import json
import urllib.request
from datetime import datetime
from xml.etree import ElementTree as ET
from pathlib import Path

CATEGORIES = ["cs.AI", "cs.TH", "cs.CV", "cs.LG"]
MAX_RESULTS = 5  # 每类最多 5 篇

def fetch_arxiv_papers():
    all_papers = []
    for cat in CATEGORIES:
        print(f"  → 获取 {cat} 的最新论文...")
        query = f"cat:{cat}"
        url = f"http://export.arxiv.org/api/query?search_query={query}&max_results={MAX_RESULTS}&sortBy=submittedDate&sortOrder=descending"

        try:
            with urllib.request.urlopen(url) as response:
                xml_data = response.read()
            papers = parse_arxiv_response(xml_data, cat)
            all_papers.extend(papers)
            print(f"    ✅ 找到 {len(papers)} 篇")
        except Exception as e:
            print(f"    ⚠️ 失败: {e}")
    
    return all_papers

def parse_arxiv_response(xml_data, expected_category):
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
        published = entry.find('atom:published', ns).text.split('T')[0]
        arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]

        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        papers.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors,
            "category": expected_category,
            "submit_date": published,
            "pdf_url": pdf_url
        })
    return papers

def run_data_agent():
    """
    Data Agent 主入口：从 arXiv 抓取真实论文数据，输出为 outputs/papers.json。
    不使用 LLM，确保数据真实性。
    """
    print("  → 开始从 arXiv 抓取真实论文数据...")
    papers = fetch_arxiv_papers()

    if not papers:
        print("    ⚠️ 未获取到任何论文，生成少量示例数据用于测试")
        papers = [{
            "id": "2412.99999",
            "title": "Sample Paper for Testing",
            "authors": ["Test Author"],
            "category": "cs.AI",
            "submit_date": datetime.utcnow().strftime('%Y-%m-%d'),
            "pdf_url": "https://arxiv.org/pdf/2412.99999"
        }]

    # ✅ 修正：从脚本位置向上两级到达项目根目录
    script_dir = Path(__file__).resolve().parent      # .../test_cases/arxiv_cs_daily
    project_root = script_dir.parent.parent           # .../test_cases → .../project-root
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "data.json"

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"  🎉 共保存 {len(papers)} 篇论文到 {output_path.resolve()}")

# ✅ 脚本入口：必须顶格！
if __name__ == "__main__":
    run_data_agent()