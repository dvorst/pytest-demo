import pytest
import pandas as pd
import numpy as np
from src.utils import apply_hamming_window


@pytest.fixture
def df_inp():
    """Fixture providing a sample DataFrame with numeric and non-numeric columns."""
    return pd.DataFrame(
        {
            "signal1": [1.0, 2.0, 3.0, 4.0, 5.0],
            "signal2": [10.0, 20.0, 30.0, 40.0, 50.0],
            "category": ["A", "B", "C", "D", "E"],  # Non-numeric column
        }
    )


def test_apply_hamming_window_correct_transformation(df_inp):
    """Test if the Hamming window is correctly applied to numeric columns."""
    # Arrange
    df = df_inp
    window = np.hamming(len(df))
    expected_df = df.copy()
    expected_df["signal1"] = expected_df["signal1"] * window
    expected_df["signal2"] = expected_df["signal2"] * window

    # Act
    result_df = apply_hamming_window(df)

    # Assert
    pd.testing.assert_frame_equal(result_df, expected_df)


def test_apply_hamming_window_ignores_non_numeric_columns(df_inp):
    """Test if non-numeric columns remain unchanged after transformation."""
    # Arrange
    df = df_inp

    # Act
    result_df = apply_hamming_window(df)

    # Assert
    assert "category" in result_df.columns
    assert result_df["category"].equals(df["category"])


def test_apply_hamming_window_raises_error_on_empty_dataframe():
    """Test if function raises ValueError when given an empty DataFrame."""
    # Arrange
    empty_df = pd.DataFrame()

    # Act & Assert
    with pytest.raises(ValueError, match="DataFrame is empty"):
        apply_hamming_window(empty_df)


def test_apply_hamming_window_does_not_modify_original_dataframe(df_inp):
    """Test if the original DataFrame remains unchanged after applying the function."""
    # Arrange
    df_original = df_inp.copy()

    # Act
    _ = apply_hamming_window(df_inp)

    # Assert
    pd.testing.assert_frame_equal(df_inp, df_original)
