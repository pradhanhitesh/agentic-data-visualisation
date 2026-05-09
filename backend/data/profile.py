import polars as pl

class DataProfile:
    """
    Class to generate profile from dataset.
    """
    def __init__(self, data):
        self.data = data

    def generate(self, cat_threshold: int = 5):
        """
        Generate profile from dataset.

        Args:
            data: Polars DataFrame
            cat_threshold: Threshold for categorical variables

        Returns:
            Profile of the dataset
        """
        df = self.data

        profile = {}
        for col in df.columns:
            col_info = {}

            # Get dtype
            dtype = df.get_column(col).dtype

            # Get missing
            col_info["missing"] = df[col].is_null().sum()

            if dtype.is_numeric():
                col_info["type"] = "numeric"
                col_info["mean"] = round(df[col].mean(),2)
                col_info["standard_deviation"] = round(df[col].std(),2)
                col_info["median"] = round(df[col].median(),2)
                col_info["skew"] = round(df[col].skew(),2)
            elif dtype.is_temporal():
                col_info["type"] = "datetime"
            else:
                uniq_vals = df[col].n_unique()
                col_info["unique_values"] = uniq_vals

                if uniq_vals < cat_threshold:
                    col_info["type"] = "categotical"
                    col_info["value_counts"] = df[col].value_counts(sort=True, normalize=True).to_dicts()
                
            profile[col] = col_info

        return profile