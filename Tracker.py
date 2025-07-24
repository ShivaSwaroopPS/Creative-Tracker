import streamlit as st
import datetime
import csv
import os

# ====== CONFIG ======
TRACKER_FILE = "daily_tracker_log.csv"
CHECKLIST_FILE = "custom_checklist.txt"
WORK_LOG_FILE = "daily_work_log.csv"
TODAY = datetime.date.today().isoformat()

st.set_page_config(page_title="Creative Builder Daily Tracker", layout="centered")
st.title("🚀 Creative Builder Daily Satisfaction Tracker")

# ====== LOAD OR INITIALIZE CHECKLIST ======
def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    else:
        default_items = [
            "Avoided Social Media",
            "No movies/YouTube (weekdays only)",
            "Ate healthy (no junk/sugar)",
            "Exercised (even light)",
            "1 or less cigarettes only",
            "No alcohol today (except weekend)",
            "Worked on something I love",
            "Explored something new",
            "Got at least 1 new idea today",
            "Reflected for 2 mins (notes / thought dump)",
            "Do I feel satisfied today?"
        ]
        save_checklist(default_items)
        return default_items

def save_checklist(items):
    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        for item in items:
            f.write(item + "\n")

checklist_items = load_checklist()

# ====== ADD/EDIT/DELETE CHECKLIST ITEMS ======
st.sidebar.title("🛠️ Customize Checklist")
new_item = st.sidebar.text_input("Add new item")
if st.sidebar.button("➕ Add") and new_item.strip():
    checklist_items.append(new_item.strip())
    save_checklist(checklist_items)
    st.experimental_rerun()

selected_item_to_delete = st.sidebar.selectbox("Select item to delete", ["-- Select --"] + checklist_items)
if st.sidebar.button("❌ Delete") and selected_item_to_delete != "-- Select --":
    checklist_items.remove(selected_item_to_delete)
    save_checklist(checklist_items)
    st.experimental_rerun()

# ====== DAILY CHECKLIST ======
st.subheader("✅ Daily Checklist")
responses = {}
for item in checklist_items:
    responses[item] = st.checkbox(item)

st.subheader("📝 Journal (Optional)")
journal_entry = st.text_area("What am I proud of today? What could I improve?", height=150)

# ====== WORK LOG ENTRY ======
st.subheader("💻 What did you work on today?")
work_entry = st.text_area("E.g., SNIIM chicken prices, cloud script update, etc.", height=100)

# ====== SAVE LOGIC ======
def save_to_csv(date, responses, notes):
    file_exists = os.path.isfile(TRACKER_FILE)
    with open(TRACKER_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date"] + list(responses.keys()) + ["Notes"])
        writer.writerow([date] + list(responses.values()) + [notes])

def save_work_log(date, work_note):
    if work_note.strip():
        file_exists = os.path.isfile(WORK_LOG_FILE)
        with open(WORK_LOG_FILE, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Date", "Work Done"])
            writer.writerow([date, work_note.strip()])

if st.button("💾 Save Today's Log"):
    save_to_csv(TODAY, responses, journal_entry)
    save_work_log(TODAY, work_entry)
    st.success("Saved! Come back tomorrow to track again ✨")

# ====== VIEW PAST ENTRIES ======
if os.path.exists(TRACKER_FILE):
    with st.expander("📅 View Past Checklist Entries"):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            st.text("".join(lines[-10:]))  # show last 10 entries
else:
    st.info("No past checklist logs found yet.")

if os.path.exists(WORK_LOG_FILE):
    with st.expander("🧾 View Past Work Entries"):
        with open(WORK_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            st.text("".join(lines[-10:]))  # show last 10 work logs
else:
    st.info("No past work logs found yet.")
    
    
    
#streamlit run "C:\Users\SHIVA.SWAROOP.P.S\OneDrive - S&P Global\Attachments\My Projects\Tracker.py"
