import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import io

# Load data
data = pd.read_csv(r"D:\Python\Guvi\EDA\EDA\depression_dataset.csv")

# Page config
st.set_page_config(page_title='Visualization of Depression Data', layout='wide')
st.title("Analysis of Depression Dataset")

# Sidebar filters
st.sidebar.header("Filter Data")

gender_options = ['All'] + data['Gender'].dropna().unique().tolist()
selected_gender = st.sidebar.multiselect("Select Gender(s)", options=gender_options, default=['All'])

# Apply filters
filtered_data = data.copy()

if 'All' not in selected_gender:
    filtered_data = filtered_data[filtered_data['Gender'].isin(selected_gender)]

# Download helpers
def get_image_download_link(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Markdown-style section selector
section = st.selectbox("Select Visualization Section", [
    "Age vs Depression Cases",
    "Gender vs Suicidal Thoughts",
    "KDE Plot of CGPA",
    "Dietary Habits Distribution",
    "Age vs Suicidal Thoughts",
    "Top 10 CGPA Cities (Pie Chart)",
    "Top 10 Cities - Depression Count",
    "Family History vs Depression"
])

if section == "Age vs Depression Cases":
    st.subheader(section)
    age_depression = filtered_data[filtered_data['Depression'] == 1].groupby(['Age'])['Depression'].count().reset_index()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=age_depression, x='Age', y='Depression', ax=ax)
    ax.set_title(section)
    ax.set_xlabel('Age')
    ax.set_ylabel('Number of Depression Cases')
    plt.xticks(rotation=55)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "age_vs_depression.png", "image/png")
    st.download_button("Download Data as CSV", convert_df_to_csv(age_depression), "age_vs_depression.csv", "text/csv")

elif section == "Gender vs Suicidal Thoughts":
    st.subheader(section)
    df = filtered_data.groupby(['Gender','Have you ever had suicidal thoughts ?']).size().reset_index(name='Count')
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=df, x='Gender', y='Count', hue='Have you ever had suicidal thoughts ?', ax=ax)
    ax.set_title(section)
    plt.xticks(rotation=55)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "gender_vs_thoughts.png", "image/png")
    st.download_button("Download Data as CSV", convert_df_to_csv(df), "gender_vs_thoughts.csv", "text/csv")

elif section == "KDE Plot of CGPA":
    st.subheader(section)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.kdeplot(filtered_data['CGPA'], fill=True, color='purple', ax=ax)
    ax.set_title(section)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "kde_cgpa.png", "image/png")

elif section == "Dietary Habits Distribution":
    st.subheader(section)
    counts = filtered_data['Dietary Habits'].value_counts()
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'], startangle=140, explode=[0.05]*len(counts), shadow=True)
    ax.set_title(section)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "dietary_habits.png", "image/png")

elif section == "Age vs Suicidal Thoughts":
    st.subheader(section)
    df = filtered_data.groupby(['Age','Have you ever had suicidal thoughts ?']).size().reset_index(name='count')
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=df, x='Age', y='count', hue='Have you ever had suicidal thoughts ?', ax=ax)
    ax.set_title(section)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "age_vs_suicidal_thoughts.png", "image/png")
    st.download_button("Download Data as CSV", convert_df_to_csv(df), "age_vs_suicidal_thoughts.csv", "text/csv")

elif section == "Top 10 CGPA Cities (Pie Chart)":
    st.subheader(section)
    df = filtered_data.groupby('City')['CGPA'].mean().reset_index()
    df = df.sort_values(by='CGPA', ascending=False).head(10)
    fig = px.pie(df, names='City', values='CGPA', title=section, hole=0.2)
    fig.update_traces(pull=[0.1]*10, textinfo='percent+label')
    st.plotly_chart(fig)
    st.download_button("Download Data as CSV", convert_df_to_csv(df), "top10_cgpa_cities.csv", "text/csv")

elif section == "Top 10 Cities - Depression Count":
    st.subheader(section)
    top_cities = filtered_data['City'].value_counts().head(10).index
    df = filtered_data[filtered_data['City'].isin(top_cities)]
    fig, ax = plt.subplots(figsize=(12,6))
    sns.countplot(x='City', hue='Depression', data=df, ax=ax, palette='viridis')
    ax.set_title(section)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "city_depression.png", "image/png")
    st.download_button("Download Data as CSV", convert_df_to_csv(df), "city_depression.csv", "text/csv")

elif section == "Family History vs Depression":
    st.subheader(section)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(x='Family History of Mental Illness', hue='Depression', data=filtered_data, ax=ax, palette='cubehelix')
    ax.set_title(section)
    st.pyplot(fig)
    st.download_button("Download Plot as PNG", get_image_download_link(fig), "family_history.png", "image/png")

