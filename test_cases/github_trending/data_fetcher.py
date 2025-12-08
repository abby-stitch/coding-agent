# github_fetcher.py —— GitHub Trending 数据抓取器（Data Agent）
import json
from datetime import datetime
from pathlib import Path
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# 配置：抓取 Python 项目的今日 trending
LANGUAGE = "python"
TIME_WINDOW = "daily"  # or "weekly"
MAX_RESULTS = 10

def fetch_github_trending():
    print(f"  → 获取 GitHub {LANGUAGE} 今日 trending 项目...")
    base_url = "https://github.com/trending"
    if LANGUAGE:
        url = f"{base_url}/{LANGUAGE}?since={TIME_WINDOW}"
    else:
        url = f"{urljoin(base_url, '')}?since={TIME_WINDOW}"

    # 设置 User-Agent 避免被拒
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; ArxivAgent/1.0; +https://github.com/yourname)"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
        projects = parse_github_trending(html)
        print(f"    ✅ 找到 {len(projects)} 个项目")
        return projects[:MAX_RESULTS]
    except Exception as e:
        print(f"    ⚠️ 失败: {e}")
        return []

def parse_github_trending(html):
    soup = BeautifulSoup(html, "html.parser")
    projects = []

    for article in soup.select("article.Box-row"):
        # 项目名（带 owner）
        name_elem = article.select_one("h2 a")
        if not name_elem:
            continue
        full_name = name_elem.get("href").strip("/")
        owner, repo = full_name.split("/", 1)

        # 描述
        desc_elem = article.select_one("p.col-9")
        description = desc_elem.get_text(strip=True) if desc_elem else ""

        # 语言
        lang_elem = article.select_one("span[itemprop='programmingLanguage']")
        language = lang_elem.get_text(strip=True) if lang_elem else LANGUAGE or "Unknown"

        # 星标数 & 增长
        stars = ""
        forks = ""
        for span in article.select("span.d-inline-block.float-sm-right"):
            text = span.get_text(strip=True)
            if "stars" in text:
                stars = text.replace("stars today", "").replace("star today", "").strip()
            elif "forks" in text:
                forks = text

        # 项目链接
        project_url = f"https://github.com/{full_name}"

        projects.append({
            "id": full_name,  # e.g., "microsoft/vscode"
            "owner": owner,
            "repo": repo,
            "description": description,
            "language": language,
            "stars_today": stars,
            "forks": forks,
            "url": project_url,
            "fetch_date": datetime.utcnow().strftime('%Y-%m-%d')
        })

    return projects

def run_data_agent():
    """
    Data Agent 主入口：抓取 GitHub Trending 项目，输出为 outputs/data.json。
    不使用 LLM，确保数据真实性。
    """
    print("  → 开始从 GitHub 抓取 trending 项目...")
    projects = fetch_github_trending()

    if not projects:
        print("    ⚠️ 未获取到任何项目，生成示例数据")
        projects = [{
            "id": "example/hello-world",
            "owner": "example",
            "repo": "hello-world",
            "description": "A sample project for testing",
            "language": "Python",
            "stars_today": "123",
            "forks": "45",
            "url": "https://github.com/example/hello-world",
            "fetch_date": datetime.utcnow().strftime('%Y-%m-%d')
        }]

    # ✅ 路径：回到项目根目录（两级 parent）
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "data.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

    print(f"  🎉 共保存 {len(projects)} 个项目到 {output_path.resolve()}")

if __name__ == "__main__":
    run_data_agent()