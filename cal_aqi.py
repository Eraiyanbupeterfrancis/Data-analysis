import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"
#exploring the given dataset
data=pd.read_csv('delhiaqi.csv')

a=go.Figure()
for pollutant in ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']:
    a.add_trace(go.Scatter(x=data['date'],y=data[pollutant],mode='lines',name=pollutant))
a.update_layout(title="Delhi Air quality index",xaxis_title="Date",yaxis_title="Air quality index")
a.show()
data['date']=pd.to_datetime(data['date'])
#defining AQI breakpoints
aqi_breakpoints = [
    (0, 12.0, 50), (12.1, 35.4, 100), (35.5, 55.4, 150),
    (55.5, 150.4, 200), (150.5, 250.4, 300), (250.5, 350.4, 400),
    (350.5, 500.4, 500)
]
#calculating AQI for each pollutant
def calculate_aqi(pollutant_name, concentration):
    for low, high, aqi in aqi_breakpoints:
        if low <= concentration <= high:
            return aqi
    return None
#calculating AQI for each row
def calculate_overall_aqi(row):
    aqi_val=[]
    pollutants=['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']
    for pollutant in pollutants:
       aqi = calculate_aqi(pollutant, row[pollutant])
       if aqi is not None:
            aqi_val.append(aqi)
    return max(aqi_val)
data['AQI'] = data.apply(calculate_overall_aqi, axis=1)
aqi_categories = [(0, 50, 'Good'), (51, 100, 'Moderate'), (101, 150, 'Unhealthy for Sensitive Groups'),
    (151, 200, 'Unhealthy'), (201, 300, 'Very Unhealthy'), (301, 500, 'Hazardous')]
def categorize_aqi(aqi_value):
    for low, high, category in aqi_categories:
        if low <= aqi_value <= high:
            return category
    return None
data['AQI Category'] = data['AQI'].apply(categorize_aqi)
print(data.head())


#Analyzing AQI of Delhi City

a=px.bar(data,x="date",y="AQI",title="Air quality index of delhi in jan")
a.update_xaxes(title="DATE")
a.update_yaxes(title="AQI")
a.show()
#aqi distribution in delhi

a= px.histogram(data, x="date", 
                    color="AQI Category", 
                    title="AQI Category Distribution Over Time")
a.update_xaxes(title="Date")
a.update_yaxes(title="Count")
a.show()
#pollutants distribution using pie chart
pollutants = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
pollutant_colors = px.colors.qualitative.Plotly


total_concentrations = data[pollutants].sum()


concentration_data = pd.DataFrame({
    "Pollutant": pollutants,
    "Concentration": total_concentrations
})


a = px.pie(concentration_data, names="Pollutant", values="Concentration",
             title="Pollutant Concentrations in Delhi",
             hole=0.4, color_discrete_sequence=pollutant_colors)

a.update_traces(textinfo="percent+label")
a.update_layout(legend_title="Pollutant")
a.show()
#air quality index vs hour
data['Hour'] = pd.to_datetime(data['date']).dt.hour


hourly_avg_aqi = data.groupby('Hour')['AQI'].mean().reset_index()


a = px.line(hourly_avg_aqi, x='Hour', y='AQI', 
              title='Hourly Average AQI Trends in Delhi (Jan 2023)')
a.update_xaxes(title="Hour of the Day")
a.update_yaxes(title="Average AQI")
a.show()

# Average AQI by Day of the Week
data['Day_of_Week'] = data['date'].dt.day_name()
average_aqi_by_day = data.groupby('Day_of_Week')['AQI'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
a = px.bar(average_aqi_by_day, x=average_aqi_by_day.index, y='AQI', 
              title='Average AQI by Day of the Week')
a.update_xaxes(title="Day of the Week")
a.update_yaxes(title="Average AQI")
a.show()
