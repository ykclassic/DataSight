# app/services/insight_service.py
from app.engines.insight_engine import analyze_insights

def generate_insights(db_data_dict):
    """
    Combines schema + profiling + AI insights
    """
    insights = analyze_insights(db_data_dict)
    return insights
