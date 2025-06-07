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

        self.filter = BuzzWordsFilter(keywords, all_skills)
        self.checker = RussianSpellGrammarChecker()
        self.weights = weights

    def evaluate(self, text: str) -> Dict[str, Any]:
        kw_report = self.filter.check(text)
        error_report = self.checker.analyze(text)

        total_kw = len(self.filter.keywords)
        score_kw = len(kw_report['found_keywords']) / total_kw if total_kw else 1.0

        total_sk = len(self.filter.all_skills)
        score_sk = len(kw_report['found_skills']) / total_sk if total_sk else 1.0

        errs = len(error_report['spelling']) + len(error_report['grammar'])
        wc = max(1, len(text.split()))
        score_err = max(0.0, 1 - errs / (0.05 * wc))

        w = self.weights
        score = w['kw']*score_kw + w['skills']*score_sk + w['errors']*score_err
        return {
            'score': round(score*100, 2),
            'keywords': kw_report,
            'errors': error_report
        }
