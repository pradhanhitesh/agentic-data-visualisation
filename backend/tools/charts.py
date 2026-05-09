import matplotlib
matplotlib.use("Agg")

import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os


def _prepare_df(df):
    """
    Args:
        df (dict): Dictionary representation of DataFrame
    
    Returns:
        pd.DataFrame: DataFrame
    """
    if isinstance(df, pl.DataFrame):
        return df.to_pandas()
    return df


def _save(fig, save_fig: bool, save_path: str, filename: str):
    """
    Args:
        fig (matplotlib.figure.Figure): Figure to save
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
        filename (str): Filename
    
    Returns:
        str: Path to the saved figure
    """
    if save_fig:
        os.makedirs(save_path, exist_ok=True)
        full_path = os.path.join(save_path, filename)
        fig.savefig(full_path, bbox_inches="tight")
        return full_path
    return None

def histogram(df: dict, column: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        column (str): Column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    fig, ax = plt.subplots()
    sns.histplot(df[column], kde=True, ax=ax)

    ax.set_title(f"Histogram of {column}")

    path = _save(fig, save_fig, save_path, f"hist_{column}.png")
    plt.close(fig)

    return f"Histogram generated for {column}" + (f" | saved to {path}" if path else "")

def boxplot(df: dict, column: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        column (str): Column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    fig, ax = plt.subplots()
    sns.boxplot(x=df[column], ax=ax)

    ax.set_title(f"Boxplot of {column}")

    path = _save(fig, save_fig, save_path, f"box_{column}.png")
    plt.close(fig)

    return f"Boxplot generated for {column}" + (f" | saved to {path}" if path else "")

def bar(df: dict, column: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        column (str): Column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    fig, ax = plt.subplots()
    sns.countplot(x=df[column], ax=ax)

    ax.set_title(f"Bar plot of {column}")
    ax.tick_params(axis='x', rotation=45)

    path = _save(fig, save_fig, save_path, f"bar_{column}.png")
    plt.close(fig)

    return f"Bar chart generated for {column}" + (f" | saved to {path}" if path else "")

def grouped_bar(df: dict, group_col: str, value_col: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        group_col (str): Grouping column name
        value_col (str): Value column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    fig, ax = plt.subplots()
    sns.barplot(data=df, x=group_col, y=value_col, ax=ax)

    ax.set_title(f"{value_col} by {group_col}")
    ax.tick_params(axis='x', rotation=45)

    path = _save(fig, save_fig, save_path, f"grouped_{group_col}_{value_col}.png")
    plt.close(fig)

    return f"Grouped bar chart for {value_col} by {group_col}" + (f" | saved to {path}" if path else "")

def scatter(df: dict, x: str, y: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        x (str): X-axis column name
        y (str): Y-axis column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x, y=y, ax=ax)

    ax.set_title(f"{x} vs {y}")

    path = _save(fig, save_fig, save_path, f"scatter_{x}_{y}.png")
    plt.close(fig)

    return f"Scatter plot for {x} vs {y}" + (f" | saved to {path}" if path else "")

def regression(df: dict, x: str, y: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        x (str): X-axis column name
        y (str): Y-axis column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    fig, ax = plt.subplots()
    sns.regplot(data=df, x=x, y=y, ax=ax)

    ax.set_title(f"Regression: {x} vs {y}")

    path = _save(fig, save_fig, save_path, f"reg_{x}_{y}.png")
    plt.close(fig)

    return f"Regression plot for {x} vs {y}" + (f" | saved to {path}" if path else "")

def stacked_bar(df: dict, column: str, save_fig: bool = False, save_path: str = "assets/plots") -> str:
    """
    Args:
        df (dict): Dictionary representation of DataFrame
        column (str): Column name
        save_fig (bool): Whether to save the figure
        save_path (str): Path to save the figure
    
    Returns:
        str: Message indicating the status of the operation
    """
    df = _prepare_df(pl.DataFrame(df))

    counts = df[column].value_counts().to_pandas()

    fig, ax = plt.subplots()
    ax.bar(counts[column], counts["count"])

    ax.set_title(f"Composition of {column}")
    ax.tick_params(axis='x', rotation=45)

    path = _save(fig, save_fig, save_path, f"stacked_{column}.png")
    plt.close(fig)

    return f"Stacked bar chart for {column}" + (f" | saved to {path}" if path else "")