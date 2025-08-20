from pydantic import BaseModel
from typing import Dict, List

class SimulationRequest(BaseModel):
    scenario: str

class SimulationResult(BaseModel):
    adoption_probability: float
    churn_risk: float
    referral_likelihood: float
    regional_heat: Dict[str, str]
    adoption_curve: List[float]
    retention_curve: List[float]
    revenue_projection: Dict[str, float]
    customer_segments: Dict[str, float]
    satisfaction_score: float
    break_even_point_months: int
    industry_fit: str
    summary: str
    query: str
