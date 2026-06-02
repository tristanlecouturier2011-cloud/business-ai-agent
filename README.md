# AdTok Agent 🤖

**AdTok Agent** est un assistant IA autonome qui automatise la création et le lancement de campagnes TikTok Ads rentables en 48 heures.

## 🎯 Fonctionnalités

### 1. **Sourcing Intelligent**
- Scrape les tendances TikTok en temps réel
- Analyse les produits candidats par niche
- Détecte l'activité des concurrents

### 2. **Scoring Automatisé**
- Score de potentiel de conversion (0-100)
- Pondération multidimensionnelle:
  - Social proof (30%)
  - Engagement rate (25%)
  - CTR estimé (20%)
  - Compétition (15%)
  - Marge produit (10%)

### 3. **Génération Créative**
- Scripts UGC via GPT-4o
- Hooks viraux optimisés
- Briefs vidéo pour Heygen/Runway
- Offres promo générées automatiquement

### 4. **Construction Mini-Site**
- One-product landing page
- Intégration Stripe
- Pixels TikTok & Meta
- Preuve sociale automatique

### 5. **Pilotage Campagnes TikTok Ads**
- Création automatique de campagnes
- Ciblage multi-audiences
- Règles d'optimisation temps réel

### 6. **Rapports H+48**
- KPIs en temps réel
- Recommandations d'actions
- Tableaux de bord enrichis

## 📋 Structure du Projet

```
adtok-agent/
├── .env                    # Configuration (API keys)
├── requirements.txt        # Dépendances
├── adtok_agent.py         # Orchestrateur principal
├── modules/
│   ├── __init__.py
│   ├── sourcing.py        # Scraping TikTok & competitor radar
│   ├── scoring.py         # Calcul score de potentiel
│   ├── creative.py        # Génération créative (LLM)
│   ├── site.py            # Mini-site builder
│   ├── ads.py             # Pilotage TikTok Ads
│   └── reporting.py       # Rapports & dashboards
├── data/
│   └── adtok.db          # SQLite (runs, products, campaigns)
└── README.md
```

## 🚀 Démarrage Rapide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
Remplissez le fichier `.env`:
```bash
OPENAI_API_KEY=sk-xxx
TIKTOK_ACCESS_TOKEN=xxx
TIKTOK_ADVERTISER_ID=xxx
STRIPE_SECRET_KEY=sk_test_xxx
LOVABLE_PROJECT_URL=https://xxx.lovable.app
```

### 3. Exécution
```bash
# Pipeline complet avec niche "beauty"
python adtok_agent.py beauty 100

# Pipeline avec niche et budget personnalisé
python adtok_agent.py "skincare" 250
```

## 📊 Pipeline 48h

```
H+0 → H+2   : Sourcing & Scoring (50 produits → Top 10)
              ↓
H+6         : Génération Créative (6 vidéos UGC + 10 hooks)
              ↓
H+12        : Construction & Publication Mini-Site
              ↓
H+24        : Lancement Campagnes TikTok Ads (3 audiences)
              ↓
H+48        : Rapport KPIs + Recommandations d'Actions
```

## 🔧 Architecture Modulaire

### **Sourcing** (`modules/sourcing.py`)
```python
TikTokSourcer(token)
  .fetch_trending(niche, limit=50)      # 50 produits tendance
  .competitor_radar(keyword)             # Ads actives
```

### **Scoring** (`modules/scoring.py`)
```python
ProductScorer()
  .score(product)                        # Score unique (0-100)
  .top_n(products, n=10)                 # Tri & sélection
```

### **Créatif** (`modules/creative.py`)
```python
CreativeEngine(api_key)
  .generate_pack(product)                # Scripts + hooks + offres
  .generate_video_brief(script)          # Storyboard détaillé
```

### **Site** (`modules/site.py`)
```python
MiniSiteBuilder(lovable_url)
  .build_brief(product, creative)        # Brief de page
  .publish(brief)                        # Déploiement
```

### **Ads** (`modules/ads.py`)
```python
TikTokAdsManager(token, advertiser_id)
  .create_campaign(product, site_url)    # Campagne
  .create_adgroups(campaign_id)          # 3 audiences
  .apply_rules(metrics)                  # Optimisation
```

### **Reporting** (`modules/reporting.py`)
```python
Reporter()
  .top10_report(products)                # Tableau Top 10
  .h48_report(campaign_data)             # Rapport final
```

## 📈 Exemple de Résultat

```json
{
  "product": {
    "product_name": "Produit beauty #0",
    "potential_score": 87.5,
    "views": 1200000,
    "ctr_estimate": 1.5
  },
  "creative": {
    "scripts": [3 vidéos UGC],
    "hooks_text": [10 hooks courts],
    "offers": [{"type": "discount", "value": "-29%"}]
  },
  "site_url": "https://adtok.shop/produit-beauty-0",
  "campaign": {
    "campaign_id": "camp_Produit b",
    "status": "ACTIVE"
  },
  "report": {
    "kpis": {"ctr": 1.4, "cpa": 18, "impressions": 25000},
    "recommendations": ["SCALE +25% — CPA below target"]
  }
}
```

## 🔌 Intégrations

- **OpenAI GPT-4o** : Génération créative
- **TikTok API** : Sourcing & Ads
- **Stripe** : Paiements
- **Lovable** : Site builder (no-code)
- **SQLite** : Persistance runs

## 📝 Logs & Persistance

- Tous les runs sont enregistrés dans `data/adtok.db`
- Le dernier résultat JSON est sauvegardé dans `data/last_run.json`
- Sortie rich console en temps réel

## 🛠️ Développement

### Ajouter une nouvelle niche
```python
agent.run_pipeline("fitness", budget_daily=150)
```

### Personnaliser les règles d'optimisation
Modifiez `modules/ads.py` > `apply_rules()`

### Intégrer une vraie API TikTok
Remplacez les mocks dans `modules/sourcing.py` > `fetch_trending()`

## 📄 License

MIT

---

**Créé par** Tristan Lecouturier | **Année** 2026
