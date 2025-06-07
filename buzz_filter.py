from typing import List, Set, Dict

class BuzzWordsFilter:
    def __init__(self, keywords: List[str], all_skills: Set[str]) -> None:
        self.keywords = keywords
        self.all_skills = all_skills

    def check(self, text: str) -> Dict[str, List[str]]:
        low = text.lower()
        found_kw = [kw for kw in self.keywords if kw.lower() in low]
        missing_kw = [kw for kw in self.keywords if kw not in found_kw]
        found_skills = [s for s in self.all_skills if s.lower() in low]
        return {'found_keywords': found_kw, 'missing_keywords': missing_kw, 'found_skills': found_skills}
