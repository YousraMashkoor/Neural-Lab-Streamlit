import pandas as pd
import streamlit as st
import altair as alt
     
# reading dataset
data = pd.read_csv('stats_full_stack_dev.csv')
data = data.dropna(subset=['time_stamp'])


def visualize_functions(df, rows):
    # Filter the dataframe to get the required number of rows
    df = df.head(rows)
    
    # Using Altair, create a grid of charts for each function
    charts = []
    for function in df['Function'].unique():
        data = df[df['Function'] == function]
        chart = alt.Chart(data).mark_line().encode(
            x='time_stamp',
            y='Time',
            color='Function'
        ).properties(
            width=300,
            height=200,
            title=function
        )
        charts.append(chart)
    
    # Display the charts
    st.altair_chart(alt.hconcat(*charts))


def main():
    # Set the page title
    st.set_page_config(page_title='Log Functions Visualizations')
    
    # Add a title to the page
    st.title('Log Functions Visualizations')
    
    # Add an input field to enter number of rows to display, default 100
    rows = int(st.text_input("Number of rows to visualize_functions", 100))
    
    # Create the visualizations
    visualize_functions(data, rows)

if __name__ == '__main__':
    main()