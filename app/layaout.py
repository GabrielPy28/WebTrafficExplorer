import streamlit as st
import datetime
import pandas as pd
from typing import Callable
from babel.dates import format_date

def generate_layout(
    data: pd.DataFrame,
    plot_heatmap: Callable,
    plot_boxplot: Callable,
    plot_forecast: Callable,
    plot_acf_pacf: Callable,
    plot_violin: Callable,
    plot_moving_average: Callable
):
    
    st.markdown(
        """
        <style>
        .main {
            color: #fcffff;
        }

        ul, p {
            color: #fcffff;
        }

        .appview-container {
            min-height: 100vh;
            height: 100%;            
            background-image: linear-gradient(to top, #09203f 0%, #537895 100%);
            background-blend-mode: multiply,multiply;
            background-color: #fcffff !important;
            color: #082338 !important;
            background-size: cover;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #f7f9f9 !important;
        }
        .stDataFrame, .stTable {
            background: #7bbbf2 !important;
            border-radius: 10px;
            color: #082338 !important;
        }
        .stButton>button {
            background-color: #1f62b7 !important;
            color: #fcffff !important;
            border-radius: 5px;
        }
        .sidebar .sidebar-content {
            background: #072f4e !important;
            color: #fcffff !important;
        }
        .stNumberInput>div>input {
            background: #bcfdff !important;
            color: #082338 !important;
        }
        .stExpanderHeader {
            background: #509beb !important;
            color: #f7f9f9 !important;
        }
        hr {
            border: linear-gradient(197deg,rgba(247, 249, 250, 1) 0%, rgba(170, 172, 173, 0.86) 50%, rgba(182, 192, 194, 1) 100%);
        }
        /* Main insights cards */
        .insight-card {
            background: rgba(255,255,255,0.85);
            border-radius: 14px;
            padding: 18px 8px 18px 8px;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px #002f7a22;
            margin-bottom: 8px;
            color: #1c2833 !important;
        }
        .insight-card span.emoji {
            font-size: 2.2em;
        }
        .insight-card .main-value {
            font-size: 1.5em;
            font-weight: bold;
        }
        .insight-card .label {
            font-size: 1.1em;
            margin-bottom: 2px;
        }
        .insight-card .desc {
            font-size: 0.95em;
        }
        @media (max-width: 900px) {
            .element-container .stColumn {
                width: 100% !important;
                flex: unset !important;
                max-width: 100% !important;
            }
            .insight-card {
                min-height: 120px;
                margin-bottom: 12px;
            }
        }
        </>
        """,
        unsafe_allow_html=True
    )
    
    # Storytelling and general insights at the beginning with responsive cards
    max_day = data.loc[data['Unique_Visits'].idxmax()]
    min_day = data.loc[data['Unique_Visits'].idxmin()]
    avg_visits = int(data['Unique_Visits'].mean())
    trend = data['Unique_Visits'].rolling(7).mean().iloc[-1] - data['Unique_Visits'].rolling(7).mean().iloc[-8]
    trend_icon = '🔼' if trend > 0 else '🔽'
    trend_text = 'increased' if trend > 0 else 'decreased'

    col1, col2 = st.columns(2) 
    col3, col4 = st.columns(2)

    with col1:
        maximum_day = format_date(max_day['Date'], format='long', locale='en_US')
        st.markdown(f"""
        <div class='insight-card' style='background: linear-gradient(135deg, #6dd5ed, #2193b0); padding: 20px; border-radius: 12px; height: 200px;'>
            <span class='emoji' style='font-size:2.5rem;'>📈</span>
            <div class='label'><b>Record Day</b></div>
            <div>{maximum_day}</div>
            <div class='main-value' style='color:#ffffff; font-size: 2rem; font-weight: bold;'>{max_day['Unique_Visits']:,}</div>
            <div class='desc' style='color: #ffffff;'>unique visits</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        minimum_day = format_date(min_day['Date'], format='long', locale='en_US')
        st.markdown(f"""
        <div class='insight-card' style='background: linear-gradient(135deg, #ff758c, #ff7eb3); padding: 16px; border-radius: 12px; height: 200px;'>
            <span class='emoji' style='font-size:2rem;'>📉</span>
            <div class='label'><b>Lowest Day</b></div>
            <div>{minimum_day}</div>
            <div class='main-value' style='color:#ffffff; font-size: 1.5rem;'>{min_day['Unique_Visits']:,}</div>
            <div class='desc' style='color: #ffffff;'>unique visits</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='insight-card' style='background: linear-gradient(135deg, #fbc2eb, #a6c1ee); padding: 12px; border-radius: 12px; height: 200px;'>
            <span class='emoji' style='font-size:1.8rem;'>📊</span>
            <div class='label'><b>Daily Average</b></div>
            <div class='main-value' style='color:#1f62b7; font-size: 1.3rem;'>{avg_visits:,}</div>
            <div class='desc' style='color: #1f62b7;'>unique visits</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class='insight-card' style='background: linear-gradient(135deg, #ffecd2, #fcb69f); padding: 16px; border-radius: 12px; height: 200px;'>
            <span class='emoji' style='font-size:2rem;'>{trend_icon}</span>
            <div class='label'><b>Weekly Trend</b></div>
            <div class='main-value' style='color:#1f62b7; font-size: 1.5rem;'>{abs(int(trend)):,}</div>
            <div class='desc' style='color: #1f62b7;'>visits {trend_text} on average</div>
        </div>
        """, unsafe_allow_html=True)

    st.title("Web Traffic Analysis, Data Exploration and Forecasting")
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Heatmap")
        st.markdown("""
            The heatmap shows unique visits by day of the week and month. 
            Darker colors indicate a higher number of visits, allowing us to quickly identify 
            the days and months with the most activity. This information is crucial for planning marketing campaigns 
            and optimizing site content.
        """)
        plot_heatmap(data)
        st.markdown(f"""
            - The day with the highest traffic is usually **{data.groupby('Day_Name')['Unique_Visits'].mean().idxmax()}**.
            - The strongest month on average is **{data.groupby(data['Date'].dt.month_name().str.slice(stop=3))['Unique_Visits'].mean().idxmax()}**.
        """)

    with col2:
        st.subheader("Distribution (Boxplot)")     
        st.markdown("""
            The boxplot illustrates the distribution of unique visits, first-time and returning visits. 
            It allows us to observe the median, quartiles, and possible outliers in each category. 
            This visualization is useful for understanding variability in traffic and visitor loyalty.
        """)
        plot_boxplot(data)
        st.markdown(f"""
            - The median of unique visits is **{int(data['Unique_Visits'].median())}**.
            - The interquartile range is **{int(data['Unique_Visits'].quantile(0.75) - data['Unique_Visits'].quantile(0.25))}**.
        """)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("ACF and PACF")
    st.markdown("""
        The autocorrelation function (ACF) and partial autocorrelation function (PACF) help us identify 
        the relationship between observations at different points in time. 
        These tools are fundamental for time series analysis and for building predictive models.
    """)
    plot_acf_pacf(data)
    st.markdown(f"""
        - The first autocorrelation value is **{data['Unique_Visits'].autocorr():.2f}**.
    """)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("Analysis of Unique Visits Distribution by Day of the Week")
    with st.expander("Distribution and Violin Plot", expanded=True):
        st.markdown("""
            The violin plot complements the boxplot by showing the density of unique visits by day of the week. 
            This visualization allows us to see not only the median and quartiles but also how visits are distributed 
            throughout each day. Additionally, the moving average helps us smooth out fluctuations 
            and observe long-term patterns in traffic.
        """)
        plot_violin(data)
        plot_moving_average(data)
        st.markdown(f""" 
            - The day with the highest visit dispersion is **{data.groupby('Day_Name')['Unique_Visits'].std().idxmax()}**.

        """)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("Forecasting Future Visits to Optimize Strategies")
    with st.expander("Traffic Forecast", expanded=True):
        st.markdown("""
            In this section, we can predict the traffic of our website for the upcoming days. 
            By entering the number of days we wish to forecast, we will use an ARIMA model to 
            estimate future visits. This is useful for anticipating traffic spikes and preparing 
            appropriate strategies to handle site load.
        """)
        days = st.number_input(
            "**Number of days for forecast:**",
            min_value=1, max_value=90, value=30, step=1,
            help="Choose how many days ahead you want to predict"
        )
        plot_forecast(data, days)
        st.markdown(f"""            
            - The ARIMA model predicts the general traffic trend for the next {days} days.
        """)
    
    st.markdown("<hr>", unsafe_allow_html=True)

    st.header("Filtered Data")
    st.markdown("""
        Here you can see the filtered data that was used to generate the previous visualizations. 
        This table allows you to explore the data in detail and perform additional analyses if desired.
    """)
    data_frame = data[['Day', 'Day_Of_Week', 'Date', 'Page_Loads', 'Unique_Visits', 'First_Time_Visits', 'Returning_Visits', 'Month']]
    data_frame.columns = ['Day', 'Day of the Week', 'Date', 'Page Loads', 'Unique Visits', 'First Time Visits', 'Returning Visits', 'Month']
    data_frame['Date'] = pd.to_datetime(data_frame['Date']).dt.date
    styled_data = data_frame.style.set_table_attributes('style="width:100%; text-align: center; vertical-align: middle !important;"') \
        .set_properties(**{'text-align': 'center',' vertical-align': 'middle !important'}) \
        .set_caption("Filtered Data")
    st.dataframe(styled_data, hide_index=True, use_container_width=True)

    # Add the footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <footer style='text-align: center; padding: 20px;'>
            <h5 style='margin: 0;'>Gabriel Piñero</h5>
            <h6 style='margin: 0;'>Python Developer | Data Analyst</h6>
            <p style='margin: 10px 0;'>
                <a href='https://www.linkedin.com/in/gabriel-pi%C3%B1ero-a151321a9/' target='_blank' style='text-decoration: none; margin-right: 15px;'>
                    <span style='background: linear-gradient(135deg, #6dd5ed, #2193b0); padding: 5px 10px; border-radius: 5px;'>
                        <img src='https://img.icons8.com/ios-filled/50/ffffff/linkedin.png' alt='LinkedIn' style='vertical-align: middle; width: 24px; height: 24px;'/>
                    </span>
                </a>
                <a href='https://portfolio-web-python.netlify.app' target='_blank' style='text-decoration: none; margin-right: 15px;'>
                    <span style='background: linear-gradient(135deg, #6dd5ed, #2193b0); padding: 5px 10px; border-radius: 5px;'>
                        <img src='https://img.icons8.com/ios-filled/50/ffffff/domain.png' alt='Web Portfolio' style='vertical-align: middle; width: 24px; height: 24px;'/>
                    </span>
                </a>
                <a href='https://github.com/GabrielPy28' target='_blank' style='text-decoration: none;'>
                    <span style='background: linear-gradient(135deg, #6dd5ed, #2193b0); padding: 5px 10px; border-radius: 5px;'>
                        <img src='https://img.icons8.com/ios-filled/50/ffffff/github.png' alt='GitHub' style='vertical-align: middle; width: 24px; height: 24px;'/>
                    </span>
                </a>
            </p>
            <span style='margin: 0; color: #43CBFF;'>&copy; {} Gabriel Piñero. All rights reserved.</span>
        </footer>
    """.format(datetime.datetime.now().year), unsafe_allow_html=True)
