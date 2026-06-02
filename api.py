"""FastAPI Web Server pour AdTok Agent."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
from adtok_agent import AdTokAgent

# Initialiser FastAPI
app = FastAPI(
    title="AdTok Agent API",
    description="Automatise la création de campagnes TikTok Ads rentables en 48h",
    version="1.0.0"
)

# CORS - Autoriser tous les domaines (adapter en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser l'agent
agent = AdTokAgent()

# Modèles Pydantic
class PipelineRequest(BaseModel):
    niche: str
    budget: Optional[float] = 100.0

class PipelineResponse(BaseModel):
    status: str
    message: str
    data: dict

# Routes
@app.get("/")
async def root():
    """Root endpoint - bienvenue."""
    return {
        "app": "AdTok Agent API",
        "version": "1.0.0",
        "endpoints": {
            "POST /run": "Lancer le pipeline complet 48h",
            "GET /health": "Vérifier la santé de l'API",
            "GET /docs": "Documentation interactive (Swagger)",
            "GET /redoc": "Documentation alternative (ReDoc)"
        }
    }

@app.get("/health")
async def health():
    """Vérifier la santé de l'API."""
    return {
        "status": "healthy",
        "agent": "ready",
        "database": "connected" if os.path.exists("data/adtok.db") else "initializing"
    }

@app.post("/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest):
    """
    Lancer le pipeline complet AdTok Agent.
    
    **Paramètres:**
    - `niche` (str): Niche produit (beauty, skincare, fitness, etc.)
    - `budget` (float): Budget quotidien en € (défaut: 100)
    
    **Retour:**
    - Résultats du pipeline complet 48h
    
    **Exemple:**
    ```json
    {
      "niche": "beauty",
      "budget": 150.0
    }
    ```
    """
    try:
        if not request.niche or len(request.niche.strip()) == 0:
            raise HTTPException(status_code=400, detail="Niche ne peut pas être vide")
        
        if request.budget <= 0:
            raise HTTPException(status_code=400, detail="Budget doit être > 0")
        
        # Lancer le pipeline
        result = agent.run_pipeline(request.niche, request.budget)
        
        return PipelineResponse(
            status="success",
            message=f"Pipeline complété pour la niche '{request.niche}' avec budget {request.budget}€",
            data=result
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/runs")
async def get_runs():
    """Récupérer tous les runs précédents."""
    try:
        import sqlite3
        conn = sqlite3.connect("data/adtok.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM runs ORDER BY created_at DESC LIMIT 50")
        runs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"status": "success", "count": len(runs), "data": runs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur BD: {str(e)}")

@app.get("/last-run")
async def get_last_run():
    """Récupérer le dernier run complet."""
    try:
        if not os.path.exists("data/last_run.json"):
            raise HTTPException(status_code=404, detail="Aucun run trouvé. Lancez d'abord /run")
        
        with open("data/last_run.json", "r") as f:
            data = json.load(f)
        
        return {"status": "success", "data": data}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Aucun run trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Récupérer les statistiques globales."""
    try:
        import sqlite3
        conn = sqlite3.connect("data/adtok.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM runs")
        total_runs = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(score) FROM runs")
        avg_score = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT MAX(score) FROM runs")
        max_score = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(DISTINCT niche) FROM runs")
        niches_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "success",
            "total_runs": total_runs,
            "avg_score": round(avg_score, 1),
            "max_score": round(max_score, 1),
            "niches_tested": niches_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# Lancement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
