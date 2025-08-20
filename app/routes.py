# app/routes.py
from fastapi import APIRouter
from app.models import SimulationRequest, SimulationResult
from app.services import run_simulation
from app.database import db, to_dict

router = APIRouter()

@router.post("/simulate", response_model=SimulationResult)
async def simulate(request: SimulationRequest):
    """
    Run a new simulation for a given scenario.
    Returns structured metrics + AI-generated insights.
    """
    # Run enhanced simulation
    result = run_simulation(request.scenario)

    # Save into DB with clear structure
    record = {
        "scenario": request.scenario,
        "metrics": {
            "adoption_probability": result["adoption_probability"],
            "churn_risk": result["churn_risk"],
            "referral_likelihood": result["referral_likelihood"],
            "regional_heat": result["regional_heat"],
        },
        "summary": result["summary"],
        "dataset_row": result.get("dataset_row"),
        "timestamp": result.get("timestamp")
    }
    await db.results.insert_one(record)
    # Add the query and timestamp to the result for frontend display
    result_with_query = {**result, "query": request.scenario, "timestamp": result.get("timestamp")}
    return result_with_query


@router.get("/history")
async def get_history(limit: int = 50):
    """
    Fetch past simulation results (default: last 50).
    Includes metrics, summary, and dataset reference.
    """
    results = await db.results.find().sort("_id", -1).to_list(limit)
    # Add 'query' and 'timestamp' fields to each history item (from 'scenario' and 'timestamp')
    return [{**to_dict(r), "query": r.get("scenario", ""), "timestamp": r.get("timestamp", "") } for r in results]


@router.delete("/history/clear")
async def clear_history():
    """
    Delete all simulation history records.
    Useful for resetting before a demo/hackathon pitch.
    """
    result = await db.results.delete_many({})
    return {"status": "success", "deleted_count": result.deleted_count}
