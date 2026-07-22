import json
from datetime import datetime, date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROGRESS_FILE = BASE_DIR / "progress.json"


def _load() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"interviews": [], "resources": [], "queries": []}


def _save(data: dict):
    PROGRESS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    from git_sync import auto_commit
    auto_commit(["progress.json"])


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

    reading_notes = data.get("reading_notes", {})
    files_with_notes = len(reading_notes)
    total_notes = sum(len(notes) for notes in reading_notes.values())
    for notes in reading_notes.values():
        for n in notes:
            study_days.add(n["date"][:10])

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
        "files_read": files_with_notes,
        "total_notes": total_notes,
    }


def load_todos() -> list:
    data = _load()
    return data.get("todos", [])


def save_todo(title: str, priority: str = "medium"):
    data = _load()
    if "todos" not in data:
        data["todos"] = []
    data["todos"].append({
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "title": title,
        "priority": priority,
        "done": False,
        "created": datetime.now().isoformat(),
    })
    _save(data)


def toggle_todo(todo_id: str):
    data = _load()
    for t in data.get("todos", []):
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            break
    _save(data)


def delete_todo(todo_id: str):
    data = _load()
    data["todos"] = [t for t in data.get("todos", []) if t["id"] != todo_id]
    _save(data)


def load_meeting_rooms() -> list:
    data = _load()
    return data.get("meeting_rooms", [])


def save_meeting_room(name: str, url: str):
    data = _load()
    if "meeting_rooms" not in data:
        data["meeting_rooms"] = []
    data["meeting_rooms"].append({
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "name": name,
        "url": url,
    })
    _save(data)


def delete_meeting_room(room_id: str):
    data = _load()
    data["meeting_rooms"] = [r for r in data.get("meeting_rooms", []) if r["id"] != room_id]
    _save(data)


def save_reading_note(file_key: str, content: str):
    data = _load()
    if "reading_notes" not in data:
        data["reading_notes"] = {}
    if file_key not in data["reading_notes"]:
        data["reading_notes"][file_key] = []
    data["reading_notes"][file_key].append({
        "date": datetime.now().isoformat(),
        "content": content,
    })
    _save(data)


def load_reading_notes(file_key: str) -> list:
    data = _load()
    return data.get("reading_notes", {}).get(file_key, [])


REVIEW_INTERVALS = [1, 3, 7, 14, 30, 60]


def add_review_card(front: str, back: str, source: str, source_ref: str = ""):
    data = _load()
    if "review_cards" not in data:
        data["review_cards"] = []
    data["review_cards"].append({
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "front": front,
        "back": back,
        "source": source,
        "source_ref": source_ref,
        "created": datetime.now().isoformat(),
        "next_review": date.today().isoformat(),
        "level": 0,
        "ease_factor": 1.0,
        "reviews": 0,
        "last_review": None,
    })
    _save(data)


def get_due_cards(target_date: str = None) -> list:
    if target_date is None:
        target_date = date.today().isoformat()
    data = _load()
    cards = data.get("review_cards", [])
    return [c for c in cards if c["next_review"] <= target_date]


def review_card(card_id: str, rating: str):
    data = _load()
    for card in data.get("review_cards", []):
        if card["id"] == card_id:
            card["reviews"] += 1
            card["last_review"] = date.today().isoformat()

            if rating == "forgot":
                card["level"] = 0
                card["ease_factor"] = max(0.5, card["ease_factor"] - 0.2)
                card["next_review"] = (date.today() + timedelta(days=1)).isoformat()
            elif rating == "fuzzy":
                interval = REVIEW_INTERVALS[min(card["level"], len(REVIEW_INTERVALS) - 1)]
                card["next_review"] = (date.today() + timedelta(days=interval)).isoformat()
            else:  # remembered
                card["level"] = min(card["level"] + 1, len(REVIEW_INTERVALS) - 1)
                card["ease_factor"] = min(2.5, card["ease_factor"] + 0.1)
                interval = REVIEW_INTERVALS[card["level"]]
                days = max(1, int(interval * card["ease_factor"]))
                card["next_review"] = (date.today() + timedelta(days=days)).isoformat()
            break
    _save(data)


def get_review_stats() -> dict:
    data = _load()
    cards = data.get("review_cards", [])
    today = date.today().isoformat()
    due = sum(1 for c in cards if c["next_review"] <= today)
    mastered = sum(1 for c in cards if c["level"] >= 4)
    return {
        "total_cards": len(cards),
        "due_today": due,
        "mastered": mastered,
    }


def delete_review_card(card_id: str):
    data = _load()
    data["review_cards"] = [c for c in data.get("review_cards", []) if c["id"] != card_id]
    _save(data)


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
