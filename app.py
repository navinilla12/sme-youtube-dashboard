import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & ENTERPRISE STYLING
# ==============================================================================
st.set_page_config(
    page_title="SME Media | YouTube Analytics Engine",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .header-card {
        background: #1E293B;
        padding: 1.2rem 1.8rem;
        border-radius: 6px;
        border-left: 4px solid #0284C7;
        margin-bottom: 1.5rem;
    }
    .header-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 0;
    }
    .header-subtitle {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA ENGINE (SME MEDIA YOUTUBE DATASET WITH DURATION METRICS)
# ==============================================================================
@st.cache_data
def load_sme_youtube_data():
    raw_data = [
        {
            "Video_ID": "AiH4rJoibhA",
            "Video_Title": "Advancing the Line - AI in Manufacturing: How Edge Computing Empowers Operators",
            "Publish_Day": "Thursday",
            "Publish_Date": "2026-10-08",
            "Views": 1420,
            "Likes": 184,
            "Watch_Time_Mins": 4210,
            "Avg_Duration_Sec": 224,
            "Min_Watch_Sec": 45,
            "Max_Watch_Sec": 480,
            "Total_Video_Duration_Min": 8.5,
            "Category": "AI & Automation",
            "Watch_Time_Tier": "Medium (3k-6k min)"
        },
        {
            "Video_ID": "e1U9aX_v3b4",
            "Video_Title": "What's Next for the Global A&D Market?",
            "Publish_Day": "Thursday",
            "Publish_Date": "2026-10-01",
            "Views": 2890,
            "Likes": 312,
            "Watch_Time_Mins": 8940,
            "Avg_Duration_Sec": 310,
            "Min_Watch_Sec": 60,
            "Max_Watch_Sec": 650,
            "Total_Video_Duration_Min": 11.2,
            "Category": "Aerospace & Defense",
            "Watch_Time_Tier": "High (>6k min)"
        },
        {
            "Video_ID": "f2G8bC_k4l5",
            "Video_Title": "Inside FANUC's Next-Gen Physical AI Innovations Live from IMTS",
            "Publish_Day": "Tuesday",
            "Publish_Date": "2026-09-29",
            "Views": 5410,
            "Likes": 620,
            "Watch_Time_Mins": 14200,
            "Avg_Duration_Sec": 280,
            "Min_Watch_Sec": 30,
            "Max_Watch_Sec": 720,
            "Total_Video_Duration_Min": 12.5,
            "Category": "Robotics & AI",
            "Watch_Time_Tier": "High (>6k min)"
        },
        {
            "Video_ID": "g3H9cD_m5n6",
            "Video_Title": "Manufacturing in Michigan: Conversation with Macomb County Executive Mark Hackel",
            "Publish_Day": "Thursday",
            "Publish_Date": "2026-09-24",
            "Views": 1150,
            "Likes": 95,
            "Watch_Time_Mins": 3100,
            "Avg_Duration_Sec": 195,
            "Min_Watch_Sec": 20,
            "Max_Watch_Sec": 390,
            "Total_Video_Duration_Min": 7.0,
            "Category": "Workforce & Leadership",
            "Watch_Time_Tier": "Medium (3k-6k min)"
        },
        {
            "Video_ID": "h4J0eE_n6o7",
            "Video_Title": "Advancing the Line - AI in Manufacturing: The Pilot Purgatory Problem",
            "Publish_Day": "Thursday",
            "Publish_Date": "2026-09-17",
            "Views": 3820,
            "Likes": 410,
            "Watch_Time_Mins": 11400,
            "Avg_Duration_Sec": 265,
            "Min_Watch_Sec": 50,
            "Max_Watch_Sec": 590,
            "Total_Video_Duration_Min": 10.0,
            "Category": "AI & Automation",
            "Watch_Time_Tier": "High (>6k min)"
        },
        {
            "Video_ID": "j5K1fF_o7p8",
            "Video_Title": "Simulate Before You Automate: Proven Method to Evaluate ROI & System Impact",
            "Publish_Day": "Thursday",
            "Publish_Date": "2026-09-10",
            "Views": 4200,
            "Likes": 490,
            "Watch_Time_Mins": 12800,
            "Avg_Duration_Sec": 290,
            "Min_Watch_Sec": 40,
            "Max_Watch_Sec": 610,
            "Total_Video_Duration_Min": 10.5,
            "Category": "Smart Manufacturing",
            "Watch_Time_Tier": "High (>6k min)"
        }
    ]
    df = pd.DataFrame(raw_data)
    df['Publish_Date'] = pd.to_datetime(df['Publish_Date'])
    df['Engagement_Rate_%'] = round((df['Likes'] / df['Views']) * 100, 2)
    return df

df_youtube = load_sme_youtube_data()

# ==============================================================================
# 3. HEADER & NAVIGATION
# ==============================================================================
st.markdown("""
<div class="header-card">
    <div class="header-subtitle">SME Digital Product Strategy & Analytics</div>
    <div class="header-title">YouTube Media Performance Dashboard</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Navigation & Filters")
st.sidebar.caption("Target: @SMEMedia Channel")

selected_categories = st.sidebar.multiselect(
    "Filter by Category:",
    options=df_youtube['Category'].unique(),
    default=df_youtube['Category'].unique()
)

selected_tiers = st.sidebar.multiselect(
    "Filter by Watch Time Category:",
    options=df_youtube['Watch_Time_Tier'].unique(),
    default=df_youtube['Watch_Time_Tier'].unique()
)

df_filtered = df_youtube[
    (df_youtube['Category'].isin(selected_categories)) & 
    (df_youtube['Watch_Time_Tier'].isin(selected_tiers))
]

video_options = ["Channel Overview (All Filtered Uploads)"] + list(df_filtered['Video_Title'].unique()) if not df_filtered.empty else ["Channel Overview (All Filtered Uploads)"]
selected_video = st.sidebar.selectbox("Select Video Record for Deep-Dive:", video_options)

# ==============================================================================
# 4. DASHBOARD VIEW CONTROLLER
# ==============================================================================

if selected_video != "Channel Overview (All Filtered Uploads)":
    video_data = df_filtered[df_filtered['Video_Title'] == selected_video].iloc[0]
    
    st.subheader(f"Content Analysis: {selected_video}")
    st.caption(f"Publication Date: {video_data['Publish_Date'].strftime('%B %d, %Y')} ({video_data['Publish_Day']}) | Category: {video_data['Category']} | Total Duration: {video_data['Total_Video_Duration_Min']} min")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Views", f"{video_data['Views']:,}")
    col2.metric("Total Likes", f"{video_data['Likes']:,}")
    col3.metric("Watch Time", f"{video_data['Watch_Time_Mins']:,} min")
    col4.metric("Avg View Duration", f"{video_data['Avg_Duration_Sec']} sec")
    
    st.markdown("##### Viewer Watch Time Depth (Min / Avg / Max)")
    w1, w2, w3 = st.columns(3)
    w1.metric("Minimum Watch Time", f"{video_data['Min_Watch_Sec']} sec")
    w2.metric("Average Watch Time", f"{video_data['Avg_Duration_Sec']} sec")
    w3.metric("Maximum Watch Time", f"{video_data['Max_Watch_Sec']} sec")
    
    st.markdown("---")
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("##### Video Asset Preview")
        st.video(f"https://www.youtube.com/watch?v={video_data['Video_ID']}")
    with c_right:
        st.markdown("##### Performance vs. Filtered Benchmark")
        bench_df = pd.DataFrame({
            "Metric": ["Views", "Watch Time (Mins)", "Likes x10"],
            "Selected Video": [video_data['Views'], video_data['Watch_Time_Mins'], video_data['Likes'] * 10],
            "Filtered Average": [df_filtered['Views'].mean(), df_filtered['Watch_Time_Mins'].mean(), df_filtered['Likes'].mean() * 10]
        })
        fig_bench = px.bar(
            bench_df, x="Metric", y=["Selected Video", "Filtered Average"], barmode="group",
            color_discrete_sequence=["#0284C7", "#64748B"], template="plotly_dark"
        )
        fig_bench.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=280, 
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color="#F8FAFC", size=12))
        )
        st.plotly_chart(fig_bench, use_container_width=True)

else:
    # --- CHART SELECTION INTERACTION ENGINE ---
    display_df = df_filtered.copy()
    
    # Calculate initial KPI values
    total_views = int(display_df['Views'].sum()) if not display_df.empty else 0
    total_watch = int(display_df['Watch_Time_Mins'].sum()) if not display_df.empty else 0
    total_likes = int(display_df['Likes'].sum()) if not display_df.empty else 0
    avg_eng = round(display_df['Engagement_Rate_%'].mean(), 2) if not display_df.empty else 0.0

    st.markdown("### Executive Channel Summary")
    
    # Placeholder for Dynamic KPI updates
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    kpi_col1.metric("Catalog Views", f"{total_views:,}")
    kpi_col2.metric("Total Watch Time", f"{total_watch:,} mins")
    kpi_col3.metric("Engagement Likes", f"{total_likes:,}")
    kpi_col4.metric("Avg Engagement Rate", f"{avg_eng}%")
    
    st.markdown("---")
    
    if display_df.empty:
        st.warning("No records match your selected filter criteria. Please adjust your sidebar filters.")
    else:
        col_a, col_b = st.columns([3, 2])
        
        # Chart 1: Views by Video Title (High contrast legend)
        with col_a:
            st.markdown("##### Views by Video Title (Click a bar to filter / click empty space to reset)")
            fig_views = px.bar(
                display_df, x="Video_Title", y="Views", color="Category", 
                template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_views.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                height=350, xaxis=dict(showticklabels=False), margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#F8FAFC", size=12), title=dict(font=dict(color="#38BDF8", size=13)))
            )
            selected_bar = st.plotly_chart(fig_views, use_container_width=True, on_select="rerun", selection_mode="points")
            
        # Chart 2: Watch Time Share by Category (High contrast legend)
        with col_b:
            st.markdown("##### Watch Time Share by Category (Click a slice to filter / click empty space to reset)")
            fig_pie = px.pie(
                display_df, names="Category", values="Watch_Time_Mins", hole=0.5, 
                template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#F8FAFC", size=12), title=dict(font=dict(color="#38BDF8", size=13)))
            )
            selected_pie = st.plotly_chart(fig_pie, use_container_width=True, on_select="rerun", selection_mode="points")
            
        # Handle empty space deselection to restore original dataset
        active_filter_df = display_df.copy()
        if selected_bar and "selection" in selected_bar and selected_bar["selection"]["points"]:
            point = selected_bar["selection"]["points"][0]
            clicked_title = point.get("x")
            if clicked_title:
                active_filter_df = active_filter_df[active_filter_df["Video_Title"] == clicked_title]
        elif selected_pie and "selection" in selected_pie and selected_pie["selection"]["points"]:
            point = selected_pie["selection"]["points"][0]
            clicked_category = point.get("label")
            if clicked_category:
                active_filter_df = active_filter_df[active_filter_df["Category"] == clicked_category]

        st.markdown("---")
        
        # NEW ROW: Likes Visual & Retention Depth Visual
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.markdown("##### Audience Likes by Video Title")
            fig_likes = px.bar(
                active_filter_df, y="Video_Title", x="Likes", color="Category",
                orientation="h", template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_likes.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, yaxis=dict(showticklabels=False), margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#F8FAFC", size=11))
            )
            st.plotly_chart(fig_likes, use_container_width=True)
            
        with col_d:
            st.markdown("##### Viewer Retention Depth (Avg vs Max Watch Time in Sec)")
            fig_retention = go.Figure()
            fig_retention.add_trace(go.Bar(
                x=active_filter_df['Video_Title'], y=active_filter_df['Avg_Duration_Sec'],
                name='Avg Watch Duration (Sec)', marker_color='#0284C7'
            ))
            fig_retention.add_trace(go.Bar(
                x=active_filter_df['Video_Title'], y=active_filter_df['Max_Watch_Sec'],
                name='Max Watch Duration (Sec)', marker_color='#38BDF8'
            ))
            fig_retention.update_layout(
                barmode='group', template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, xaxis=dict(showticklabels=False), margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#F8FAFC", size=11))
            )
            st.plotly_chart(fig_retention, use_container_width=True)

        st.markdown("##### Granular Content Records")
        st.dataframe(
            active_filter_df[['Video_Title', 'Category', 'Total_Video_Duration_Min', 'Watch_Time_Tier', 'Publish_Day', 'Views', 'Likes', 'Watch_Time_Mins', 'Avg_Duration_Sec', 'Max_Watch_Sec']], 
            use_container_width=True, 
            hide_index=True
        )