import pandas as pd
import numpy as np
import yfinance as yf
import warnings

warnings.filterwarnings("ignore")

# TODO:
# Type hint
# Field
# Optional
# Document functions
# Pytest/Unit Tests (Udacity content)
# log (Udacity content)


# Generic
class QuantFeatures:
    def __init__(self, data=None):
        self.data = data

    def download_data(self, ticker, start_date, end_date):
        """Download stock data from Yahoo Finance.

        Args:
            ticker (str): Stock symbol.
            start_date (str): Start date for data in the format "YYYY-MM-DD".
            end_date (str): End date for data in the format "YYYY-MM-DD".

        Returns:
            DataFrame: Stock data.
        """
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data

    def simple_moving_average(self, data, window):
        """Method to calculate SMA (Simple Moving Average) from a series of values.

        The Series must be ordered from oldest date to newest date.

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: Calculated moving average.
        """

        return data.rolling(window).mean()

    def moving_std(self, data, window):
        """Method to calculate moving standard deviation from a series of values.

        The Series must be ordered from oldest date to newest date.

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: Calculated moving standard deviation.
        """

        return data.rolling(window).std()

    def moving_median(self, data, window):
        """Method to calculate moving median from a series of values.

        The Series must be ordered from oldest date to newest date.

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: Calculated moving standard median.
        """

        return data.rolling(window).median()

    # TODO: Variações -1, -5, -20
    # TODO: Time Features: % da semana, % do mês, % do trimestre % do ano

    # Oscilators
    def rolling_z_score(self, data, window):
        """Calculate the rolling Z-score.

        The Series must be ordered from oldest date to newest date.

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: Rolling Z-score.
        """

        sma = self.simple_moving_average(data, window)

        # Calculating the moving standard deviation
        moving_std_dev = self.moving_std(data, window)

        # Calculating distance between price and the MA
        distance_price_sma = data - sma

        return distance_price_sma / moving_std_dev

    def rolling_median_z_score(self, data, window):
        """Calculate the rolling median Z-score.

        The Series must be ordered from oldest date to newest date.

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: Rolling median Z-score.
        """

        mm = self.moving_median(data, window)

        # Calculating the moving standard deviation
        moving_std_dev = self.moving_std(data, window)

        # Calculating distance between price and the MA
        distance_price_mm = data - mm

        return distance_price_mm / moving_std_dev

    def rolling_ratio(self, data, window):
        """Calculate the rolling ratio of data and its mean (RSL).

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: Rolling ratio.
        """
        sma = self.simple_moving_average(data, window)

        return np.round((data / sma - 1), 3) * 100

    def rsi(self, data, window=15):
        """Calculate RSI indicator.

        Args:
            data (Series): Input data.
            window (int): Rolling window size.

        Returns:
            Series: RSI.
        """
        df_rsi = pd.DataFrame(data={"close": data})

        # Establish gains and losses for each day
        df_rsi["variation"] = df_rsi.diff()
        df_rsi = df_rsi[1:]
        df_rsi["gain"] = np.where(df_rsi["variation"] > 0, df_rsi["variation"], 0)
        df_rsi["loss"] = np.where(df_rsi["variation"] < 0, df_rsi["variation"], 0)

        # Calculate simple averages so we can initialize the classic averages
        df_rsi["avg_gain"] = df_rsi["gain"].rolling(window).mean()
        df_rsi["avg_loss"] = df_rsi["loss"].abs().rolling(window).mean()

        for i in range(window, len(df_rsi["avg_gain"])):
            df_rsi["avg_gain"][i] = df_rsi["avg_gain"][i - 1] * (window - 1)
            df_rsi["avg_gain"][i] = df_rsi["avg_gain"][i] + df_rsi["gain"][i]
            df_rsi["avg_gain"][i] = df_rsi["avg_gain"][i] / window

            df_rsi["avg_loss"][i] = df_rsi["avg_loss"][i - 1] * (window - 1)
            df_rsi["avg_loss"][i] = df_rsi["avg_loss"][i] + df_rsi["loss"].abs()[i]
            df_rsi["avg_loss"][i] = df_rsi["avg_loss"][i] / window

        # Calculate the RSI
        df_rsi["rs"] = df_rsi["avg_gain"] / df_rsi["avg_loss"]
        df_rsi["rsi"] = 100 - (100 / (1 + df_rsi["rs"]))

        return df_rsi["rsi"]

    # Candles Patterns
    def candle_proportions(self, open, high, low, close):
        """Method to calculate proportion of the candle's body and shadows.

        Args:
            open, high, low, close (Series): Input data from candle.

        Returns:
            Series: Proportions of candle's body.
            Series: Proportions of top shadow.
            Series: Proportions of bottom shadow.
        """
        candle_size = high - low

        body_top = pd.Series(map(max, zip(open, close)))
        body_top.index = close.index
        top_shadow = (high - body_top) / candle_size

        body_bottom = pd.Series(map(min, zip(open, close)))
        body_bottom.index = close.index
        bottom_shadow = (body_bottom - low) / candle_size

        body = 1 - top_shadow - bottom_shadow

        return top_shadow, body, bottom_shadow

    def sequence_counter(self, data):
        """Method to count sequence of periods in the same direction.

        Args:
            data (Series): Input data.

        Returns:
            Series: Sequence count on same direction.
        """

        shifted_data = data.shift(1)

        high_or_low = data - shifted_data

        high_or_low[high_or_low > 0] = 1
        high_or_low[high_or_low < 0] = -1
        high_or_low[high_or_low == 0] = 0

        shifted_values_directions = high_or_low.shift(1)
        # Comparing if has direction change
        has_direction_change = high_or_low.ne(shifted_values_directions)
        # Calculate cumsum of direction change to obtain the references for groupby
        group_references = has_direction_change.cumsum()
        # Group by positions where have direction change
        grouped_values = high_or_low.groupby(group_references)

        # Cumulative count to calculate each sequence (starting by 1)
        return (grouped_values.cumcount()) + 1

    def candle_color(self, open, close):
        """Method to get the candle color.

        Args:
            open, close (Series): Input data from candle.

        Returns:
            color (Int): {1:Green, -1:Red}.
        """

        return np.where(close > open, 1, -1)

    # TODO
    # Resistencias complexas e rompimentos (Tipo MVST)
    # Classe de execução de Backtest
    # Classe que ajuda na criação de features (Passa um dicionário com features e parametros)
