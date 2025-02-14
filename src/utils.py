import pandas as pd
import numpy as np


def apply_hamming_window(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies a Hamming window to all numeric columns in the DataFrame.

    The function multiplies each numeric column by a Hamming window of the same length.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing numeric and non-numeric columns.

    Returns:
    --------
    pd.DataFrame
        A new DataFrame where numeric columns have been multiplied by the Hamming window.
        Non-numeric columns remain unchanged.

    Raises:
    -------
    ValueError
        If the input DataFrame is empty.

    Example:
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [10, 20, 30, 40]})
    >>> apply_hamming_window(df)
          A     B
    0  0.08   0.8
    1  1.54  15.4
    2  2.31  23.1
    3  0.32   3.2
    """
    if df.empty:
        raise ValueError("DataFrame is empty")

    df = df.copy()  # Avoid modifying the original DataFrame
    window = np.hamming(len(df))  # Generate Hamming window

    for column in df.select_dtypes(include=[np.number]).columns:
        df[column] = df[column] * window  # Apply window

    return df


def some_function_not_covered_by_a_test(x: pd.DataFrame) -> pd.DataFrame:
    return x.apply(lambda x: float(x.replace(" ", "").replace(",", ".")))
