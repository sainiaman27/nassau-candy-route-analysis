import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Nassau Candy Route Efficiency Dashboard",
    page_icon="🍬",
    layout="wide"
)

# Load cleaned dataset
@st.cache_data
def load_data():
    df = pd.read_csv("nassau_candy_cleaned.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎛️ Dashboard Filters")

# Date range filter
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()
date_range = st.sidebar.date_input("Order Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Ship Mode filter
ship_modes = df['Ship Mode'].unique().tolist()
selected_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)

# Region filter
regions = df['Region'].unique().tolist()
selected_regions = st.sidebar.multiselect("Customer Region", regions, default=regions)

# Apply Filters
mask = (
    (df['Order Date'].dt.date >= date_range[0]) &
    (df['Order Date'].dt.date <= date_range[-1]) &
    (df['Ship Mode'].isin(selected_modes)) &
    (df['Region'].isin(selected_regions))
)
filtered_df = df[mask].copy()

# --- MAIN DASHBOARD HEADER ---
st.title("🍬 Nassau Candy Distributor: Route Efficiency Analytics")
st.markdown("Operational intelligence dashboard tracking factory-to-customer shipping performance, transit bottlenecks, and delivery lead times.")

# --- TOP-LEVEL METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Shipments", f"{len(filtered_df):,}")
col2.metric("Average Lead Time", f"{filtered_df['shipping_lead_time'].mean():.2f} days")
col3.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col4.metric("Gross Profit", f"${filtered_df['Gross Profit'].sum():,.2f}")

st.markdown("---")

# --- DASHBOARD TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Route Leaderboard", "🗺️ Geographic Shipping Map", "📦 Ship Mode Analysis", "🔍 Route Drill-Down"])

with tab1:
    st.subheader("Route Performance Leaderboard")
    route_perf = filtered_df.groupby(['Factory', 'Route_State']).agg(
        Shipments=('Order ID', 'count'),
        Avg_Lead_Time=('shipping_lead_time', 'mean'),
        Total_Sales=('Sales', 'sum')
    ).reset_index().sort_values(by='Avg_Lead_Time')
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Top 10 Most Efficient Routes")
        st.dataframe(route_perf.head(10), use_container_width=True)
    with col_b:
        st.markdown("### Top 10 Slowest Routes")
        st.dataframe(route_perf.sort_values(by='Avg_Lead_Time', ascending=False).head(10), use_container_width=True)

with tab2:
    st.subheader("US Geographic Shipping Efficiency Heatmap")
    map_df = filtered_df.groupby('State/Province').agg(
        Avg_Lead_Time=('shipping_lead_time', 'mean'),
        Shipments=('Order ID', 'count')
    ).reset_index()
    
    fig_map = px.choropleth(
        map_df, 
        locations='State/Province',
        locationmode='USA-states',
        color='Avg_Lead_Time',
        scope='usa',
        hover_data=['Shipments'],
        color_continuous_scale='Reds',
        title="Average Shipping Lead Time by US State"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    st.subheader("Ship Mode Efficiency Comparison")
    mode_summary = filtered_df.groupby('Ship Mode').agg(
        Avg_Lead_Time=('shipping_lead_time', 'mean'),
        Avg_Cost=('Cost', 'mean'),
        Shipments=('Order ID', 'count')
    ).reset_index()
    
    fig_mode = px.bar(
        mode_summary, x='Ship Mode', y='Avg_Lead_Time', color='Ship Mode',
        text_auto='.2f', title="Mean Lead Time by Shipping Method"
    )
    st.plotly_chart(fig_mode, use_container_width=True)

with tab4:
    st.subheader("Route & Order Drill-Down")
    selected_state = st.selectbox("Select State for Detailed View", sorted(filtered_df['State/Province'].unique()))
    state_orders = filtered_df[filtered_df['State/Province'] == selected_state]
    st.write(f"Showing {len(state_orders)} orders for {selected_state}:")
    st.dataframe(state_orders[['Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Product Name', 'Factory', 'shipping_lead_time', 'Sales']], use_container_width=True)