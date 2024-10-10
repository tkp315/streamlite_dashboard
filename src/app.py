import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Load the dataset
url = "https://drive.google.com/uc?id=16Jlpg04DTPbMiVlgPPjnngLpyXV7LZYK"
output = "data2.csv"

# Download the file using gdown
file = gdown.download(url, output, quiet=False)

if file:
    st.write(f"{file} downloaded successfully.")
else:
    st.write("File download failed.")

# Read the CSV file
df2 = pd.read_csv(output)
# st.write(df2.head()) 
# Add padding to the container
st.markdown('<style>div.block-container{padding-top:1rem}</style>', unsafe_allow_html=True)

# Title
st.markdown("""
    <div style="text-align: center; font-weight: bold; padding: 5px; border-radius: 6px;">
        <h1>Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# Search and filter
st.subheader("Search and Filter")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

# Search box
search_term = col1.text_input("Search by Repo Name", '')

# Sliders for stars, forks, and watchers
min_stars = col2.slider('Minimum Stars', min_value=int(df2['stars_count'].min()), max_value=int(df2["stars_count"].max()), value=int(df2["stars_count"].min()))
max_stars = col3.slider('Maximum Stars', min_value=int(df2['stars_count'].min()), max_value=int(df2["stars_count"].max()), value=int(df2["stars_count"].max()))

min_fork = col4.slider('Minimum Forks', min_value=int(df2['forks_count'].min()), max_value=int(df2["forks_count"].max()), value=int(df2["forks_count"].min()))
max_fork = col5.slider('Maximum Forks', min_value=int(df2['forks_count'].min()), max_value=int(df2["forks_count"].max()), value=int(df2["forks_count"].max()))

min_watchers = col6.slider('Minimum Watchers', min_value=int(df2['watchers'].min()), max_value=int(df2["watchers"].max()), value=int(df2["watchers"].min()))
max_watchers = col7.slider('Maximum Watchers', min_value=int(df2['watchers'].min()), max_value=int(df2["watchers"].max()), value=int(df2["watchers"].max()))

# Language filter
language_filter = st.selectbox('Primary Language', options=['All'] + list(df2['primary_language'].unique()))

# Clear filters button
if st.button("Clear Filters"):
    search_term = ''
    min_stars = int(df2['stars_count'].min())
    max_stars = int(df2['stars_count'].max())
    min_fork = int(df2['forks_count'].min())
    max_fork = int(df2['forks_count'].max())
    min_watchers = int(df2['watchers'].min())
    max_watchers = int(df2['watchers'].max())
    language_filter = 'All'

# Filter the data based on inputs
filtered_data = df2[
    (df2['name'].str.contains(search_term, case=False)) &
    (df2['stars_count'] >= min_stars) & (df2['stars_count'] <= max_stars) &
    (df2['forks_count'] >= min_fork) & (df2['forks_count'] <= max_fork) &
    (df2['watchers'] >= min_watchers) & (df2['watchers'] <= max_watchers)
]

# Apply the language filter
if language_filter != 'All':
    filtered_data = filtered_data[filtered_data['primary_language'] == language_filter]

# Table for filtered data
st.subheader("Complete Repository Table")
rows_per_page = st.selectbox("Select number of rows per page", options=[10, 20, 40, 80], index=1)

total_rows = filtered_data.shape[0]
total_pages = (total_rows + rows_per_page - 1) // rows_per_page

current_page = st.number_input("Select page number", min_value=1, max_value=total_pages, value=1)
start_index = (current_page - 1) * rows_per_page
end_index = start_index + rows_per_page

if total_rows > 0:
    st.dataframe(filtered_data.iloc[start_index:end_index])
else:
    st.write("No repositories found for the applied filters.")

# Title for Graphs and Visualizations
st.markdown("""
    <div style="text-align: center; font-weight: bold; padding: 5px; border-radius: 6px;">
        <h1>Graphs and Visualizations</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("Visualize Data with Graphs")

# Pagination for Graphs
graph_rows_per_page = st.selectbox("Select number of rows for graph per page", options=[50, 100, 200], index=1)
graph_total_rows = filtered_data.shape[0]
graph_total_pages = (graph_total_rows + graph_rows_per_page - 1) 

graph_current_page = st.number_input("Select graph page number", min_value=1, max_value=graph_total_pages, value=1)
graph_start_index = (graph_current_page - 1) * graph_rows_per_page
graph_end_index = graph_start_index + graph_rows_per_page

# Filtered data for graph pagination
filtered_graph_data = filtered_data.iloc[graph_start_index:graph_end_index]

# Bar chart for Stars
st.write('Repositories vs Stars')
fig1 = px.bar(filtered_graph_data, x='name', y='stars_count', title="Stars per Repository")
st.plotly_chart(fig1)

# Bar chart for Forks
st.write("Repositories vs Forks")
fig2 = px.bar(filtered_graph_data, x='name', y='forks_count', title="Forks per Repository")
st.plotly_chart(fig2)

# Pie chart for Primary Language distribution
st.write("Primary Language Distribution")
fig3 = px.pie(filtered_graph_data, names='primary_language', title="Primary Language Distribution")
st.plotly_chart(fig3)

# Line chart for Commit Count Over Time (if 'created_at' exists)
if 'created_at' in filtered_graph_data.columns:
    st.write("Commit Count Over Time")
    filtered_data_copy = filtered_graph_data.copy()  # Avoid modifying the original data
    filtered_data_copy['created_at'] = pd.to_datetime(filtered_data_copy['created_at'])
    fig4 = px.line(filtered_data_copy.sort_values('created_at'), x='created_at', y='commit_count', title='Commits Over Time')
    st.plotly_chart(fig4)
