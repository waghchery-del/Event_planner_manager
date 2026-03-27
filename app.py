import streamlit as st
import pandas as pd
import os
from datetime import date

# --- Configuration & Styling ---
st.set_page_config(page_title="Event Manager", layout="wide")

# Applying a professional, minimal look via CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Logic ---
DATA_FILE = "events.csv"

def load_data():
    """Load events from CSV or create a new DataFrame if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Event Name", "Date", "Speaker", "Category"])

def save_data(df):
    """Save the current DataFrame to a CSV file."""
    df.to_csv(DATA_FILE, index=False)

# Initialize session state data
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- Application Header ---
st.title("Event Planner & Manager")
st.markdown("---")

# --- Dashboard Section ---
st.header("Dashboard")
total_events = len(st.session_state.df)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Events", total_events)
st.markdown("---")

# --- Main Layout: Add Event and Event List ---
left_column, right_column = st.columns([1, 2], gap="large")

with left_column:
    st.header("Add Event")
    with st.form("event_form", clear_on_submit=True):
        event_name = st.text_input("Event Name")
        event_date = st.date_input("Date", min_value=date.today())
        speaker = st.text_input("Speaker")
        category = st.selectbox("Category", ["Tech", "Cultural", "Workshop", "Other"])
        
        submit_button = st.form_submit_button("Confirm Event")

        if submit_button:
            if event_name and speaker:
                # Create new entry
                new_event = pd.DataFrame([{
                    "Event Name": event_name,
                    "Date": event_date,
                    "Speaker": speaker,
                    "Category": category
                }])
                
                # Update DataFrame
                st.session_state.df = pd.concat([st.session_state.df, new_event], ignore_index=True)
                save_data(st.session_state.df)
                st.success("Event successfully recorded.")
                st.rerun()
            else:
                st.error("Please fill in all fields.")

with right_column:
    st.header("Event List")
    if not st.session_state.df.empty:
        # Display the table
        st.dataframe(st.session_state.df, use_container_width=True)
        
        # Delete Functionality
        st.markdown("### Manage Records")
        event_to_delete = st.selectbox("Select event to remove", st.session_state.df["Event Name"].unique())
        if st.button("Delete Selected Event"):
            st.session_state.df = st.session_state.df[st.session_state.df["Event Name"] != event_to_delete]
            save_data(st.session_state.df)
            st.warning(f"Removed: {event_to_delete}")
            st.rerun()
    else:
        st.info("No events scheduled at this time.")