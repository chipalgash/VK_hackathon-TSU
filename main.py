import os
import argparse
import logging
import yaml

from io_utils import (
    extract_text_from_txt,
    extract_text_from_json,
    extract_text_from_pdf,
    extract_text_from_docx
)
from categories import check_categories
from evaluator import ResumeEvaluator

# --- Конфигурируем логер ---
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO
)
log = logging.getLogger(__name__)


def load_config(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def select_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        return extract_text_from_txt(path)
    if ext == '.json':
        return extract_text_from_json(path)
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    if ext == '.docx':
        return extract_text_from_docx(path)
    raise ValueError(f"Неподдерживаемый формат: {ext}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Путь к резюме (.txt/.json/.pdf/.docx)')
    parser.add_argument('-c', '--config', default='config.yaml', help='Путь к config.yaml')
    parser.add_argument('-o', '--output', default=None, help='Сохранить JSON-отчёт в файл')
    args = parser.parse_args()

    cfg = load_config(args.config)
    skill_cats = cfg['skill_categories']
    keywords = cfg['keywords']
    weights = cfg['weights']

    text = select_text(args.file)
    log.info("Извлечён текст резюме (длина %d знаков)", len(text))

    cat_match, found = check_categories(text, skill_cats)
    log.info("Найдено категорий навыков: %s", [k for k,v in cat_match.items() if v])

    all_skills = {s for vals in skill_cats.values() for s in vals}
    evaluator = ResumeEvaluator(keywords, all_skills, weights)
    report = evaluator.evaluate(text)

    print(f"Score: {report['score']}/100")
    print("Keywords found:", report['keywords']['found'])
    print("Keywords missing:", report['keywords']['missing'])
    print("Skills found:", report['skills']['found'])
    print("Spelling errors:", len(report['errors']['spelling']))
    print("Grammar errors:", len(report['errors']['grammar']))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            import json; json.dump(report, f, ensure_ascii=False, indent=2)
        log.info("Отчёт сохранён в %s", args.output)

if __name__ == '__main__':
    main()
