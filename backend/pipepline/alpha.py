from data.load import load_data
from data.profile import DataProfile
from agents.insight import InsightAgent
from tools.executor import execute_plans
import os

def run_pipeline(filepath: str, session_id: str):
    try:
        # Load dataset
        data = load_data(filepath=filepath)

        # Make folder
        os.makedirs(f"assets/sessions/{session_id}", exist_ok=True)

        # Generate profile
        profile = DataProfile(data=data)
        profile_data = profile.generate()

        # Generate insight
        insight_agent = InsightAgent(data_profile=profile_data)
        insight_summary = insight_agent.generate()

        # Save markdown
        insight_text = insight_summary.root[0].insight
        with open(f"assets/sessions/{session_id}/insight.md", "w", encoding="utf-8") as f:
            f.write(insight_text)

        # Save plots
        execute_plans(insight_summary.root[0].plans, data, save_path=f"assets/sessions/{session_id}/plots")
        
    except Exception as e:
        raise AssertionError(e)
