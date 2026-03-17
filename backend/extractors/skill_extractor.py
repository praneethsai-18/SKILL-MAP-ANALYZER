# extractors/skill_extractor.py
# Core ML skill extraction using spaCy + BERT sentence transformers

import re
import sys
import numpy as np
from typing import List, Dict, Tuple
from data.skill_taxonomy import SKILL_TAXONOMY, get_all_skills, get_skill_category, get_skill_weight

# ── Lazy load models (load once on first use) ──────────────────
_nlp = None
_bert_model = None
_skill_embeddings = None
_all_skills = None

def _load_spacy():
    """Load spaCy model."""
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded")
        except OSError:
            print("⚠️  spaCy model not found. Run: python -m spacy download en_core_web_sm")
            import spacy
            _nlp = spacy.blank("en")
    return _nlp

def _load_bert():
    """Load BERT sentence transformer model."""
    global _bert_model
    if _bert_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            # all-MiniLM-L6-v2 — fast, accurate, small (80MB)
            _bert_model = SentenceTransformer("all-MiniLM-L6-v2")
            print("✅ BERT model loaded (all-MiniLM-L6-v2)")
        except Exception as e:
            print(f"⚠️  BERT model load failed: {e}")
            _bert_model = None
    return _bert_model

def _get_skill_embeddings():
    """Pre-compute BERT embeddings for all skills."""
    global _skill_embeddings, _all_skills
    if _skill_embeddings is None:
        model = _load_bert()
        if model is None:
            return None, None
        _all_skills = get_all_skills()
        print(f"📊 Computing BERT embeddings for {len(_all_skills)} skills...")
        _skill_embeddings = model.encode(_all_skills, convert_to_numpy=True)
        print("✅ Skill embeddings computed")
    return _skill_embeddings, _all_skills


# ── Skill Aliases — normalize alternate spellings ─────────────
SKILL_ALIASES = {
    "js": "JavaScript", "ts": "TypeScript", "py": "Python",
    "golang": "Go", "c plus plus": "C++", "csharp": "C#",
    "nodejs": "Node.js", "node": "Node.js", "expressjs": "Express.js",
    "reactjs": "React", "vuejs": "Vue.js", "angularjs": "Angular",
    "nextjs": "Next.js", "ml": "Machine Learning", "dl": "Deep Learning",
    "nlp": "Natural Language Processing", "cv": "Computer Vision",
    "tf": "TensorFlow", "sklearn": "Scikit-learn", "scikit learn": "Scikit-learn",
    "postgres": "PostgreSQL", "mongo": "MongoDB", "k8s": "Kubernetes",
    "kube": "Kubernetes", "gh actions": "GitHub Actions",
    "ci cd": "CI/CD", "cicd": "CI/CD", "aws lambda": "AWS Lambda",
    "gcp": "Google Cloud Platform", "azure": "Microsoft Azure",
    "rest": "REST API", "restful": "REST API", "spark": "Apache Spark",
    "kafka": "Apache Kafka", "airflow": "Apache Airflow",
    "spacy": "spaCy", "bert": "BERT", "gpt": "GPT",
    "pandas": "Pandas", "numpy": "NumPy", "matplotlib": "Matplotlib"
}


class SkillExtractor:
    """
    Extracts skills from text using 3 methods combined:
    1. Exact match — fast lookup against skill taxonomy
    2. spaCy NLP — entity recognition + noun phrase matching
    3. BERT semantic similarity — catches paraphrases and synonyms
    """

    def __init__(self):
        self.all_skills = get_all_skills()
        self.skill_lookup = {s.lower(): s for s in self.all_skills}
        for alias, canonical in SKILL_ALIASES.items():
            self.skill_lookup[alias.lower()] = canonical

    def extract(self, text: str) -> List[str]:
        """
        Main extraction method — combines all 3 approaches.
        Returns deduplicated list of canonical skill names.
        """
        if not text or len(text.strip()) < 10:
            return []

        found = set()

        # Method 1: Exact + alias matching (fastest)
        found.update(self._exact_match(text))

        # Method 2: spaCy NLP matching
        found.update(self._spacy_match(text))

        # Method 3: BERT semantic similarity (most powerful)
        found.update(self._bert_match(text))

        return sorted(list(found))

    def _exact_match(self, text: str) -> List[str]:
        """Exact keyword matching with word boundaries."""
        found = []
        text_lower = text.lower()

        for skill_lower, canonical in self.skill_lookup.items():
            # Use word boundary matching to avoid partial matches
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower, re.IGNORECASE):
                found.append(canonical)

        # Multi-word phrase matching
        words = text_lower.split()
        for n in [2, 3]:
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i+n])
                if phrase in self.skill_lookup:
                    found.append(self.skill_lookup[phrase])

        return list(set(found))

    def _spacy_match(self, text: str) -> List[str]:
        """Use spaCy NLP for entity and noun phrase extraction."""
        found = []
        try:
            nlp = _load_spacy()
            doc = nlp(text[:10000])  # limit for performance

            # Check noun chunks against skill list
            for chunk in doc.noun_chunks:
                chunk_lower = chunk.text.lower().strip()
                if chunk_lower in self.skill_lookup:
                    found.append(self.skill_lookup[chunk_lower])

            # Check named entities
            for ent in doc.ents:
                ent_lower = ent.text.lower().strip()
                if ent_lower in self.skill_lookup:
                    found.append(self.skill_lookup[ent_lower])

        except Exception as e:
            pass  # Graceful degradation if spaCy fails

        return list(set(found))

    def _bert_match(self, text: str, threshold: float = 0.82) -> List[str]:
        """
        Use BERT sentence embeddings to find semantically similar skills.
        Catches synonyms and paraphrases that exact matching misses.
        """
        found = []
        try:
            model = _load_bert()
            if model is None:
                return found

            skill_embeddings, all_skills = _get_skill_embeddings()
            if skill_embeddings is None:
                return found

            # Extract sentences/phrases from text
            sentences = self._extract_candidate_phrases(text)
            if not sentences:
                return found

            # Encode candidate phrases
            from sentence_transformers import util
            phrase_embeddings = model.encode(sentences, convert_to_numpy=True)

            # Compute cosine similarity against all skill embeddings
            for phrase_emb in phrase_embeddings:
                similarities = np.dot(skill_embeddings, phrase_emb) / (
                    np.linalg.norm(skill_embeddings, axis=1) * np.linalg.norm(phrase_emb) + 1e-9
                )
                best_idx = np.argmax(similarities)
                if similarities[best_idx] >= threshold:
                    found.append(all_skills[best_idx])

        except Exception as e:
            pass  # Graceful degradation

        return list(set(found))

    def _extract_candidate_phrases(self, text: str) -> List[str]:
        """Extract short phrases from text to compare against skills."""
        sentences = re.split(r'[.\n,;|•\-/]', text)
        candidates = []
        for sent in sentences:
            sent = sent.strip()
            if 2 <= len(sent.split()) <= 5 and len(sent) > 3:
                candidates.append(sent)
        return candidates[:200]  # Limit for performance


# ── Singleton extractor ────────────────────────────────────────
_extractor = None

def get_extractor() -> SkillExtractor:
    global _extractor
    if _extractor is None:
        _extractor = SkillExtractor()
    return _extractor

def extract_skills(text: str) -> List[str]:
    """Convenience function — extract skills from text."""
    return get_extractor().extract(text)
