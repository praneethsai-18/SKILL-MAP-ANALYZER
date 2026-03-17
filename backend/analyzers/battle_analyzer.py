# analyzers/battle_analyzer.py
# Multi-role battle mode — compares resume against 2-3 roles simultaneously

from typing import List, Dict
from analyzers.skill_analyzer import get_analyzer
from extractors.skill_extractor import extract_skills
from extractors.resume_parser import extract_metadata
from data.skill_taxonomy import ROLE_PROFILES


class BattleAnalyzer:
    """
    Analyzes resume against multiple roles simultaneously.
    Determines winner, tiers, and skill overlaps.
    """

    def analyze_battle(
        self,
        resume_text: str,
        resume_skills: List[str],
        roles: List[str],
        metadata: dict = None
    ) -> dict:
        """
        Run battle analysis — compare resume against 2-3 roles.
        Returns full battle result with winner, tiers, overlaps.
        """
        analyzer = get_analyzer()
        metadata = metadata or {}

        # Analyze each role
        role_results = []
        for role_name in roles:
            result = analyzer.analyze_single(
                resume_text, resume_skills, role_name, metadata
            )
            role_results.append(result)

        # Sort by match score (winner first)
        role_results.sort(key=lambda x: x["match_score"], reverse=True)

        # Assign tiers
        scores = [r["match_score"] for r in role_results]
        for i, role in enumerate(role_results):
            role["tier"] = self._assign_tier(role["match_score"], scores, i)

        # Winner
        winner = role_results[0]["role"]

        # Overall resume score — weighted average
        overall = round(
            sum(r["match_score"] for r in role_results) / len(role_results) * 0.7
            + role_results[0]["match_score"] * 0.3
        )

        # Skill overlap matrix
        skill_overlap = self._compute_overlap(role_results, resume_skills)

        # Career gap note
        gap_note = self._detect_career_gaps(resume_text)

        # Overall verdict
        winner_role = role_results[0]
        overall_verdict = self._generate_battle_verdict(role_results, metadata)

        return {
            "candidate_name": metadata.get("candidate_name", "Unknown"),
            "detected_skills": resume_skills,
            "total_experience_years": metadata.get("experience_years", 0),
            "roles": role_results,
            "winner_role": winner,
            "skill_overlap": skill_overlap,
            "overall_resume_score": max(10, min(98, overall)),
            "career_gap_note": gap_note,
            "overall_verdict": overall_verdict
        }

    def _assign_tier(self, score: int, all_scores: list, rank: int) -> str:
        """Assign tier based on score and rank."""
        if rank == 0:
            return "BEST_FIT"
        elif score >= 55:
            return "REACHABLE"
        else:
            return "STRETCH"

    def _compute_overlap(self, role_results: list, resume_skills: list) -> dict:
        """
        Compute skill overlap between roles.
        Identifies skills needed by all roles, 2 roles, winner only.
        """
        if len(role_results) < 2:
            return {
                "all_roles_need": [],
                "two_roles_need": [],
                "winner_only": []
            }

        resume_set = {s.lower() for s in resume_skills}

        # Missing skills per role (skills NOT in resume)
        missing_sets = []
        for role in role_results:
            missing = {s["name"].lower() for s in role["missing_skills"]}
            missing_sets.append(missing)

        # Skills needed by ALL roles (not in resume)
        all_need = missing_sets[0]
        for ms in missing_sets[1:]:
            all_need = all_need & ms
        all_roles_need = sorted(list(all_need))[:6]

        # Skills needed by exactly 2 roles
        two_need = set()
        for i in range(len(missing_sets)):
            for j in range(i + 1, len(missing_sets)):
                shared = missing_sets[i] & missing_sets[j]
                # Exclude ones needed by ALL roles
                two_need.update(shared - all_need)
        two_roles_need = sorted(list(two_need))[:6]

        # Skills unique to winner only
        if len(missing_sets) >= 2:
            winner_missing = missing_sets[0]
            others_missing = set()
            for ms in missing_sets[1:]:
                others_missing.update(ms)
            winner_only = winner_missing - others_missing
        else:
            winner_only = missing_sets[0]

        # Capitalize back
        def cap(skills_set):
            result = []
            for s in sorted(list(skills_set))[:5]:
                # Find canonical name
                for role in role_results:
                    for ms in role["missing_skills"]:
                        if ms["name"].lower() == s:
                            result.append(ms["name"])
                            break
            return result

        return {
            "all_roles_need": cap(set(all_roles_need)),
            "two_roles_need": cap(two_need),
            "winner_only": cap(winner_only)
        }

    def _detect_career_gaps(self, resume_text: str) -> str:
        """Detect employment gaps from resume text."""
        import re
        if not resume_text:
            return "No significant gaps detected"

        years = re.findall(r'\b(20\d{2})\b', resume_text)
        years = sorted(set([int(y) for y in years if 2000 <= int(y) <= 2025]))

        if len(years) >= 2:
            gaps = []
            for i in range(len(years) - 1):
                gap = years[i + 1] - years[i]
                if gap > 1:
                    gaps.append(f"{years[i]}–{years[i+1]} ({gap} year gap)")
            if gaps:
                return f"Potential employment gaps detected: {', '.join(gaps[:2])}"

        return "No significant gaps detected"

    def _generate_battle_verdict(self, role_results: list, metadata: dict) -> str:
        """Generate overall battle verdict."""
        metadata = metadata or {}
        name = metadata.get("candidate_name", "The candidate")
        winner = role_results[0]
        runner_up = role_results[1] if len(role_results) > 1 else None

        verdict = (
            f"{name} is a {self._fit_label(winner['match_score'])} for "
            f"{winner['role']} ({winner['match_score']}% match). "
        )

        if runner_up:
            verdict += (
                f"{runner_up['role']} is {'within reach' if runner_up['match_score'] >= 55 else 'a longer-term goal'} "
                f"at {runner_up['match_score']}% match. "
            )

        if len(winner["missing_skills"]) > 0:
            top_gap = winner["missing_skills"][0]["name"]
            weeks = winner["missing_skills"][0]["weeks_to_learn"]
            verdict += f"Closing the {top_gap} gap (~{weeks} weeks) would significantly boost competitiveness."

        return verdict

    def _fit_label(self, score: int) -> str:
        if score >= 75: return "strong fit"
        if score >= 55: return "moderate fit"
        return "developing fit"


# ── Singleton ──────────────────────────────────────────────────
_battle_analyzer = None

def get_battle_analyzer() -> BattleAnalyzer:
    global _battle_analyzer
    if _battle_analyzer is None:
        _battle_analyzer = BattleAnalyzer()
    return _battle_analyzer
