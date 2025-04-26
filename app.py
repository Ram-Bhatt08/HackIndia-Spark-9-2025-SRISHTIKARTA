import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Refresh every 2 seconds, stop after 100 iterations
count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

# Time and date setup
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

st.title("Live Attendance Monitor")
st.write(f"Last updated at: {timestamp}")

# FizzBuzz-style counter output
if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Load attendance CSV if exists
csv_path = f"Attendance/Attendance_{date}.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.dataframe(df.style.highlight_max(axis=0))
else:
    st.warning(f"No attendance data found for {date}")

