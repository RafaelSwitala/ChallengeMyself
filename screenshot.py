# pyright: reportUndefinedVariable=false



def filter_by_date_range(df: pd.DataFrame, 
                         date_from: Optional[str] = None, 
                         date_to: Optional[str] = None
                         ) -> pd.DataFrame:
    if date_from:
        df = df[df["date"] >= pd.to_datetime(date_from)]
    if date_to:
        df = df[df["date"] <= pd.to_datetime(date_to)]
    return df





