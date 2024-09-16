import streamlit as st
import openai
import pandas as pd
import yfinance as yf

# Set OpenAI API Key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title('Interactive Financial Stock Market Comparative Analysis Tool')

# Function to fetch stock data
def get_stock_data(ticker, start_date='2024-01-01', end_date='2024-02-01'):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Sidebar for user inputs
st.sidebar.header('User Input Options')
selected_stock = st.sidebar.text_input('Enter Stock Ticker 1', 'AAPL').upper()
selected_stock2 = st.sidebar.text_input('Enter Stock Ticker 2', 'GOOGL').upper()

# Fetch stock data
stock_data = get_stock_data(selected_stock)
stock_data2 = get_stock_data(selected_stock2)

combined_data = pd.DataFrame({
    f'{selected_stock} Close': stock_data['Close'],
    f'{selected_stock2} Close': stock_data2['Close']
})

col1, col2, col3 = st.columns(3)

# Display stock data
with col1:
    st.subheader(f"Displaying data for: {selected_stock}")
    st.write(stock_data)
    

with col2:
    st.subheader(f"Displaying data for: {selected_stock2}")
    st.write(stock_data2)
    
with col3:
    chart_type2 = st.sidebar.selectbox(f'Select Chart Type for {selected_stock} and {selected_stock2} combined', ['Line', 'Bar'])
    if chart_type2 == 'Bar':
        st.bar_chart(combined_data)
    elif chart_type2 == 'Line':
        st.line_chart(combined_data)
    

# Comparative Performance using OpenAI GPT
if st.button('Comparative Performance'):
    # Prepare messages for GPT-3.5 Turbo
    prompt = f"""
    This is the {selected_stock} stock data : {stock_data.to_string(index=False)},
    and this is {selected_stock2} stock data: {stock_data2.to_string(index=False)}.
    Summarize the comparative performance of both stocks with highlights and a conclusion.
    """

    # OpenAI GPT-3.5 Turbo request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Display GPT response
    st.markdown(response['choices'][0]['message']['content'])

