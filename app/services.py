# app/services.py
import random
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load dataset
df = pd.read_csv("data/simimpact_ai_training_dataset_10k.csv")

# Setup OpenAI client (read API key from .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_simulation(scenario: str):
    """Enhanced simulation using dataset + AI narrative generation"""

    # Sample one record from dataset
    row = df.sample(1).iloc[0]

    import datetime
    result = {
        "adoption_probability": float(row["adoption_willingness"]),
        "churn_risk": float(row["monthly_churn_rate"]),
        "referral_likelihood": float(row["referral_rate"]),
        "regional_heat": {
            "Lagos": random.choice(["low", "medium", "high"]),
            "Abuja": random.choice(["low", "medium", "high"]),
            "Kano": random.choice(["low", "medium", "high"]),
        },
        "adoption_curve": [0.1, 0.3, 0.5, 0.65, 0.75, 0.8],
        "retention_curve": [1.0, 0.9, 0.8, 0.72, 0.68, 0.65],
        "revenue_projection": {
            "month_1": 1000.0,
            "month_3": 5000.0,
            "month_6": 12000.0,
            "month_12": 25000.0,
        },
        "customer_segments": {
            "students": 0.5,
            "working_class": 0.3,
            "entrepreneurs": 0.2,
        },
        "satisfaction_score": 0.75,
        "break_even_point_months": 8,
        "industry_fit": "Steady adoption with student-driven growth",
        "dataset_row": {
            "adoption_willingness": float(row["adoption_willingness"]),
            "monthly_churn_rate": float(row["monthly_churn_rate"]),
            "referral_rate": float(row["referral_rate"])
        },
        "query": scenario,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # --- Generate richer AI summary ---
    try:
        prompt = f"""
        You are a business analyst AI. Analyze the following simulation for the scenario: "{scenario}".

        Metrics:
        - Adoption Probability: {result['adoption_probability']}
        - Churn Risk: {result['churn_risk']}
        - Referral Likelihood: {result['referral_likelihood']}
        - Regional Heat: {result['regional_heat']}
        - Adoption Curve: {result['adoption_curve']}
        - Retention Curve: {result['retention_curve']}
        - Revenue Projection: {result['revenue_projection']}
        - Customer Segments: {result['customer_segments']}
        - Satisfaction Score: {result['satisfaction_score']}
        - Break-even Point (months): {result['break_even_point_months']}
        - Industry Fit: {result['industry_fit']}

        Write a clear business-style summary (5–6 sentences). Highlight:
        1. Market potential
        2. Risks (like churn)
        3. Customer behavior
        4. Financial outlook
        5. Strategic recommendation
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )

        result["summary"] = response.choices[0].message.content.strip()

    except Exception as e:
        result["summary"] = f"Scenario '{scenario}' shows adoption ~{result['adoption_probability']:.2f} (fallback summary). Error: {str(e)}"

    return result
