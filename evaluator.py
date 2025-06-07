# evaluator.py

from typing import List, Dict, Any, Set

class ResumeEvaluator:
    def __init__(
        self,
        keywords: List[str],
        all_skills: Set[str],
        weights: Dict[str, float]
    ) -> None:
        from buzz_filter import BuzzWordsFilter
        from spell_grammar import RussianSpellGrammarChecker

        # Ожидаем, что BuzzWordsFilter сохраняет keywords и all_skills
        self.filter = BuzzWordsFilter(keywords, all_skills)
        self.checker = RussianSpellGrammarChecker()
        self.weights = weights

    def evaluate(self, text: str) -> Dict[str, Any]:
        # --- 1) Ключевые слова и навыки ---
        kw_report = self.filter.check(text)
        found_kw = kw_report.get('found_keywords', [])
        missing_kw = kw_report.get('missing_keywords', [])
        found_sk = kw_report.get('found_skills', [])

        total_kw = len(getattr(self.filter, 'keywords', found_kw + missing_kw))
        total_sk = len(getattr(self.filter, 'all_skills', found_sk))

        score_kw = len(found_kw) / total_kw if total_kw > 0 else 1.0
        score_sk = len(found_sk) / total_sk if total_sk > 0 else 1.0

        # --- 2) Орфо/грамматика ---
        # приводим генераторы к спискам
        spelling_errors = list(self.checker.check_spelling(text))
        grammar_errors = list(self.checker.check_grammar(text))

        num_errors = len(spelling_errors) + len(grammar_errors)
        word_count = max(1, len(text.split()))
        score_err = max(0.0, 1 - num_errors / (0.05 * word_count))

        # --- 3) Итоговый score ---
        w = self.weights
        combined = (
            w.get('kw', 0)      * score_kw +
            w.get('skills', 0)  * score_sk +
            w.get('errors', 0)  * score_err
        )

        return {
            'score': round(combined * 100, 2),
            'keywords': {
                'found': found_kw,
                'missing': missing_kw
            },
            'skills': {
                'found': found_sk,
                'total': total_sk
            },
            'errors': {
                'spelling': spelling_errors,
                'grammar': grammar_errors
            },
            'metrics': {
                'kw_ratio': score_kw,
                'skills_ratio': score_sk,
                'error_ratio': score_err
            }
        }
