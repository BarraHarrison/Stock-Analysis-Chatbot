# Stock Analysis Chatbot powered by ChatGPT
import json
import openai
import pandas as pd 
import matplotlib as plt 
import streamlit as st 
import yfinance as yf 

openai.api_key = open("API_KEY.txt", "r").read()

def get_stock_price(ticker):
    return str(yf.Ticker(ticker).history(period="1y").iloc[-1].Close)

def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period="1y").Close
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period="1y").Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period="1y").Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14-1, adjust=False).mean()
    rs = ema_up /ema_down
    return str(100 - (100 / (1+rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period="1y").Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal

    return f"{MACD[-1], {signal[-1], MACD_histogram[-1]}}"


def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period="1y")
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f"{ticker} Stock Price Over Last Year")
    plt.x_label("Date")
    plt.y_label("Stock Price ($)")
    plt.grid(True)
    plt.savefig("stock.png")
    plt.close()


functions = [
    {
        "name": "get_stock_price",
        "description": "Gets the latest stock price given the ticker symbol of a company",
        "parameters": {
            "type": "object",
            "property": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (For example AAPL for Apple)"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "calculate_SMA",
        "description": "Calculates the Simple Moving Average (SMA) for a given stock ticker and time window",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)"
                },
                "window": {
                    "type": "integer",
                    "description": "The time window in days for calculating the SMA (e.g., 50 for a 50-day SMA)"
                }
            },
            "required": ["ticker", "window"]
        }
    },
    {
        "name": "calculate_EMA",
        "description": "Calculates the Exponential Moving Average (EMA) for a given stock ticker and time window",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)"
                },
                "window": {
                    "type": "integer",
                    "description": "The time window in days for calculating the EMA (e.g., 50 for a 50-day EMA)"
                }
            },
            "required": ["ticker", "window"]
        }
    },
    {
        "name": "calculate_RSI",
        "description": "Calculates the Relative Strength Index (RSI) for a given stock ticker",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "calculate_MACD",
        "description": "Calculates the Moving Average Convergence Divergence (MACD) indicator for a given stock ticker",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "plot_stock_price",
        "description": "Generates and saves a stock price chart for the given ticker symbol over the last year",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)"
                }
            },
            "required": ["ticker"]
        }
    }

    ]