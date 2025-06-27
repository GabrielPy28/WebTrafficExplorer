import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.stattools import acf, pacf
import numpy as np
import plotly.express as px
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA

@st.cache_data
def load_data():
    try:
        dtype_dict = {
            'Row': int,
            'Day': str,
            'Day_Of_Week': int,
            'Date': str,
            'Page_Loads': str,
            'Unique_Visits': str,
            'First_Time_Visits': str,
            'Returning_Visits': str
        }
        df = pd.read_csv("../dataset/daily-website-visitors.csv", dtype=dtype_dict)
        df.columns = [col.replace('.', '_') for col in df.columns]
        for col in ['Page_Loads', 'Unique_Visits', 'First_Time_Visits', 'Returning_Visits']:
            df[col] = df[col].str.replace(',', '', regex=False).astype(int)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        return df
    except FileNotFoundError:
        st.error("The file 'daily-website-visitors.csv' was not found.")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def plot_heatmap(data):
    # Create columns for month and day of the week
    data['Month'] = data['Date'].dt.month_name().str.slice(stop=3)  # abbreviation
    data['Day_Name'] = data['Date'].dt.day_name().str.slice(stop=3)
    
    # Create pivot table with average unique visits by day and month
    pivot_table = data.pivot_table(
        index='Day_Name',
        columns='Month',
        values='Unique_Visits',
        aggfunc='mean'
    )
    
    # Order days and months to make sense in the heatmap
    days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    pivot_table = pivot_table.reindex(index=days_order)
    pivot_table = pivot_table[months_order]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale=[[0, '#fcffff'], [0.1, '#bcfdff'], [0.2, '#9ddbf9'], [0.3, '#7bbbf2'], [0.4, '#509beb'], [0.6, '#2b7ed7'], [0.8, '#1f62b7'], [0.9, '#114898'], [1, '#002f7a']],
        colorbar=dict(title='Unique Visits', bgcolor='rgba(252, 255, 255, 0)', tickcolor='#fdfefe', titlefont=dict(color='#fdfefe'))
    ))
    
    fig.update_layout(
        title='Heatmap: Unique Visits by Day of the Week and Month',
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        xaxis=dict(title='Month', titlefont=dict(color='#fdfefe'), tickfont=dict(color='#fdfefe')),
        yaxis=dict(title='Day of the Week', titlefont=dict(color='#fdfefe'), tickfont=dict(color='#fdfefe'))
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_boxplot(data):
    # Change category names in the DataFrame
    df_melt = data.melt(id_vars=['Date'], value_vars=['Unique_Visits', 'First_Time_Visits', 'Returning_Visits'], 
                        var_name='Visit Type', value_name='Count')
    
    # Change category names
    df_melt['Visit Type'] = df_melt['Visit Type'].replace({
        'Unique_Visits': 'Unique Visits',
        'First_Time_Visits': 'New User Visits',
        'Returning_Visits': 'Returning User Visits'
    })

    fig = px.box(
        df_melt,
        x='Visit Type',
        y='Count',
        color='Visit Type',
        color_discrete_sequence=['#002f7a', '#509beb', '#1f62b7'],
        title='Distribution of Unique, First-Time, and Returning Visits'
    )
    fig.update_layout(
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        font_color='#fdfefe',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

import plotly.subplots as sp

def plot_acf_pacf(data, nlags=30):
    ts = data.sort_values('Date').set_index('Date')['Unique_Visits']
    ts = ts.dropna()
    
    acf_vals = acf(ts, nlags=nlags, fft=False)
    pacf_vals = pacf(ts, nlags=nlags, method='ywm')
    lags = np.arange(len(acf_vals))
    
    # Create subplots
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=('ACF', 'PACF'))
    
    # ACF subplot
    fig.add_trace(go.Bar(
        x=lags,
        y=acf_vals,
        name=' ',
        marker_color='#002f7a'
    ), row=1, col=1)
    
    # PACF subplot
    fig.add_trace(go.Bar(
        x=lags,
        y=pacf_vals,
        name=' ',
        marker_color='#509beb'
    ), row=1, col=2)
    
    # Layout with two subplots
    fig.update_layout(
        title='Autocorrelation Function (ACF) and Partial (PACF)',
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        font_color='#fdfefe',
        showlegend=False,
        margin=dict(l=70, r=70, t=70, b=50)  # margin to avoid cutting labels
    )
    
    # Adjust axes
    fig.update_xaxes(title='Lag', title_font=dict(size=14), tickfont=dict(size=12), row=1, col=1)
    fig.update_yaxes(title='ACF', title_font=dict(size=14), tickfont=dict(size=12), autorange=True, title_standoff=10, ticks='outside', ticklen=5, row=1, col=1)
    
    fig.update_xaxes(title='Lag', title_font=dict(size=14), tickfont=dict(size=12), row=1, col=2)
    fig.update_yaxes(title='PACF', title_font=dict(size=14), tickfont=dict(size=12), autorange=True, title_standoff=10, ticks='outside', ticklen=5, row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)

def plot_distribution_kde(data):
    fig = px.histogram(
        data,
        x='Unique_Visits',
        nbins=30,
        marginal='rug',
        histnorm='density',
        title='Distribution and KDE of Unique Visits',
        color_discrete_sequence=['#1f62b7']
    )
    fig.update_layout(
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        font_color='#fdfefe'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_violin(data):
    fig = px.violin(
        data,
        x='Day',
        y='Unique_Visits',
        labels={'Unique_Visits': 'Unique Visits', 'Day': 'Date'},
        box=True,
        points='all',
        color='Day',
        title='Distribution of Unique Visits by Day of the Week (Violin Plot)',
        color_discrete_sequence=['#002f7a', '#114898', '#1f62b7', '#2b7ed7', '#509beb', '#7bbbf2', '#9ddbf9']
    )
    fig.update_layout(
        template='plotly_white',
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        font_color='#fdfefe',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_moving_average(data, window=7):
    df = data.sort_values('Date')
    df['Moving_Avg'] = df['Unique_Visits'].rolling(window=window).mean()
    fig = px.line(
        df,
        x='Date',
        y=['Unique_Visits', 'Moving_Avg'],
        labels={'value': 'Count', 'variable': 'Metric', 'Date': 'Date'},
        title=f'Moving Average ({window} days) of Unique Visits',
        color_discrete_sequence=['#002f7a', '#509beb']
    )
    fig.update_layout(
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        font_color='#fdfefe',
        legend=dict(bgcolor='rgba(252, 255, 255, 0)', bordercolor='#fdfefe', borderwidth=1),
    )
    fig.update_traces(mode='lines+markers')
    st.plotly_chart(fig, use_container_width=True)

def plot_forecast(data: pd.DataFrame, days: int):
    df = data.copy()
    df = df.sort_values('Date')
    df.set_index('Date', inplace=True)

    last_date = df.index.max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)

    series_list = ['First_Time_Visits', 'Returning_Visits']
    forecasts = {}

    for col in series_list:
        ts = df[col].dropna()
        model = ARIMA(ts, order=(5,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=days)
        # Create DataFrame with dates and forecasted values
        forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast.values})
        # Extract day of the week in text (e.g., Monday, Tuesday)
        forecast_df['DayOfWeek'] = forecast_df['Date'].dt.day_name(locale='en_US')  # English

        # Calculate average by day of the week
        avg_by_day = forecast_df.groupby('DayOfWeek')['Forecast'].mean()
        
        # Order days of the week in natural order Monday to Sunday
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        avg_by_day = avg_by_day.reindex([d.capitalize() for d in days_order])
        forecasts[col] = avg_by_day.fillna(0).values.tolist()

    categories = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig = go.Figure()

    for col, color in zip(series_list, ['#002f7a', '#509beb']):
        values = forecasts[col]
        values.append(values[0])  # close polygon
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=col.replace('_', ' '),
            line=dict(color=color)
        ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(252, 255, 255, 0)',
            radialaxis=dict(
                visible=True,
                color='#fdfefe',
                gridcolor='#7bbbf2'
            ),
            angularaxis=dict(
                tickfont=dict(color='#fdfefe')
            )
        ),
        plot_bgcolor='rgba(252, 255, 255, 0)',
        paper_bgcolor='rgba(252, 255, 255, 0)',
        font_color='#fdfefe',
        title=f'Radar Forecast by Day of the Week - Next {days} Days',
        legend=dict(bgcolor='rgba(252, 255, 255, 0)', bordercolor='#fdfefe', borderwidth=1),
        margin=dict(l=50, r=50, t=70, b=50),
        height=500,
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)
