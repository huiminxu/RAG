import json
from datetime import datetime, date
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROGRESS_FILE = BASE_DIR / "progress.json"


def _load() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"interviews": [], "resources": [], "queries": []}


def _save(data: dict):
    PROGRESS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def record_interview(score: int, num_questions: int, categories: list[str], details: str = ""):
    data = _load()
    data["interviews"].append({
        "date": datetime.now().isoformat(),
        "score": score,
        "num_questions": num_questions,
        "categories": categories,
        "details": details,
    })
    _save(data)


def record_resource(title: str, category: str, source_type: str, url: str = ""):
    data = _load()
    data["resources"].append({
        "date": datetime.now().isoformat(),
        "title": title,
        "category": category,
        "source_type": source_type,
        "url": url,
    })
    _save(data)


def record_query(question: str, category: str = "general"):
    data = _load()
    data["queries"].append({
        "date": datetime.now().isoformat(),
        "question": question,
        "category": category,
    })
    _save(data)


def get_stats() -> dict:
    data = _load()
    interviews = data.get("interviews", [])
    resources = data.get("resources", [])
    queries = data.get("queries", [])

    category_count = {}
    for r in resources:
        cat = r.get("category", "未分类")
        category_count[cat] = category_count.get(cat, 0) + 1

    scores = [i["score"] for i in interviews if i.get("score")]
    avg_score = sum(scores) / len(scores) if scores else 0

    today = date.today().isoformat()
    today_count = sum(1 for r in resources if r["date"].startswith(today))
    today_count += sum(1 for i in interviews if i["date"].startswith(today))

    study_days = set()
    for item in interviews + resources:
        study_days.add(item["date"][:10])

    return {
        "total_interviews": len(interviews),
        "total_resources": len(resources),
        "total_queries": len(queries),
        "avg_score": round(avg_score, 1),
        "best_score": max(scores) if scores else 0,
        "recent_scores": scores[-10:],
        "category_distribution": category_count,
        "today_activities": today_count,
        "total_study_days": len(study_days),
        "study_days": sorted(study_days),
    }


def get_progress_summary() -> str:
    data = _load()
    interviews = data.get("interviews", [])
    resources = data.get("resources", [])

    summary = "## 学习数据摘要\n\n"
    summary += f"- 模拟面试次数: {len(interviews)}\n"
    summary += f"- 导入资源数: {len(resources)}\n"

    if interviews:
        scores = [i["score"] for i in interviews if i.get("score")]
        if scores:
            summary += f"- 平均分: {sum(scores)/len(scores):.1f}\n"
            summary += f"- 最高分: {max(scores)}\n"
            summary += f"- 最近5次: {scores[-5:]}\n"

        recent = interviews[-5:]
        summary += "\n### 最近面试记录\n"
        for i in recent:
            summary += f"- {i['date'][:10]} | 分数:{i.get('score','N/A')} | 分类:{','.join(i.get('categories',[]))}\n"

    if resources:
        summary += "\n### 最近学习资源\n"
        for r in resources[-10:]:
            summary += f"- {r['date'][:10]} | [{r['category']}] {r['title']}\n"

    cat_count = {}
    for r in resources:
        cat = r.get("category", "未分类")
        cat_count[cat] = cat_count.get(cat, 0) + 1
    if cat_count:
        summary += "\n### 分类分布\n"
        for cat, count in sorted(cat_count.items(), key=lambda x: -x[1]):
            summary += f"- {cat}: {count} 篇\n"

    return summary
