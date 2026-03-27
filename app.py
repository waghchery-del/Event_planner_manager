import streamlit as st
import pandas as pd
import os

# -------------------- Setup --------------------
st.set_page_config(page_title="Event Planner", page_icon="🎤", layout="centered")

st.title("🎤 Event Planner & Manager")
st.markdown("Organize your events like a pro 😌")

FILE = "events.csv"

# -------------------- Load Data --------------------
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Event", "Date", "Speaker", "Category"])

# -------------------- Dashboard --------------------
st.subheader("📊 Dashboard")
st.write(f"Total Events: **{len(df)}**")

# -------------------- Add Event --------------------
st.subheader("➕ Add New Event")

event = st.text_input("Event Name")
date = st.date_input("Event Date")
speaker = st.text_input("Speaker Name")
category = st.selectbox("Category", ["Tech", "Cultural", "Workshop", "Other"])

if st.button("Add Event 🚀"):
    if event and speaker:
        new_data = pd.DataFrame([[event, date, speaker, category]],
                                columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("✅ Event added successfully!")
    else:
        st.warning("⚠️ Please fill all fields")

# -------------------- View Events --------------------
st.subheader("📅 All Events")

if not df.empty:
    st.dataframe(df)

    # -------------------- Delete Event --------------------
    st.subheader("🗑️ Delete Event")

    event_to_delete = st.selectbox("Select event to delete", df["Event"].unique())

    if st.button("Delete Event ❌"):
        df = df[df["Event"] != event_to_delete]
        df.to_csv(FILE, index=False)
        st.success("Event deleted successfully!")
else:
    st.info("No events added yet 😢")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("Made using Streamlit")