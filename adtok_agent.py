"""AdTok Agent — Pipeline complet 48h."""
import os
import sqlite3
import json
from dotenv import load_dotenv
from rich.console import Console
from modules.sourcing import TikTokSourcer
from modules.scoring import ProductScorer
from modules.creative import CreativeEngine
from modules.site import MiniSiteBuilder
from modules.ads import TikTokAdsManager
from modules.reporting import Reporter

load_dotenv()
console = Console()

class AdTokAgent:
    def __init__(self):
        self.sourcer = TikTokSourcer(os.getenv("TIKTOK_ACCESS_TOKEN", "mock"))
        self.scorer = ProductScorer()
        self.creative = CreativeEngine(os.getenv("OPENAI_API_KEY"))
        self.site = MiniSiteBuilder(os.getenv("LOVABLE_PROJECT_URL"))
        self.ads = TikTokAdsManager(
            os.getenv("TIKTOK_ACCESS_TOKEN", "mock"),
            os.getenv("TIKTOK_ADVERTISER_ID", "mock"),
        )
        self.reporter = Reporter()
        self._init_db()

    def _init_db(self):
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect("data/adtok.db")
        conn.execute("""CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            niche TEXT, product TEXT, site_url TEXT,
            campaign_id TEXT, score REAL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.commit()
        conn.close()

    def run_pipeline(self, niche: str, budget_daily: float = 100):
        console.rule(f"[bold cyan]AdTok Agent — Niche: {niche}")
        
        # H+0 → H+2 : Sourcing & scoring
        console.print("[yellow]→ Sourcing TikTok trends...")
        products = self.sourcer.fetch_trending(niche, limit=50)
        top10 = self.scorer.top_n(products, n=10)
        self.reporter.top10_report(top10)
        
        # H+6 : Sélection top 1 + génération créa
        winner = top10[0]
        console.print(f"\n[green]✔ Produit sélectionné: {winner['product_name']} (score {winner['potential_score']})")
        console.print("[yellow]→ Génération pack créa (6 vidéos, 10 hooks)...")
        creative_pack = self.creative.generate_pack(winner)
        console.print(f"[green]✔ {len(creative_pack['scripts'])} scripts générés, {len(creative_pack['hooks_text'])} hooks")
        
        # H+12 : Mini-site
        console.print("[yellow]→ Build mini-site...")
        site_brief = self.site.build_brief(winner, creative_pack)
        site_url = self.site.publish(site_brief)
        console.print(f"[green]✔ Site publié: {site_url}")
        
        # H+24 : Campagnes Ads
        console.print("[yellow]→ Lancement campagnes TikTok Ads...")
        campaign = self.ads.create_campaign(winner, site_url, daily_budget=budget_daily)
        adgroups = self.ads.create_adgroups(campaign["campaign_id"])
        console.print(f"[green]✔ Campagne {campaign['campaign_id']} active, {len(adgroups)} adgroups")
        
        # Persistance
        conn = sqlite3.connect("data/adtok.db")
        conn.execute(
            "INSERT INTO runs (niche, product, site_url, campaign_id, score) VALUES (?, ?, ?, ?, ?)",
            (niche, winner["product_name"], site_url, campaign["campaign_id"], winner["potential_score"]),
        )
        conn.commit()
        conn.close()
        
        # H+48 : Rapport simulé
        mock_metrics = {"ctr": 1.4, "cpa": 18, "target_cpa": 25, "hook_retention_3s": 0.42, "impressions": 25000}
        actions = self.ads.apply_rules(mock_metrics)
        report = self.reporter.h48_report({
            "campaign_id": campaign["campaign_id"],
            "metrics": mock_metrics,
            "actions": actions,
        })
        console.print("\n[bold magenta]Rapport H+48:")
        console.print_json(data=report)
        
        return {
            "product": winner,
            "creative": creative_pack,
            "site_url": site_url,
            "campaign": campaign,
            "report": report,
        }

if __name__ == "__main__":
    import sys
    niche = sys.argv[1] if len(sys.argv) > 1 else "beauty"
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 100
    agent = AdTokAgent()
    result = agent.run_pipeline(niche, budget)
    with open("data/last_run.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    console.print("\n[bold green]✔ Pipeline terminé. Voir data/last_run.json")
