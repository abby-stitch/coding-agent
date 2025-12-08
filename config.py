# config.py
# 配置当前运行的 test case

# CURRENT_TEST_CASE = "arxiv_cs_daily"
CURRENT_TEST_CASE = "github_trending"

# （可选）供其他模块使用，比如 plan_agent 读 prompt
PROMPT_DIR = f"test_cases/{CURRENT_TEST_CASE}"