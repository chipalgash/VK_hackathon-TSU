import re
from typing import Dict, List, Tuple
from functools import lru_cache

SKILL_CATEGORIES: Dict[str, List[str]] = {}

@lru_cache(maxsize=None)
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-zа-я0-9\s\-]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def check_categories(
    resume_text: str,
    skill_categories: Dict[str, List[str]]
) -> Tuple[Dict[str, bool], Dict[str, List[str]]]:
    pre = normalize(resume_text)
    category_matched: Dict[str, bool] = {}
    found: Dict[str, List[str]] = {}

    for cat, keywords in skill_categories.items():
        hits: List[str] = []
        for kw in keywords:
            if normalize(kw) in pre:
                hits.append(kw)
        category_matched[cat] = bool(hits)
        found[cat] = hits
    return category_matched, found
