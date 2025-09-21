from typing import Dict, List, Tuple


def score_career_paths(
    user_skill_levels: Dict[int, int],
    career_to_required_skills: Dict[int, List[int]],
) -> List[Tuple[int, float]]:
    """
    Returns list of (career_path_id, score_percent) sorted desc.
    Simple overlap-weighted scoring: sum(user_level for required skills) / (len(required)*100) * 100.
    """
    scores: List[Tuple[int, float]] = []
    for career_id, required_ids in career_to_required_skills.items():
        if not required_ids:
            scores.append((career_id, 0.0))
            continue
        total_possible = len(required_ids) * 100
        achieved = 0
        for sid in required_ids:
            achieved += max(0, min(100, user_skill_levels.get(sid, 0)))
        score = round((achieved / total_possible) * 100.0, 2)
        scores.append((career_id, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


