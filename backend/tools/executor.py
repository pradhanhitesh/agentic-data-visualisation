from agents.insight import VisualizationPlan
from tools.charts import *
from data.load import load_data
import polars as pl

# Maps visualization plans to functions
TOOLS_MAP = {
    "histogram": histogram,
    "bar": bar,
    "boxplot": boxplot,
    "scatter": scatter,
    "regression": regression,
    "grouped_bar": grouped_bar,
    "stacked_bar": stacked_bar,
}


def get_feature_type(df: pl.DataFrame, col: str) -> str:
    """
    Args:
        df (pl.DataFrame): DataFrame
        col (str): Column name
    
    Output:
        str: Type of feature
    """
    dtype = df[col].dtype
    return "numeric" if dtype.is_numeric() else "categorical"


def validate_plan(plan: VisualizationPlan, df: pl.DataFrame) -> bool:
    """
    Args:
        plan (VisualizationPlan): Visualization plan
        df (pl.DataFrame): DataFrame
    
    Output:
        bool: True if plan is valid, False otherwise
    """
    for col in plan.vars:
        if col not in df.columns:
            return False
    return True

def execute_plans(plans: list[VisualizationPlan], df: pl.DataFrame, save_path: str):
    """
    Args:
        plans (list[VisualizationPlan]): List of visualization plans
        df (pl.DataFrame): DataFrame
        save_path (str): Path to save the visualizations
    
    Output:
        list[dict]: List of results
    """
    # Create save path if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # Empty list to store the results
    results = []

    # Convert DataFrame to dictionary for easier processing
    df_dict = df.to_dict()  

    # Iterate through the plans
    for i, plan in enumerate(plans):
        # Validate the plan
        if not validate_plan(plan, df):
            continue

        # Pick tool
        tool_name = plan.tools[0] if plan.tools else None
        func = TOOLS_MAP.get(tool_name)

        # Skip if tool is not found
        if not func:
            continue

        # Try to execute the plan
        try:
            # Route based on analysis_type
            if plan.analysis_type == "distribution":
                output = func(df_dict, plan.vars[0], save_fig=True, save_path=save_path)

            elif plan.analysis_type == "comparison":
                output = func(df_dict, plan.vars[0], plan.vars[1], save_fig=True, save_path=save_path)

            elif plan.analysis_type == "relationship":
                output = func(df_dict, plan.vars[0], plan.vars[1], save_fig=True, save_path=save_path)

            elif plan.analysis_type == "composition":
                output = func(df_dict, plan.vars[0], save_fig=True, save_path=save_path)

            else:
                continue

            results.append({
                "plan": plan,
                "tool": tool_name,
                "status": "success",
                "output": output
            })

        except Exception as e:
            results.append({
                "plan": plan,
                "tool": tool_name,
                "status": "failed",
                "error": str(e)
            })

    return results
