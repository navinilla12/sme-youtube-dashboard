import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & LIGHT EXECUTIVE CORPORATE STYLING
# ==============================================================================
st.set_page_config(
    page_title="SME Media | YouTube Analytics Engine",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .header-card {
        background: #FFFFFF;
        padding: 1.2rem 1.8rem;
        border-radius: 8px;
        border-left: 5px solid #0284C7;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .header-subtitle {
        font-size: 0.85rem;
        color: #0284C7;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        padding: 16px !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetricValue"] {
        color: #0284C7 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATA ENGINE (SME MEDIA YOUTUBE SAMPLE DATASET WITH UPLOAD TIMESTAMP)
# ==============================================================================
@st.cache_data
def load_sme_youtube_data():
    raw_data = [
        {
            "Video_ID": "AiH4rJoibhA",
            "Video_Title": "Advancing the Line - AI in Manufacturing: How Edge Computing Empowers Operators",
            "Publish_Day": "Thursday",
            "Publish_Timestamp": "2026-10-08 14:30:00",
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
            "Publish_Timestamp": "2026-10-01 10:15:00",
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
            "Publish_Timestamp": "2026-09-29 09:00:00",
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
            "Publish_Timestamp": "2026-09-24 15:45:00",
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
            "Publish_Timestamp": "2026-09-17 11:30:00",
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
            "Publish_Timestamp": "2026-09-10 12:00:00",
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
    df['Publish_Timestamp'] = pd.to_datetime(df['Publish_Timestamp'])
    df['Publish_Date_Only'] = df['Publish_Timestamp'].dt.date
    # Combined formatted column displaying both date and time (e.g., Oct 08, 2026 - 14:30)
    df['Publish_Date_Time'] = df['Publish_Timestamp'].dt.strftime('%b %d, %Y - %H:%M')
    df['Engagement_Rate_%'] = round((df['Likes'] / df['Views']) * 100, 2)
    return df

df_youtube = load_sme_youtube_data()

# ==============================================================================
# 3. MAIN TITLE CARD (TOP OF PAGE)
# ==============================================================================
st.markdown("""
<div class="header-card">
    <div class="header-subtitle">SME Digital Product Strategy & Analytics</div>
    <div class="header-title">YouTube Media Performance Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. SIDEBAR FILTERS
# ==============================================================================
st.sidebar.markdown("### Navigation & Filters")
st.sidebar.caption("Target: @SMEMedia Channel")

st.sidebar.markdown("#### Timeline Filter")
min_date = df_youtube['Publish_Date_Only'].min()
max_date = df_youtube['Publish_Date_Only'].max()

date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

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

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df_filtered = df_youtube[
    (df_youtube['Publish_Date_Only'] >= start_date) &
    (df_youtube['Publish_Date_Only'] <= end_date) &
    (df_youtube['Category'].isin(selected_categories)) & 
    (df_youtube['Watch_Time_Tier'].isin(selected_tiers))
]

video_options = ["Channel Overview (All Filtered Uploads)"] + list(df_filtered['Video_Title'].unique()) if not df_filtered.empty else ["Channel Overview (All Filtered Uploads)"]
selected_video = st.sidebar.selectbox("Select Video Record for Deep-Dive:", video_options)

# ==============================================================================
# 5. DASHBOARD VIEW CONTROLLER
# ==============================================================================

if selected_video != "Channel Overview (All Filtered Uploads)":
    video_data = df_filtered[df_filtered['Video_Title'] == selected_video].iloc[0]
    
    st.subheader(f"Content Analysis: {selected_video}")
    st.caption(f"Exact Upload Date & Time: {video_data['Publish_Timestamp'].strftime('%B %d, %Y at %H:%M')} ({video_data['Publish_Day']}) | Category: {video_data['Category']} | Total Duration: {video_data['Total_Video_Duration_Min']} min")
    
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
            color_discrete_sequence=["#0284C7", "#64748B"], template="plotly_white"
        )
        fig_bench.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=280, 
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color="#0F172A", size=12))
        )
        st.plotly_chart(fig_bench, use_container_width=True)

else:
    active_df = df_filtered.copy()

    if active_df.empty:
        st.warning("No records match your selected timeline and filter criteria. Please adjust your sidebar filters.")
    else:
        selected_bar = st.session_state.get("bar_chart", None)
        selected_pie = st.session_state.get("pie_chart", None)

        clicked_df = active_df.copy()
        selected_video_title = None

        bar_points = selected_bar.get("selection", {}).get("points", []) if selected_bar else []
        pie_points = selected_pie.get("selection", {}).get("points", []) if selected_pie else []

        if bar_points:
            clicked_title = bar_points[0].get("x")
            if clicked_title:
                selected_video_title = clicked_title
                clicked_df = clicked_df[clicked_df["Video_Title"] == clicked_title]
        elif pie_points:
            clicked_category = pie_points[0].get("label")
            if clicked_category:
                clicked_df = clicked_df[clicked_df["Category"] == clicked_category]

        # ======================================================================
        # 1. EXECUTIVE CHANNEL SUMMARY & KPI CARDS (RENDERED AT THE TOP)
        # ======================================================================
        if selected_video_title:
            single_vid_row = active_df[active_df["Video_Title"] == selected_video_title].iloc[0]
            exact_pub_timestamp = single_vid_row['Publish_Timestamp'].strftime('%B %d, %Y at %H:%M')
            st.markdown(f"### Executive Channel Summary &nbsp;|&nbsp; <span style='font-size:1rem; color:#0284C7;'>Exact Publish Date & Time: {exact_pub_timestamp} ({single_vid_row['Publish_Day']})</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"### Executive Channel Summary &nbsp;|&nbsp; <span style='font-size:1rem; color:#0284C7;'>Viewing Timeline: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}</span>", unsafe_allow_html=True)
        
        total_views = int(clicked_df['Views'].sum()) if not clicked_df.empty else 0
        total_watch = int(clicked_df['Watch_Time_Mins'].sum()) if not clicked_df.empty else 0
        total_likes = int(clicked_df['Likes'].sum()) if not clicked_df.empty else 0
        avg_eng = round(clicked_df['Engagement_Rate_%'].mean(), 2) if not clicked_df.empty else 0.0

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric("Catalog Views", f"{total_views:,}")
        kpi_col2.metric("Total Watch Time", f"{total_watch:,} mins")
        kpi_col3.metric("Engagement Likes", f"{total_likes:,}")
        kpi_col4.metric("Avg Engagement Rate", f"{avg_eng}%")

        st.markdown("---")

        # ======================================================================
        # 2. BAR & PIE CHARTS SECTION (RENDERED BELOW SUMMARY CARDS)
        # ======================================================================
        col_a, col_b = st.columns([3, 2])
        
        with col_a:
            st.markdown("##### Views by Video Title")
            fig_views = px.bar(
                active_df, x="Video_Title", y="Views", color="Category", 
                template="plotly_white", color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_views.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                height=350, xaxis=dict(showticklabels=False, title_font=dict(color="#0F172A")),
                yaxis=dict(title_font=dict(color="#0F172A")),
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#0F172A", size=12), title=dict(font=dict(color="#0284C7", size=13)))
            )
            st.plotly_chart(fig_views, use_container_width=True, on_select="rerun", selection_mode="points", key="bar_chart")
            
        with col_b:
            st.markdown("##### Watch Time Share by Category")
            fig_pie = px.pie(
                active_df, names="Category", values="Watch_Time_Mins", hole=0.5, 
                template="plotly_white", color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                height=350, margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#0F172A", size=12), title=dict(font=dict(color="#0284C7", size=13)))
            )
            st.plotly_chart(fig_pie, use_container_width=True, on_select="rerun", selection_mode="points", key="pie_chart")

        st.markdown("---")
        
        # ======================================================================
        # 3. LOWER VISUALS & DATA TABLE (WITH COMBINED DATE & TIME COLUMN)
        # ======================================================================
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.markdown("##### Audience Likes by Video Title")
            fig_likes = px.bar(
                clicked_df, y="Video_Title", x="Likes", color="Category",
                orientation="h", template="plotly_white", color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_likes.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, yaxis=dict(showticklabels=False), margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#0F172A", size=11))
            )
            st.plotly_chart(fig_likes, use_container_width=True)
            
        with col_d:
            st.markdown("##### Viewer Retention Depth (Avg vs Max Watch Time in Sec)")
            fig_retention = go.Figure()
            fig_retention.add_trace(go.Bar(
                x=clicked_df['Video_Title'], y=clicked_df['Avg_Duration_Sec'],
                name='Avg Watch Duration (Sec)', marker_color='#0284C7'
            ))
            fig_retention.add_trace(go.Bar(
                x=clicked_df['Video_Title'], y=clicked_df['Max_Watch_Sec'],
                name='Max Watch Duration (Sec)', marker_color='#38BDF8'
            ))
            fig_retention.update_layout(
                barmode='group', template="plotly_white",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, xaxis=dict(showticklabels=False), margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color="#0F172A", size=11))
            )
            st.plotly_chart(fig_retention, use_container_width=True)

        st.markdown("##### Granular Content Records")
        st.dataframe(
            clicked_df[['Video_Title', 'Category', 'Total_Video_Duration_Min', 'Watch_Time_Tier', 'Publish_Day', 'Publish_Date_Time', 'Views', 'Likes', 'Watch_Time_Mins', 'Avg_Duration_Sec', 'Max_Watch_Sec']], 
            use_container_width=True, 
            hide_index=True
        )