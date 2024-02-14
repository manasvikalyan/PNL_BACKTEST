import streamlit as st
import pandas as pd

def load_data(uploaded_file):
    """
    Function to load CSV file into DataFrame.
    """
    df = pd.read_csv(uploaded_file)
    return df

def plot_profit_from_timeperiod(df, start_date, end_date):
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df2 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    st.title('Profit from {} to {}'.format(start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y')))
    st.bar_chart(df2.set_index('Date')['Profit'])

def plot_equity_curve(df, start_date, end_date):
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df2 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df2['Equity'] = df2['Profit'].cumsum()

    st.title('Equity Curve from {} to {}'.format(start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y')))
    st.line_chart(df2.set_index('Date')['Equity'])

def calculate_overall_profit(df):
    return df['Profit'].sum()

def calculate_overall_profit_percentage(df):
    return df['Profit'].sum() / 1000000 * 100

def calculate_max_profit(df):
    return df['Profit'].max()

def calculate_max_loss(df):
    return df['Profit'].min()

def calculate_loss_percentage(df):
    return (df['Profit'] < 0).sum() / len(df) * 100

def calculate_win_percentage(df):
    return (df['Profit'] > 0).sum() / len(df) * 100

def calculate_max_drawdown(df):
    peak = df['Profit'].cummax()
    trough = df['Profit'].cummin()
    return (peak - trough).max()    

def main():
    st.title("Stock Market Analysis")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.write("### Original Data")
        st.write(df)

        st.write("### Select Date Range")
        start_date = st.date_input("Start Date", pd.to_datetime(df['Date'].min()))
        end_date = st.date_input("End Date", pd.to_datetime(df['Date'].max()))

        if st.button("Process"):
            st.write("### Analysis Results")

            st.write("### 1. Profit Plot for Time Period")
            plot_profit_from_timeperiod(df, start_date, end_date)

            st.write("### 2. Equity Curve for Time Period")
            plot_equity_curve(df, start_date, end_date)

            df_selected = df[(df['Date'] >= start_date.strftime('%Y-%m-%d')) & (df['Date'] <= end_date.strftime('%Y-%m-%d'))]

            st.write("### 3. Overall Profit")
            overall_profit = calculate_overall_profit(df_selected)
            st.write(f"Overall Profit: {overall_profit}")

            st.write("### 4. Overall Profit Percentage")
            overall_profit_percentage = calculate_overall_profit_percentage(df_selected)
            st.write(f"Overall Profit Percentage: {overall_profit_percentage}")

            st.write("### 5. Max Profit")
            max_profit = calculate_max_profit(df_selected)
            st.write(f"Max Profit: {max_profit}")

            st.write("### 6. Max Loss")
            max_loss = calculate_max_loss(df_selected)
            st.write(f"Max Loss: {max_loss}")

            st.write("### 7. Loss Percentage (Days)")
            loss_percentage = calculate_loss_percentage(df_selected)
            st.write(f"Loss Percentage (Days): {loss_percentage}")

            st.write("### 8. Win Percentage (Days)")
            win_percentage = calculate_win_percentage(df_selected)
            st.write(f"Win Percentage (Days): {win_percentage}")

            st.write("### 9. Max Drawdown")
            max_drawdown = calculate_max_drawdown(df_selected)
            st.write(f"Max Drawdown: {max_drawdown}")

if __name__ == "__main__":
    main()
