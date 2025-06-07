from typing import List, Dict, Any
import pyaspeller
import language_tool_python

class RussianSpellGrammarChecker:
    def __init__(self) -> None:
        self.speller = pyaspeller.YandexSpeller()
        self.ltool = language_tool_python.LanguageTool('ru')

    def check_spelling(self, text: str) -> List[Dict[str, Any]]:
        return self.speller.spell_words(text)

    def check_grammar(self, text: str) -> List[Dict[str, Any]]:
        matches = self.ltool.check(text)
        return [
            {
                'message': m.message,
                'replacements': m.replacements,
                'offset': m.offset,
                'length': m.errorLength,
                'context': text[m.offset:m.offset + m.errorLength]
            }
            for m in matches
        ]

    def analyze(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        return {'spelling': self.check_spelling(text), 'grammar': self.check_grammar(text)}
