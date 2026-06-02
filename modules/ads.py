"""Crée et pilote les campagnes TikTok Ads."""
import requests
from typing import Dict, List

class TikTokAdsManager:
    def __init__(self, token: str, advertiser_id: str):
        self.token = token
        self.advertiser_id = advertiser_id
        self.base = "https://business-api.tiktok.com/open_api/v1.3"

    def create_campaign(self, product: Dict, site_url: str, daily_budget: float = 100) -> Dict:
        payload = {
            "advertiser_id": self.advertiser_id,
            "campaign_name": f"ADTOK_{product['product_name']}_TEST",
            "objective_type": "CONVERSIONS",
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": daily_budget,
        }
        # En prod: requests.post(f"{self.base}/campaign/create/", json=payload, headers=...)
        return {"campaign_id": f"camp_{product['product_name'][:8]}", "status": "ACTIVE", "site_url": site_url}

    def create_adgroups(self, campaign_id: str) -> List[Dict]:
        audiences = [
            {"name": "Broad_FR_18_45", "type": "broad", "age": "18-45", "geo": "FR"},
            {"name": "Lookalike_1pct", "type": "lookalike", "seed": "purchasers_90d"},
            {"name": "Interest_Beauty", "type": "interest", "interests": ["beauty", "skincare"]},
        ]
        return [{"adgroup_id": f"ag_{i}", **a, "campaign_id": campaign_id} for i, a in enumerate(audiences)]

    def apply_rules(self, metrics: Dict) -> List[str]:
        actions = []
        if metrics["ctr"] < 0.8 and metrics["impressions"] > 1000:
            actions.append("KILL creative — CTR too low")
        if metrics["cpa"] < metrics["target_cpa"] * 0.8:
            actions.append("SCALE +25% — CPA below target")
        if metrics["hook_retention_3s"] < 0.35:
            actions.append("ITERATE hook — retention weak")
        return actions
