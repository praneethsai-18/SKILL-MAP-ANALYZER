# analyzers/skill_analyzer.py
# ALL FIXES: #2 zero=0%, #3 zero=full roadmap, #3 verdict for zero match
import re
from typing import List
from data.skill_taxonomy import (SKILL_TAXONOMY, ROLE_PROFILES,
    get_skill_weight, get_skill_category, get_courses_for_skill)

class SkillAnalyzer:
    def analyze_single(self, resume_text, resume_skills, role_name, resume_metadata=None):
        role_profile = self._get_role_profile(role_name)
        required     = role_profile["required"]
        nice_to_have = role_profile.get("nice_to_have", [])
        all_role     = required + nice_to_have
        resume_set   = {s.lower() for s in resume_skills}
        required_set = {s.lower() for s in required}
        ntf_set      = {s.lower() for s in nice_to_have}
        matched          = [s for s in all_role if s.lower() in resume_set]
        missing_required = [s for s in required if s.lower() not in resume_set]
        missing_ntf      = [s for s in nice_to_have if s.lower() not in resume_set]
        bonus            = [s for s in resume_skills if s.lower() not in {x.lower() for x in all_role}]
        match_score  = self._calculate_match_score(resume_set, required_set, ntf_set, role_profile)
        ats_score    = self._calculate_ats_score(resume_text, required, match_score)
        strength     = self._calculate_strength_scores(resume_text, resume_skills, match_score, resume_metadata)
        cat_scores   = self._calculate_category_scores(resume_set, role_profile)

        # FIX #3 — zero match shows full role roadmap
        if match_score == 0:
            src_req = required[:8]
            src_ntf = nice_to_have[:4]
        else:
            src_req = missing_required[:8]
            src_ntf = missing_ntf[:4]

        missing_data = []
        for s in src_req:
            missing_data.append({"name":s,"priority":"Critical","weeks_to_learn":self._estimate_weeks(s),"courses":get_courses_for_skill(s)})
        for s in src_ntf:
            missing_data.append({"name":s,"priority":"Recommended","weeks_to_learn":self._estimate_weeks(s),"courses":get_courses_for_skill(s)})

        roadmap     = self._build_roadmap(missing_data)
        total_weeks = sum(s["weeks_to_learn"] for s in missing_data)
        verdict     = self._generate_verdict(resume_metadata, matched, missing_required, match_score, role_name)

        return {"role":role_name,"match_score":match_score,"ats_score":ats_score,
                "matched_skills":matched,"missing_skills":missing_data,
                "bonus_skills":bonus[:10],"verdict":verdict,
                "strength_scores":strength,"category_scores":cat_scores,
                "roadmap":roadmap,"salary_range":role_profile.get("salary_range","Market dependent"),
                "total_learning_weeks":total_weeks}

    def _get_role_profile(self, role_name):
        if role_name in ROLE_PROFILES: return ROLE_PROFILES[role_name]
        for key in ROLE_PROFILES:
            if role_name.lower() in key.lower() or key.lower() in role_name.lower():
                return ROLE_PROFILES[key]
        return {"required":[],"nice_to_have":[],"category_weights":{"languages":0.20,"backend":0.20,"frontend":0.20,"cloud_devops":0.15,"databases":0.15,"soft_skills":0.10},"salary_range":"Market dependent"}

    def _calculate_match_score(self, resume_set, required_set, ntf_set, role_profile):
        # FIX #2 — zero match = 0%
        if not required_set: return 0
        req_matched = len(resume_set & required_set)
        if req_matched == 0:
            ntf_matched = len(resume_set & ntf_set)
            if ntf_matched == 0: return 0
            return max(1, round((ntf_matched / max(len(ntf_set),1)) * 12))
        req_score   = (req_matched / max(len(required_set),1)) * 80
        ntf_matched = len(resume_set & ntf_set)
        ntf_score   = (ntf_matched / max(len(ntf_set),1)) * 15 if ntf_set else 0
        density     = min(5, len(resume_set) * 0.2)
        return max(0, min(98, round(req_score + ntf_score + density)))

    def _calculate_ats_score(self, resume_text, required_skills, match_score):
        if not resume_text or not required_skills: return max(0, round(match_score*0.8))
        text_lower = resume_text.lower()
        kw_hits    = sum(1 for s in required_skills if s.lower() in text_lower)
        if kw_hits == 0: return max(0, min(10, round(match_score*0.4)))
        base = round((kw_hits/max(len(required_skills),1))*60)
        base += sum(1 for s in ["experience","education","skills","projects","summary","work history"] if s in text_lower)*3
        if re.search(r'\b(20\d{2})\b', resume_text): base += 4
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text): base += 3
        if "\n" in resume_text: base += 3
        wc = len(resume_text.split())
        if wc < 100: base -= 20
        elif wc < 200: base -= 8
        return max(0, min(98, round(base*0.65 + match_score*0.35)))

    def _calculate_strength_scores(self, resume_text, resume_skills, match_score, metadata=None):
        metadata  = metadata or {}
        wc        = len(resume_text.split()) if resume_text else 0
        exp       = metadata.get("experience_years", 0)
        exp_score = min(95, 40 + exp*8)
        density   = len(resume_skills)/max(wc,1)*1000
        dens_sc   = min(95, round(30 + density*50))
        actions   = ["led","built","designed","architected","managed","scaled","improved",
                     "reduced","increased","delivered","developed","deployed","optimized","automated","created"]
        tl        = resume_text.lower() if resume_text else ""
        ac        = sum(1 for w in actions if w in tl)
        kw_sc     = min(95, round(match_score*0.6 + ac*3))
        ats_c     = self._calculate_ats_score(resume_text, [], match_score)
        floor     = 0 if match_score == 0 else 10
        return {"experience":max(floor,exp_score),"skill_density":max(floor,dens_sc),
                "keyword_relevance":max(floor,kw_sc),"ats_compatibility":max(floor,ats_c)}

    def _calculate_category_scores(self, resume_set, role_profile):
        weights = role_profile.get("category_weights", {})
        scores  = {}
        for cn, cd in SKILL_TAXONOMY.items():
            cs    = {s.lower() for s in cd["skills"]}
            raw   = (len(resume_set & cs)/max(len(cs),1))*100
            w     = weights.get(cn, 0.1)
            label = cn.replace("_","/").title()
            scores[label] = max(0, min(99, round(raw*(1+w))))
        return dict(sorted(scores.items(), key=lambda x:x[1], reverse=True)[:6])

    def _estimate_weeks(self, skill_name):
        complex_skills = {"Machine Learning":8,"Deep Learning":10,"TensorFlow":6,"PyTorch":6,
            "Apache Spark":6,"Kubernetes":5,"AWS":8,"System Design":8,"Microservices":6,
            "Apache Kafka":4,"Apache Airflow":4,"dbt":3,"Snowflake":3,"React":5,
            "TypeScript":3,"Docker":3,"PostgreSQL":4,"GraphQL":3}
        return complex_skills.get(skill_name, 2)

    def _build_roadmap(self, missing_skills):
        if not missing_skills: return []
        roadmap = []; week = 1
        for sd in (sorted([s for s in missing_skills if s["priority"]=="Critical"], key=lambda x:x["weeks_to_learn"]) +
                   sorted([s for s in missing_skills if s["priority"]!="Critical"], key=lambda x:x["weeks_to_learn"]))[:8]:
            w   = sd["weeks_to_learn"]
            end = week + w - 1
            lbl = f"Week {week}" if week==end else f"Week {week}–{end}"
            courses  = sd.get("courses",[])
            resource = courses[0]["title"] if courses else f"{sd['name']} — Official Documentation"
            roadmap.append({"week":lbl,"skill":sd["name"],"hours_per_week":6 if sd["priority"]=="Critical" else 4,"resource":resource})
            week = end + 1
        return roadmap

    def _generate_verdict(self, metadata, matched, missing, match_score, role_name):
        metadata = metadata or {}
        exp      = metadata.get("experience_years", 0)
        exp_note = f" with {exp} years of experience" if exp > 0 else ""
        # FIX #3 — zero match verdict
        if match_score == 0:
            top = ", ".join(missing[:3]) if missing else "the core skills"
            return (f"This resume has no direct skill overlap with {role_name}{exp_note}. "
                    f"To transition into this role, start by learning {top}. "
                    f"The roadmap below shows the fastest path from your current background to {role_name}.")
        fit = "strong fit" if match_score>=75 else ("moderate fit" if match_score>=55 else "developing fit")
        ms  = ", ".join(matched[:3]) if matched else "some relevant skills"
        gs  = " and ".join(missing[:2]) if missing else "a few areas"
        return (f"This resume shows a {fit} for {role_name}{exp_note}. "
                f"Key strengths include {ms}, which directly align with role requirements. "
                f"The primary gaps are {gs} — bridging these would significantly improve competitiveness.")

_analyzer = None
def get_analyzer():
    global _analyzer
    if _analyzer is None: _analyzer = SkillAnalyzer()
    return _analyzer
