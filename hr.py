
#Streamlit Setup
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Industrial Workforce Analysis",
    layout="wide"
)

st.title(" Industrial Workforce Analysis Dashboard")
st.markdown("Census 2011 – India Industrial Workforce Data")
#Load Cleaned Data
@st.cache_data
def load_data():
    return pd.read_csv("final_cleaned_data.csv")

df = load_data()
#Sidebar Filters
st.sidebar.header("🔎 Filters")

selected_state = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["state_name"].unique()),
    default=df["state_name"].unique()
)

selected_industry = st.sidebar.multiselect(
    "Select Industry Category",
    options=sorted(df["industry_category"].unique()),
    default=df["industry_category"].unique()
)

filtered_df = df[
    (df["state_name"].isin(selected_state)) &
    (df["industry_category"].isin(selected_industry))
]
#KPI Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Workforce", f"{int(filtered_df['total_workers'].sum()):,}")
col2.metric("Male Workers", f"{int(filtered_df['total_male_workers'].sum()):,}")
col3.metric("Female Workers", f"{int(filtered_df['total_female_workers'].sum()):,}")
col4.metric("States Covered", filtered_df["state_name"].nunique())
#Charts Section
# State-wise Workforce

state_df = (
    filtered_df.groupby("state_name", as_index=False)["total_workers"]
    .sum()
    .sort_values(by="total_workers", ascending=False)
)

fig_state = px.bar(
    state_df,
    x="state_name",
    y="total_workers",
    title="Total Workforce by State"
)

st.plotly_chart(fig_state, use_container_width=True)

#Industry-wise Distribution

industry_df = (
    filtered_df.groupby("industry_category", as_index=False)["total_workers"]
    .sum()
)

fig_industry = px.pie(
    industry_df,
    names="industry_category",
    values="total_workers",
    title="Workforce Distribution by Industry"
)

st.plotly_chart(fig_industry, use_container_width=True)

#Gender Distribution

gender_df = pd.DataFrame({
    "Gender": ["Male", "Female"],
    "Count": [
        filtered_df["total_male_workers"].sum(),
        filtered_df["total_female_workers"].sum()
    ]
})

fig_gender = px.bar(
    gender_df,
    x="Gender",
    y="Count",
    title="Gender-wise Workforce Distribution"
)

st.plotly_chart(fig_gender, use_container_width=True)


#Rural vs Urban Workforce

area_df = pd.DataFrame({
    "Area": ["Rural", "Urban"],
    "Count": [
        filtered_df["total_rural_workers"].sum(),
        filtered_df["total_urban_workers"].sum()
    ]
})

fig_area = px.pie(
    area_df,
    names="Area",
    values="Count",
    title="Rural vs Urban Workforce"
)

st.plotly_chart(fig_area, use_container_width=True)






