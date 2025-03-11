Stock Portfolio Tracker

Stock Portfolio Tracker is a Python-based application that allows users to manage and track their stock investments. Users can add stock positions by entering a ticker symbol, and the application automatically retrieves the ISIN, currency, and latest stock price from Yahoo Finance. The program then generates reports that show individual position details and overall portfolio performance.

Features:

Automatic ISIN Retrieval – Users enter only the ticker, and the ISIN is fetched from Yahoo Finance.

Current Stock Price & Currency – Automatically updates stock prices for accurate profit/loss calculations.

Portfolio Aggregation – Aggregates all stock positions for each ticker, displaying a summary along with individual purchase details.

Profit/Loss Tracking – Calculates individual and total profit/loss in percentage and absolute values.

CSV Data Storage – Saves and loads stock positions from a CSV file.

Easy-to-use Interface – Simple menu-driven console UI for adding and reviewing stock positions.


Prerequisites:
pip install yfinance pandas