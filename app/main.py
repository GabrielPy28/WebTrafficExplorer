import streamlit as st
import pandas as pd
import datetime
from functions import (
    load_data,
    plot_heatmap,
    plot_boxplot,
    plot_forecast,
    plot_acf_pacf,
    plot_violin,
    plot_moving_average
)
from layaout import generate_layout

st.set_page_config(page_title="Dashboard de Tráfico Web", layout="wide")

START_DATE = pd.to_datetime("2014-09-14")
END_DATE = pd.to_datetime("2020-08-19")

start_date = st.date_input("Fecha de inicio", START_DATE.date(), max_value=datetime.date(2019, 9, 1))
end_date = st.date_input(label="Fecha de fin", value=END_DATE.date(), max_value=END_DATE.date())

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

if start_date > end_date:
    st.error("La fecha de inicio no puede ser mayor que la fecha de fin.")
    st.stop()

raw_data = load_data()
filtered_data = raw_data[(raw_data['Date'] >= start_date) & (raw_data['Date'] <= end_date)]

generate_layout(
    filtered_data,
    plot_heatmap,
    plot_boxplot,
    plot_forecast,
    plot_acf_pacf,
    plot_violin,
    plot_moving_average
)
