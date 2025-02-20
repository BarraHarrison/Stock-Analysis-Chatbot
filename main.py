# Stock Analysis Chatbot powered by ChatGPT
import json
import openai
import pandas as pd 
import matplotlib.pyplot as plt 
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

    return json.dumps({
    "MACD": MACD.iloc[-1],
    "Signal": signal.iloc[-1],
    "Histogram": MACD_histogram.iloc[-1]
})



def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period="1y")
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f"{ticker} Stock Price Over Last Year")
    plt.xlabel("Date")
    plt.ylabel("Stock Price ($)")
    plt.grid(True)
    plt.savefig("stock.png")
    plt.close()


functions = [
    {
        "name": "get_stock_price",
        "description": "Gets the latest stock price given the ticker symbol of a company",
        "parameters": {
            "type": "object",
            "properties": {
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

available_functions = {
    "get_stock_price": get_stock_price,
    "calculate_SMA": calculate_SMA,
    "calculate_EMA": calculate_EMA,
    "calculate_RSI": calculate_RSI,
    "calculate_MACD": calculate_MACD,
    "plot_stock_price": plot_stock_price
}

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("Stock Analysis Assistant")

user_input = st.text_input("Your input:")
if user_input:
    try:
        st.session_state["messages"].append({"role": "user", "content": f"{user_input}"})
        response = openai.ChatCompletion.create(
            model = "GPT-4o",
            messages = st.session_state["messages"],
            functions = functions,
            function_call = "auto"
        )

        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_arguments = json.loads(response_message["function_call"]["arguments"])
            if function_name in ["get_stock_price", "calculate_RSI", "calculate_MACD", "plot_stock_price"]:
                arguments_dictionary = {"ticker": function_arguments.get("ticker")}
            elif function_name in ["calculate_SMA", "calculate_EMA"]:
                arguments_dictionary = {"ticker": function_arguments.get("ticker"), "window": function_arguments.get("window")}

            function_to_call = available_functions[function_name]
            function_response = function_to_call(**arguments_dictionary)

            if function_name == "plot_stock_price":
                st.image("stock.png")
            else:
                st.session_state["messages"].append(response_message)
                st.session_state["messages"].append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response
                    }
                )
                second_response = openai.ChatCompletion.create(
                    model = "GPT-4o",
                    messages = st.session_state["messages"]
                )
                st.text(second_response["choices"][0]["message"]["content"])
                st.session_state["messages"].append({"role": "assistant", "content": second_response["choices"][0]["message"]["content"]})
        
        else:
            st.text(response_message["content"])
            st.session_state["messages"].append({"role": "assistant", "content": response_message["content"]})
    except Exception as e:
        st.text(f"An error occurred: {e}")