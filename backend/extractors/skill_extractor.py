# extractors/skill_extractor.py
# Skill extraction using exact matching + aliases only
# (spaCy and BERT disabled for Render free tier compatibility)

import re
from typing import List
from data.skill_taxonomy import SKILL_TAXONOMY, get_all_skills

# ── Skill Aliases ──────────────────────────────────────────────
SKILL_ALIASES = {
    "js": "JavaScript", "ts": "TypeScript", "py": "Python",
    "golang": "Go", "nodejs": "Node.js", "node": "Node.js",
    "expressjs": "Express.js", "reactjs": "React", "vuejs": "Vue.js",
    "angularjs": "Angular", "nextjs": "Next.js",
    "ml": "Machine Learning", "dl": "Deep Learning",
    "nlp": "Natural Language Processing", "cv": "Computer Vision",
    "tf": "TensorFlow", "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn", "postgres": "PostgreSQL",
    "mongo": "MongoDB", "k8s": "Kubernetes", "kube": "Kubernetes",
    "gh actions": "GitHub Actions", "ci cd": "CI/CD", "cicd": "CI/CD",
    "gcp": "Google Cloud Platform", "azure": "Microsoft Azure",
    "rest": "REST API", "restful": "REST API",
    "spark": "Apache Spark", "kafka": "Apache Kafka",
    "airflow": "Apache Airflow", "bert": "BERT", "gpt": "GPT",
    "pandas": "Pandas", "numpy": "NumPy",
}

class SkillExtractor:
    def __init__(self):
        self.all_skills = get_all_skills()
        self.skill_lookup = {s.lower(): s for s in self.all_skills}
        for alias, canonical in SKILL_ALIASES.items():
            self.skill_lookup[alias.lower()] = canonical

    def extract(self, text: str) -> List[str]:
        if not text or len(text.strip()) < 10:
            return []
        found = set()
        found.update(self._exact_match(text))
        return sorted(list(found))

    def _exact_match(self, text: str) -> List[str]:
        found = []
        text_lower = text.lower()
        for skill_lower, canonical in self.skill_lookup.items():
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower, re.IGNORECASE):
                found.append(canonical)
        words = text_lower.split()
        for n in [2, 3]:
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i+n])
                if phrase in self.skill_lookup:
                    found.append(self.skill_lookup[phrase])
        return list(set(found))

_extractor = None

def get_extractor() -> SkillExtractor:
    global _extractor
    if _extractor is None:
        _extractor = SkillExtractor()
    return _extractor

def extract_skills(text: str) -> List[str]:
    return get_extractor().extract(text)
