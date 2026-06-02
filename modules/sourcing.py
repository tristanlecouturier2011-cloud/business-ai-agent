"""Scrape les tendances TikTok et extrait des produits candidats."""
import requests
from datetime import datetime
from typing import List, Dict

class TikTokSourcer:
    def __init__(self, token: str):
        self.token = token
        self.base = "https://open.tiktokapis.com/v2"

    def fetch_trending(self, niche: str, limit: int = 50) -> List[Dict]:
        # En prod: appel à TikTok Creative Center API ou scraping headless
        # Ici, mock structuré pour démo
        return [
            {
                "product_name": f"Produit {niche} #{i}",
                "hashtag": f"#{niche}tok",
                "views": 1_200_000 + i * 50_000,
                "likes": 80_000 - i * 1000,
                "shares": 5_000 - i * 50,
                "ctr_estimate": round(1.5 + (i % 5) * 0.3, 2),
                "sound_id": f"snd_{i}",
                "competitor_ads_active": i % 3,
                "fetched_at": datetime.utcnow().isoformat(),
            }
            for i in range(limit)
        ]

    def competitor_radar(self, keyword: str) -> List[Dict]:
        # Detection des comptes ads actifs (TikTok Ads Library)
        return [{"advertiser": f"brand_{i}", "active_creatives": 3 + i} for i in range(5)]
