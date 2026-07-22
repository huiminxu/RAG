"""
Git 自动同步模块 — Streamlit Cloud 数据持久化

在 app 内修改文件后自动 commit + push 到 GitHub，
下次重启时数据不会丢失。

需要 .env 配置 GIT_TOKEN（GitHub Personal Access Token, repo scope）。
本地开发无 GIT_TOKEN 时静默跳过。
"""

import os
import subprocess
import threading
import time
from pathlib import Path

GIT_TOKEN = os.getenv("GIT_TOKEN", "")
REPO_DIR = Path(__file__).parent
REPO_URL = "https://{token}@github.com/huiminxu/RAG.git"

_debounce_timer = None
_pending_files = set()
_lock = threading.Lock()

DEBOUNCE_SECONDS = 5


def auto_commit(files: list[str], message: str = "auto: sync data"):
    """防抖式异步 commit + push。多次调用合并为一次提交。"""
    if not GIT_TOKEN:
        return

    with _lock:
        global _debounce_timer
        for f in files:
            _pending_files.add(f)

        if _debounce_timer is not None:
            _debounce_timer.cancel()

        _debounce_timer = threading.Timer(DEBOUNCE_SECONDS, _flush, args=(message,))
        _debounce_timer.daemon = True
        _debounce_timer.start()


def _flush(message: str):
    """实际执行 git add + commit + push。"""
    global _debounce_timer

    with _lock:
        if not _pending_files:
            return
        files = list(_pending_files)
        _pending_files.clear()
        _debounce_timer = None

    threading.Thread(target=_sync, args=(files, message), daemon=True).start()


def _sync(files: list[str], message: str):
    """后台执行 git 操作。"""
    try:
        remote_url = REPO_URL.format(token=GIT_TOKEN)

        _run_git(["git", "remote", "set-url", "origin", remote_url])
        _run_git(["git", "config", "user.email", "bot@rag-app.local"])
        _run_git(["git", "config", "user.name", "RAG Bot"])

        _run_git(["git", "add"] + files)

        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO_DIR,
            capture_output=True,
        )
        if result.returncode == 0:
            return

        _run_git(["git", "commit", "-m", message])
        _run_git(["git", "push", "origin", "main"])
    except Exception:
        pass


def _run_git(cmd: list[str]):
    """执行 git 命令，静默失败。"""
    subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, timeout=30)
