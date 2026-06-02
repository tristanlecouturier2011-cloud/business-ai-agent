"""Rapports H+48 et dashboards KPI."""
from datetime import datetime
from rich.console import Console
from rich.table import Table

class Reporter:
    def __init__(self):
        self.console = Console()

    def top10_report(self, products: list) -> str:
        table = Table(title="Top 10 Produits — AdTok Agent")
        table.add_column("Rang", style="cyan")
        table.add_column("Produit")
        table.add_column("Score", justify="right")
        table.add_column("Vues", justify="right")
        table.add_column("CTR est.", justify="right")
        table.add_column("Marge", justify="right")
        
        for i, p in enumerate(products, 1):
            table.add_row(
                str(i), p["product_name"], f"{p['potential_score']}",
                f"{p['views']:,}", f"{p['ctr_estimate']}%", f"{p['estimated_margin']*100:.0f}%"
            )
        
        self.console.print(table)
        return "report_generated"

    def h48_report(self, campaign_data: dict) -> dict:
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "campaign_id": campaign_data.get("campaign_id"),
            "kpis": campaign_data.get("metrics", {}),
            "recommendations": campaign_data.get("actions", []),
            "next_cycle": "Kill 2 losers, scale 1 winner +30%, generate 3 new hooks",
        }
