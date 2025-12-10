import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import math
from statsmodels.tsa.seasonal import seasonal_decompose

# ------------------------------------------------
# PAGE CONFIG (ONLY ONE TIME)
# ------------------------------------------------
st.set_page_config(page_title="Pemchip Infotech Visualization", layout="wide")

# ------------------------------------------------
# BACKGROUND APPLY FUNCTION
# ------------------------------------------------
def set_background(url):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# PAGE STATE
# ------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# ------------------------------------------------
# FUNCTIONS
# ------------------------------------------------
def go_to_main():
    st.session_state.page = "main"
    #st.experimental_rerun()
    st.session_state["page"] = "main"
    

def save_user_data(name, contact):
    """Save user details to user.json file."""
    user_data = {
        "name": name,
        "contact": contact
    }
    with open("user.json", "w") as f:
        json.dump(user_data, f)
    st.success("User data saved successfully!")

# ------------------------------------------------
# WELCOME PAGE
# ------------------------------------------------
if st.session_state.page == "welcome":

    # Background for welcome page
    set_background("https://content.presentermedia.com/files/clipart/00032000/32823/data_visualization_background_800_wht.jpg")

    # Logo
    logo_url = "https://www.pemchip.com/html/img/logo_trans.png"
    st.markdown(
        f"""
        <div style='text-align:center; margin-top:40px;'>
            <img src='{logo_url}' width='180'>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Title
    st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <h1 style="color:black; font-size:98px;">Welcome to</h1>
            <h1 style="color:black; font-size:92px;">Pemchip Infotech</h1>
            <h3 style="color:black; font-size:52px;">Visualization Webinar</h3>
        </div>
    """, unsafe_allow_html=True)

    # Center button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Let's Start", use_container_width=True):
            st.session_state.show_form = True

    # -----------------------------
    # Popup Form Simulation
    # -----------------------------
    if st.session_state.show_form:
        with st.form("user_info_form", clear_on_submit=False):
            st.markdown("<h3 style='color:white;'>Please enter your details:</h3>", unsafe_allow_html=True)
            name = st.text_input("Full Name")
            contact = st.text_input("Contact Number")
            submitted = st.form_submit_button("Submit")

            if submitted:
                if name.strip() == "" or contact.strip() == "":
                    st.error("Please enter both Name and Contact Number.")
                else:
                    st.session_state.user_name = name
                    st.session_state.user_contact = contact
                    save_user_data(name, contact)
                    st.success(f"Welcome, {name}! Redirecting to main page...")
                    go_to_main()

    st.stop()

# ------------------------------------------------
# MAIN PAGE
# ------------------------------------------------
# Background for MAIN page
set_background("https://img.freepik.com/premium-vector/light-cyberspace-digital-background-vector-abstract-technology-white-wave-with-motion-dots_1168175-67.jpg?semt=ais_se_enriched&w=740&q=80")


st.title("🌈 Advanced & Colorful Data Visualization App")

# ---------------------------
# Load CSV or Sample
# ---------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
use_sample = st.button("Use Sample Dataset")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded!")

elif use_sample:
    np.random.seed(42)
    df = pd.DataFrame({
        "Category": np.random.choice(['A','B','C','D'], 100),
        "Value1": np.random.randint(10, 100, 100),
        "Value2": np.random.randint(20, 200, 100),
        "Score": np.random.randn(100)*10 + 50,
        "Description": np.random.choice(
            ["AI","Data","Python","Streamlit","Visualization","Plotly","Machine Learning"], 100
        )
    })
    st.success("Sample dataset loaded!")

else:
    st.warning("Upload CSV or use sample dataset")
    st.stop()

numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
text_cols = df.select_dtypes(include=['object','string']).columns.tolist()
all_cols = df.columns.tolist()

#st.write("### Columns in Dataset:")
#st.write(all_cols)


# ---------------------------------------
# SIDEBAR MENU
# ---------------------------------------
vis_type = st.sidebar.selectbox("Select Visualization", [
    "Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram",
    "Word Cloud", "Heatmap", "Radar Chart", "3D Scatter", "Animated Bubble",
    "Gauge", "Treemap", "Sunburst", "Sankey Diagram", "Parallel Coordinates",
    "Dumbbell Chart", "Slope Chart"
])


# ---------------------------------------
# CHARTS SECTION
# ---------------------------------------

# HELPERS
def ensure_date_series(df):
    for c in df.columns:
        try:
            s = pd.to_datetime(df[c], errors="ignore")
            if s.notna().sum() > 0:
                return s
        except:
            continue
    return pd.date_range(start="2024-01-01", periods=len(df), freq="D")

# --------------------------- BASIC CHARTS ---------------------------

if vis_type == "Bar Chart":
    x_col = st.selectbox("X Axis", all_cols)
    y_col = st.selectbox("Y Axis", numeric_cols)
    if st.button("Generate"):
        fig = px.bar(df, x=x_col, y=y_col, color=x_col,
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     title="🌈 Colorful Bar Chart")
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Line Chart":
    x_col = st.selectbox("X Axis", numeric_cols)
    y_col = st.selectbox("Y Axis", numeric_cols)
    grp = st.selectbox("Group By", [None] + all_cols)
    if st.button("Generate"):
        if grp:
            fig = px.line(df, x=x_col, y=y_col, color=grp,
                          color_discrete_sequence=px.colors.qualitative.Plotly)
        else:
            fig = px.line(df, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Scatter Plot":
    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols)
    color = st.selectbox("Color By", [None] + all_cols)
    size = st.selectbox("Size By", [None] + numeric_cols)
    if st.button("Generate"):
        fig = px.scatter(df, x=x, y=y, color=color, size=size,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Pie Chart":
    n = st.selectbox("Name", all_cols)
    v = st.selectbox("Value", numeric_cols)
    if st.button("Generate"):
        fig = px.pie(df, names=n, values=v,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Histogram":
    col = st.selectbox("Column", numeric_cols)
    if st.button("Generate"):
        fig = px.histogram(df, x=col, nbins=20, color=col,
                           color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Word Cloud":
    if len(text_cols) == 0:
        st.warning("No text column available.")
    else:
        col = st.selectbox("Text Column", text_cols)
        if st.button("Generate"):
            wc = WordCloud(width=900, height=400, background_color='white',
                           colormap='rainbow').generate(" ".join(df[col].astype(str)))
            fig, ax = plt.subplots(figsize=(12,5))
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)

elif vis_type == "Heatmap":
    if len(numeric_cols) >= 2:
        if st.button("Generate"):
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr, text_auto=True, color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("At least 2 numeric columns required.")


# --------------------------- ADVANCED CHARTS ---------------------------

elif vis_type == "Radar Chart":
    cols = st.multiselect("Select Columns", numeric_cols)
    if st.button("Generate"):
        vals = df[cols].mean()
        fig = go.Figure(go.Scatterpolar(r=vals, theta=cols, fill="toself"))
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "3D Scatter":
    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols)
    z = st.selectbox("Z Axis", numeric_cols)
    color = st.selectbox("Color", [None] + all_cols)
    if st.button("Generate"):
        fig = px.scatter_3d(df, x=x, y=y, z=z, color=color)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Animated Bubble":
    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols)
    size = st.selectbox("Size", numeric_cols)
    frame = st.selectbox("Frame", [None] + numeric_cols)
    if st.button("Generate"):
        temp = df.reset_index().rename(columns={"index":"frame"})
        anim = frame if frame else "frame"
        fig = px.scatter(temp, x=x, y=y, size=size, animation_frame=anim, color=x)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Gauge":
    col = st.selectbox("Metric", numeric_cols)
    if st.button("Generate"):
        avg = df[col].mean()
        fig = go.Figure(go.Indicator(mode="gauge+number", value=avg))
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Treemap":
    path = st.multiselect("Hierarchy", all_cols)
    v = st.selectbox("Value", numeric_cols)
    if st.button("Generate"):
        fig = px.treemap(df, path=path, values=v)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Sunburst":
    path = st.multiselect("Hierarchy", all_cols)
    v = st.selectbox("Value", numeric_cols)
    if st.button("Generate"):
        fig = px.sunburst(df, path=path, values=v)
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Sankey Diagram":
    src = st.selectbox("Source", all_cols)
    tgt = st.selectbox("Target", all_cols)
    val = st.selectbox("Value", numeric_cols)
    if st.button("Generate"):
        df_s = df.groupby([src, tgt])[val].sum().reset_index()
        labels = list(set(df_s[src].tolist() + df_s[tgt].tolist()))
        lbl_map = {v:i for i,v in enumerate(labels)}
        fig = go.Figure(go.Sankey(
            node=dict(label=labels),
            link=dict(
                source=df_s[src].map(lbl_map),
                target=df_s[tgt].map(lbl_map),
                value=df_s[val]
            )
        ))
        st.plotly_chart(fig, use_container_width=True)

elif vis_type == "Parallel Coordinates":
    cols = st.multiselect("Select Columns", numeric_cols)
    if st.button("Generate"):
        fig = px.parallel_coordinates(df[cols])
        st.plotly_chart(fig)

elif vis_type == "Dumbbell Chart":
    cat = st.selectbox("Category", all_cols)
    v1 = st.selectbox("Value 1", numeric_cols)
    v2 = st.selectbox("Value 2", numeric_cols)
    if st.button("Generate"):
        tmp = df[[cat, v1, v2]].dropna()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tmp[v1], y=tmp[cat], mode="markers"))
        fig.add_trace(go.Scatter(x=tmp[v2], y=tmp[cat], mode="markers"))
        st.plotly_chart(fig)

elif vis_type == "Slope Chart":
    left = st.selectbox("Left", numeric_cols)
    right = st.selectbox("Right", numeric_cols)
    label = st.selectbox("Label", all_cols)
    if st.button("Generate"):
        tmp = df[[label, left, right]]
        fig = go.Figure()
        for _, row in tmp.iterrows():
            fig.add_trace(go.Scatter(x=[0,1], y=[row[left], row[right]],
                                     text=[row[label]]))
        st.plotly_chart(fig)
