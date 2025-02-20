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