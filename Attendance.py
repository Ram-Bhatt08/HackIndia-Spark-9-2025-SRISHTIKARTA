import pandas as pd
from datetime import datetime

def mark_attendance(name):
    date = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime("%H:%M:%S")
    filename = f"Attendance/Attendance_{date}.csv"
    
    # Check if attendance folder exists
    if not os.path.exists('Attendance'):
        os.makedirs('Attendance')
    
    # If file exists, load it; else create new dataframe
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=["Name", "Time", "Date"])
    
    # Check if this person is already marked today
    if name not in df["Name"].values:
        new_entry = {"Name": name, "Time": time, "Date": date}
        df = df.append(new_entry, ignore_index=True)
        df.to_csv(filename, index=False)
        print(f"Attendance marked for {name}")
    else:
        print(f"{name} already marked present today.")
