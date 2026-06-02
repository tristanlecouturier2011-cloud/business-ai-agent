"""Calcule un score de potentiel de conversion 0-100."""
from typing import Dict

class ProductScorer:
    WEIGHTS = {
        "social_proof": 0.30,
        "engagement_rate": 0.25,
        "ctr": 0.20,
        "competition": 0.15,
        "margin": 0.10,
    }

    def score(self, product: Dict, est_margin: float = 0.6) -> Dict:
        engagement = (product["likes"] + product["shares"]) / max(product["views"], 1)
        social_proof = min(product["views"] / 5_000_000, 1.0)
        ctr_norm = min(product["ctr_estimate"] / 3.0, 1.0)
        competition_penalty = 1 - min(product["competitor_ads_active"] / 10, 1.0)
        
        score = (
            social_proof * self.WEIGHTS["social_proof"]
            + engagement * self.WEIGHTS["engagement_rate"] * 10
            + ctr_norm * self.WEIGHTS["ctr"]
            + competition_penalty * self.WEIGHTS["competition"]
            + est_margin * self.WEIGHTS["margin"]
        ) * 100
        
        return {
            **product,
            "potential_score": round(min(score, 100), 1),
            "estimated_margin": est_margin,
        }

    def top_n(self, products: list, n: int = 10) -> list:
        scored = [self.score(p) for p in products]
        return sorted(scored, key=lambda x: x["potential_score"], reverse=True)[:n]
