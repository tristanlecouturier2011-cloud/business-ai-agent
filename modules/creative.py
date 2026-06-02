"""Génère scripts UGC, hooks et briefs vidéo via LLM."""
from openai import OpenAI
import json
from typing import Dict, List

class CreativeEngine:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_pack(self, product: Dict) -> Dict:
        prompt = f"""Tu es un copywriter UGC TikTok expert. Génère un pack créa pour ce produit:
Produit: {product['product_name']}
Niche: {product.get('hashtag', '')}
Score: {product['potential_score']}/100
Fournis en JSON strict:
{{
  "scripts": [
    {{"angle": "Hook-Problem-Solution", "duration_s": 15, "hook": "...", "body": "...", "cta": "..."}},
    {{"angle": "Before/After", "duration_s": 30, "hook": "...", "body": "...", "cta": "..."}},
    {{"angle": "Social Proof", "duration_s": 30, "hook": "...", "body": "...", "cta": "..."}}
  ],
  "hooks_text": ["10 hooks courts pour Spark Ads, max 8 mots"],
  "offers": [{{"type": "discount", "value": "-29%"}}, {{"type": "bundle", "value": "2+1 gratuit"}}],
  "voiceover_tone": "...",
  "subtitles_style": "..."
}}"""
        
        resp = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)

    def generate_video_brief(self, script: Dict) -> str:
        """Brief storyboard pour générateur vidéo (Heygen, Arcads, Runway)."""
        return (
            f"Format: 9:16, durée {script['duration_s']}s.\n"
            f"Plan 1 (0-3s): {script['hook']} — gros plan visage, expression surprise.\n"
            f"Plan 2 (3-{script['duration_s']-3}s): {script['body']} — produit en action.\n"
            f"Plan 3 (final): {script['cta']} — texte animé, logo, prix barré.\n"
            f"Sous-titres: bold blanc, fond noir 60%. TTS voix naturelle FR."
        )
