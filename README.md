# Stock-Analysis Chatbot powered by GPT4ALL

## 📚 Introduction
The **Stock-Analysis Chatbot** is an AI-powered chatbot that provides stock market insights using **GPT4All**. It allows users to analyze stock trends, calculate indicators like **SMA, EMA, RSI, and MACD**, and visualize stock prices—all while running **entirely offline** with GPT4All, eliminating the need for OpenAI’s API.

## 📝 Brief Description of All Functions Created
The project includes several key functions for stock data retrieval and analysis:
- **fetch_stock_data(ticker)** – Fetches stock price history from Yahoo Finance.
- **get_stock_price(data)** – Retrieves the latest closing price of a stock.
- **calculate_SMA(data, window)** – Computes the **Simple Moving Average (SMA)** over a specified period.
- **calculate_EMA(data, window)** – Computes the **Exponential Moving Average (EMA)** over a specified period.
- **calculate_RSI(data)** – Calculates the **Relative Strength Index (RSI)** to measure stock momentum.
- **calculate_MACD(data)** – Computes the **Moving Average Convergence Divergence (MACD)** to analyze trends.
- **plot_stock_price(data, ticker)** – Generates a **visual stock price chart** and saves it as an image.

## 📈 The Purpose of Function Definitions for OpenAI API
Initially, the chatbot was designed to work with **OpenAI’s API**, where function definitions were structured to:
- Define **API-callable functions** that OpenAI’s assistant could use.
- Enable **dynamic execution of stock analysis functions** based on user queries.
- Automate the retrieval of stock prices, indicators, and chart visualization.

However, due to **OpenAI API quota expiration**, I switched to **GPT4All**, which required refactoring function execution for local AI processing.

## 🌐 The Function of the Streamlit (st) Part of the Project
The **Streamlit UI** serves as the front-end for the chatbot, allowing users to interact with the AI model seamlessly. Key features include:
- **User Input Handling** – Accepts stock-related queries.
- **Session Management** – Maintains chat history across multiple interactions.
- **Model Communication** – Sends user queries to **GPT4All** and retrieves responses.
- **Stock Chart Display** – Shows generated stock charts directly in the UI.
- **Error Handling** – Displays messages for any issues (e.g., missing model files).

## 😔 Difficulties Faced: OpenAI Tokens Expired & GPT4ALL Download Issues
### **1️⃣ OpenAI API Issues**
- Initially, the chatbot was powered by **GPT-4 via OpenAI API**, but **free trial credits expired**, blocking API requests.
- The error **"insufficient_quota"** required switching to a local LLM.

### **2️⃣ GPT4ALL Model Download Issues**
- Encountered **"Model directory does not exist"** errors.
- Some model names were **not found**, requiring manual model selection.
- **wget not installed on macOS**, requiring **curl** for downloading models.

## 📚 What I Learned
- **How to integrate GPT4All** for local AI execution.
- **The importance of API quotas** and managing dependencies in AI projects.
- **Streamlit integration** for an interactive AI chatbot UI.
- **Using technical debugging** to resolve issues with OpenAI, GPT4All, and system dependencies.

## 🎉 Conclusion
The **Stock-Analysis Chatbot** still needs to successfully transitioned from an **OpenAI API-based** system to a fully **offline GPT4All-powered** chatbot.
On top of this, future improvements could include **more technical indicators**, **multi-stock comparisons**, and **faster response times** with optimized local models.



