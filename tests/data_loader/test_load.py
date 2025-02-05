from unittest.mock import Mock
from unittest.mock import patch
from src import data_loader
import pytest
import pandas as pd
from snowflake.connector import SnowflakeConnection


@pytest.fixture
def df_snowflake():
    return pd.DataFrame({"COL_A": [1]})


@pytest.fixture
def df_true():
    return pd.DataFrame({"col_a": [1]})


@pytest.fixture
def mock_con(df_snowflake):
    m = Mock(spec=SnowflakeConnection)
    ctx = Mock()
    ctx.return_value.cursor.return_value.fetch_pandas_all.return_value = df_snowflake
    m.__enter__ = ctx
    m.__exit__ = Mock()

    return m


@pytest.fixture
def mock_connect(mock_con):
    with patch("snowflake.connector.connect") as m:
        m.return_value = mock_con
        yield m


def test_with_con(mock_con, df_true, mock_connect: Mock):
    # Act
    df_return = data_loader.load(mock_con)

    # Assert
    pd.testing.assert_frame_equal(df_return, df_true)
    mock_connect.assert_not_called()


def test_without_con(mock_connect, df_true):
    # Act
    df_return = data_loader.load()

    # Assert
    pd.testing.assert_frame_equal(df_return, df_true)
    mock_connect.assert_called_once()
