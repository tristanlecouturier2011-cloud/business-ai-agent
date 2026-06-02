"""Génère et publie un mini-site one-product."""
import requests
from typing import Dict

class MiniSiteBuilder:
    def __init__(self, lovable_url: str = None):
        self.lovable_url = lovable_url

    def build_brief(self, product: Dict, creative: Dict) -> Dict:
        offer = creative["offers"][0] if creative.get("offers") else {"type": "discount", "value": "-20%"}
        return {
            "product_name": product["product_name"],
            "hero_title": creative["scripts"][0]["hook"],
            "hero_subtitle": "Livraison gratuite • Satisfait ou remboursé 30 jours",
            "benefits": [
                "Résultats visibles en 7 jours",
                "Formule clean, testée dermatologiquement",
                "Approuvé par +10 000 clients",
            ],
            "offer": offer,
            "social_proof": [
                {"name": "Léa M.", "rating": 5, "text": "Bluffée par les résultats."},
                {"name": "Tom R.", "rating": 5, "text": "Mon nouvel essentiel."},
                {"name": "Sarah K.", "rating": 5, "text": "Je recommande à 100%."},
            ],
            "faq": [
                {"q": "Délai de livraison ?", "a": "3-5 jours ouvrés."},
                {"q": "Politique de retour ?", "a": "30 jours satisfait ou remboursé."},
                {"q": "Paiement sécurisé ?", "a": "Oui, Stripe + cryptage SSL."},
            ],
            "checkout": {"provider": "stripe", "currency": "EUR"},
            "pixels": {"tiktok": True, "meta": True},
            "colors": {"primary": "#FF4D4F", "bg": "#FFFFFF", "text": "#111111"},
        }

    def publish(self, brief: Dict) -> str:
        # Stub: en prod, appel API Lovable / OVA / Vercel deploy
        # Ici on simule un retour d'URL
        slug = brief["product_name"].lower().replace(" ", "-")
        return f"https://adtok.shop/{slug}"
