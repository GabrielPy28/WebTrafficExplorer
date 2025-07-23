# Web Traffic Analysis: Data Exploration and Forecasting

The purpose of the Web Traffic Analysis project is to provide a comprehensive tool for analyzing and forecasting web traffic data from an educational website. By leveraging exploratory data analysis (EDA) techniques and advanced forecasting models, this project aims to uncover insights into visitor behavior, identify trends over time, and predict future traffic patterns. This information is crucial for webmasters and marketers to optimize their strategies, enhance user engagement, and effectively allocate resources based on anticipated traffic fluctuations.

> [!NOTE]  
> **Estado del Proyecto:**  
> El proyecto está publicado y disponible para su visualización en: [Web Traffic Explorer](https://webtrafficexplorer-e8nsb3hvp6kyknspboaxqh.streamlit.app)

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Statsmodels
- babel

## Dataset Description

The dataset contains 5 years of daily time series data on the traffic of an educational website. The variables include:

- **Page_Loads**: Daily number of pages loaded.
- **Unique_Visits**: Daily number of unique visitors.
- **First_Time_Visits**: Number of unique visitors who do not have an identifying cookie.
- **Returning_Visits**: Number of unique visitors minus first-time visitors.
- **Date**: The date of the recorded traffic data.
- **Day**: The day of the week corresponding to the date.
- **Day_Of_Week**: Numeric representation of the day of the week.
- **Month**: The month corresponding to the date.

## Analysis and Visualizations

### The project includes:
- Exploratory Data Analysis (EDA) to visualize traffic trends over time.
- Forecasting models to predict future traffic using ARIMA.
- Comparison of the behavior of returning and new visitors.
- Interactive visualizations including heatmaps, boxplots, violin plots, and moving averages.
- Autocorrelation and partial autocorrelation analysis to understand time series relationships.

## Installation

To install the project dependencies, run the following command:

```bash
pip install -r requirements.txt
```

