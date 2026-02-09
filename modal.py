import streamlit as st
import pandas as pd
import plotly.express as px

# --- APP CONFIG ---
st.set_page_config(layout="wide", page_title="Inventory & Profit Manager")

# --- MOCK DATA INITIALIZATION ---
if 'data_masuk' not in st.session_state:
    st.session_state.data_masuk = pd.DataFrame(columns=['Date', 'Supplier', 'Barang', 'Qty', 'Modal_Price'])
if 'data_penjualan' not in st.session_state:
    st.session_state.data_penjualan = pd.DataFrame(columns=['Date', 'Type', 'Barang', 'Qty', 'Sell_Price', 'Profit'])

# --- TABS SETUP ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📥 Upload & Input", "📦 Modal (Inventory)", "💰 Capital Gains", 
    "📊 Sales Data", "📈 Profit Analysis", "📉 Summary"
])

# --- TAB 1: UPLOAD & INPUT ---
with tab1:
    st.header("Data Ingestion")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Import Excel/CSV")
        uploaded_file = st.file_uploader("Upload Masuk Barang or Luar Kota", type=['xlsx', 'csv'])
        
    with col2:
        st.subheader("Chat / Manual Input (Luar Kota)")
        chat_input = st.text_area("Paste PO/Chat here (Format: Barang, Qty, Price)")
        if st.button("Process Chat"):
            st.success("Data parsed and added to session!")

# --- TAB 2: MODAL (INVENTORY) ---
with tab2:
    st.header("Stock on Hand")
    search = st.text_input("Filter by Supplier or Barang")
    # Logic to filter st.session_state.data_masuk goes here
    st.dataframe(st.session_state.data_masuk, use_container_width=True)

# --- TAB 6: SUMMARY (The Charts) ---
with tab6:
    st.header("Monthly Performance Summary")
    
    # Example Line Chart Logic
    if not st.session_state.data_penjualan.empty:
        # Create 3-line chart for Masuk, Luar Kota, Eceran
        df_trend = st.session_state.data_penjualan.groupby(['Date', 'Type']).sum().reset_index()
        fig = px.line(df_trend, x='Date', y='Qty', color='Type', title="Monthly Comparison")
        st.plotly_chart(fig, use_container_width=True)
        
        # Percentage comparison metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Barang Masuk", "12%", "+2% vs last month")
        c2.metric("Luar Kota", "45%", "+5% vs last month")
        c3.metric("Eceran", "20%", "-1% vs last month")
    else:
        st.info("Upload data in Tab 1 to see the summary charts.")

# --- EXPORT FEATURE ---
st.sidebar.header("Export Tools")
if st.sidebar.button("Export Final Report to Excel"):
    st.sidebar.write("Generating file...")
    # Add pandas to_excel logic here
