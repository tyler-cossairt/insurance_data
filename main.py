from matplotlib.pyplot import plot
from numpy import size
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel('insurance.xlsx')

st.title('Healthcare Costs Analysis')

st.sidebar.title('Filters')

# Sidebar - Age range slider
age_min = int(df['age'].min())
age_max = int(df['age'].max())
age_slider = st.sidebar.slider('Select your age range', age_min, age_max, (age_min, age_max))

# Sidebar - BMI range slider
bmi_min = int(df['bmi'].min())
bmi_max = int(df['bmi'].max())
bmi_slider = st.sidebar.slider('Select your BMI range', bmi_min, bmi_max, (bmi_min, bmi_max))

#Sidebar - Smoker filter
#smoker_status_filter = st.sidebar.radio('Select smoking status', ['All', 'Yes', 'No'])

#Sidebar - Region filter
#region_filter = st.sidebar.radio('Select region', ['All', 'Northeast', 'Northwest', 'Southeast', 'Southwest'])



# Apply filters to the DataFrame
filtered_df = df[
    (df['age'].between(age_slider[0], age_slider[1])) &
    (df['bmi'].between(bmi_slider[0], bmi_slider[1]))
]


# Recalculate groupings based on filtered DataFrame
grouped_data = filtered_df.groupby(['sex', 'region'])['charges'].sum().reset_index()
regional_costs = filtered_df.groupby(['region'])['charges'].sum().reset_index()
smoker_grouped_data = filtered_df.groupby(['smoker', 'sex']).agg({'charges': 'mean'}).reset_index()



# Visualizations
st.container()
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Costs by Region and Sex')
    st.write(grouped_data)

with col2:
    st.write('Total Costs by Region')
    st.write(regional_costs)

with col3:
    st.write("Average Costs by Smoking Status and Gender")
    st.write(smoker_grouped_data)

st.container()
left_col, right_col = st.columns(2)
with left_col:
    fig_gender_smoker = px.bar(filtered_df.groupby(['sex', 'smoker'])['charges'].sum().reset_index(),
                               x='smoker', y='charges', color='sex',
                               title="Comparison Cost Analysis by Gender and Smoking Status",
                               labels={'charges': 'Total Charges', 'smoker': 'Smoker Status'})
    fig_gender_smoker.update_layout(xaxis_title="Smoker Status", yaxis_title="Total Charges")
    st.plotly_chart(fig_gender_smoker)

with right_col:
    fig_gender_region = px.bar(filtered_df.groupby(['sex', 'region'])['charges'].sum().reset_index(),
                               x='region', y='charges', color='sex',
                               title="Comparison Cost Analysis by Gender and Region",
                               labels={'charges': 'Total Charges', 'region': 'Region'})
    fig_gender_region.update_layout(xaxis_title="Region", yaxis_title="Total Charges")
    st.plotly_chart(fig_gender_region)

# Scatter plot with Plotly
fig = px.scatter(filtered_df, x='age', y='charges', color='smoker',
                 hover_data=['age', 'charges', 'smoker', 'sex'],
                 labels={'charges': 'Charges'},
                 title="Costs by Age of Patient and Smoking Status",
                 template='plotly')
st.plotly_chart(fig)
