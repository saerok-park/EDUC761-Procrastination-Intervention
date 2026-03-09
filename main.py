# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import os

st.set_page_config(page_title="Goal Support System", layout="centered")

# -----------------------------
# Utilities
# -----------------------------
def now_iso():
    return datetime.now().isoformat(timespec="seconds")

def append_to_csv(row: dict, path: str = "goal_support_responses.csv"):
    df_new = pd.DataFrame([row])
    try:
        df_old = pd.read_csv(path)
        df = pd.concat([df_old, df_new], ignore_index=True)
    except FileNotFoundError:
        df = df_new
    df.to_csv(path, index=False)

def header_panel(assignment_name: str, deadline_dt: datetime, progress_label: str):
    st.markdown("### Goal Support Panel")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"**Assignment:** {assignment_name}")
        st.markdown(f"**Deadline:** {deadline_dt.strftime('%a, %b %d, %I:%M %p')}")
    with c2:
        st.markdown("**Progress**")
        st.progress(st.session_state.get("progress_bar", 0))
        st.caption(progress_label)
    st.divider()

def card(title: str, body: str):
    st.markdown(
        f"""
        <div style="border:1px solid #e6e6e6;border-radius:12px;padding:16px;margin:8px 0;">
          <div style="font-size:18px;font-weight:700;margin-bottom:6px;">{title}</div>
          <div style="font-size:15px;line-height:1.4;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Demo State (so you can submit now)
# -----------------------------
if "screen" not in st.session_state:
    st.session_state.screen = "home"  # home / initiation / midway / cramming / done
if "progress_bar" not in st.session_state:
    st.session_state.progress_bar = 0

# -----------------------------
# Sidebar controls (demo-friendly)
# -----------------------------
st.sidebar.title("Demo Controls")
student_id = st.sidebar.text_input("Student ID", value="S001")
course_id = st.sidebar.text_input("Course", value="BIO101")
assignment_name = st.sidebar.text_input("Assignment name", value="Genetics Lab Report")

deadline_date = st.sidebar.date_input("Deadline date", value=date.today())
deadline_time = st.sidebar.time_input("Deadline time", value=time(23, 59))
deadline_dt = datetime.combine(deadline_date, deadline_time)

st.sidebar.divider()
trigger = st.sidebar.selectbox(
    "Select Trigger (for demo)",
    [
        "Delayed Initiation (no access)",
        "Midway Check-in (low progress)",
        "Cramming Reflection (late activity)"
    ]
)

# optional: mock metrics (for text feedback)
mock_last24_pct = st.sidebar.slider("Mock: % activity in last 24h (for cramming)", 0, 100, 72)
mock_days_since_release = st.sidebar.slider("Mock: days since assignment released", 0, 14, 4)
mock_days_to_deadline = st.sidebar.slider("Mock: days to deadline (for midway)", 0, 14, 5)

st.sidebar.divider()
if st.sidebar.button("Start Trigger Flow"):
    if "Delayed Initiation" in trigger:
        st.session_state.screen = "initiation_alert"
        st.session_state.progress_bar = 0
    elif "Midway" in trigger:
        st.session_state.screen = "midway_progress"
        st.session_state.progress_bar = 25
    else:
        st.session_state.screen = "cramming_summary"
        st.session_state.progress_bar = 80

if st.sidebar.button("Reset App State"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

if st.sidebar.button("Clear Saved Responses"):
    if os.path.exists("goal_support_responses.csv"):
        os.remove("goal_support_responses.csv")
    st.session_state.last_saved = {}
    st.sidebar.success("Saved responses cleared.")
    st.rerun()

# -----------------------------
# Main
# -----------------------------
st.title("Behavior-Triggered Goal Support System (Wireframe)")
st.caption("Rule-based triggers + structured goal scaffolds (initiating, sustaining, completing).")

# Home
if st.session_state.screen == "home":
    header_panel(assignment_name, deadline_dt, "No active intervention")
    card(
        "How to use (for your submission demo)",
        "Use the left sidebar to pick a trigger and click **Start Trigger Flow**. "
        "Complete the short workflow; responses are saved to **goal_support_responses.csv**."
    )
    st.info("Tip: You can screenshot each stage as your wireframe/prototype evidence.")

# -----------------------------
# 1) Delayed Initiation
# -----------------------------
elif st.session_state.screen == "initiation_alert":
    header_panel(assignment_name, deadline_dt, "Initiation support")
    card(
        "⚠ You haven't started this assignment yet.",
        f"Assignment has been available for **{mock_days_since_release} days**. "
        "Starting early reduces last-minute stress. Let’s set your first step."
    )
    if st.button("Plan My First Step →"):
        st.session_state.screen = "initiation_plan"
        st.rerun()

elif st.session_state.screen == "initiation_plan":
    header_panel(assignment_name, deadline_dt, "Initiation: Micro-planning")
    st.subheader("STEP 1: Define the First Action")
    first_action = st.radio(
        "What is the very first physical action you can take?",
        [
            "Open the assignment page",
            "Read the instructions carefully",
            "Gather materials/resources",
            "Create an outline / draft document",
            "Other"
        ],
        index=1
    )
    other_action = ""
    if first_action == "Other":
        other_action = st.text_input("Other (please specify)")

    st.divider()
    st.subheader("STEP 2: Schedule It")
    plan_date = st.date_input("When will you do this? (date)", value=date.today())
    plan_time = st.time_input("Time", value=time(19, 0))

    duration = st.radio("How long will the first session be?", ["10 minutes", "20 minutes", "30+ minutes"], index=1)

    colA, colB = st.columns(2)
    with colA:
        save = st.button("Save Plan ✅")
    with colB:
        back = st.button("← Back")

    if back:
        st.session_state.screen = "initiation_alert"
        st.rerun()

    if save:
        planned_dt = datetime.combine(plan_date, plan_time)
        action_final = other_action.strip() if first_action == "Other" else first_action

        row = {
            "timestamp": now_iso(),
            "student_id": student_id,
            "course_id": course_id,
            "assignment_name": assignment_name,
            "trigger_type": "delayed_initiation",
            "deadline": deadline_dt.isoformat(timespec="minutes"),
            "input_first_action": action_final,
            "input_scheduled_start": planned_dt.isoformat(timespec="minutes"),
            "input_duration": duration,
        }
        append_to_csv(row)
        st.session_state.last_saved = row
        st.session_state.progress_bar = 35
        st.session_state.screen = "initiation_confirm"
        st.rerun()

elif st.session_state.screen == "initiation_confirm":
    header_panel(assignment_name, deadline_dt, "Initiation: Plan saved")
    saved = st.session_state.get("last_saved", {})
    card(
        "✔ Plan Saved",
        f"**First step:** {saved.get('input_first_action','(missing)')}<br>"
        f"**Scheduled:** {saved.get('input_scheduled_start','(missing)')}<br>"
        f"**Duration:** {saved.get('input_duration','(missing)')}",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Close"):
            st.session_state.screen = "home"
            st.rerun()
    with c2:
        st.caption("Optional: connect to calendar later (not needed for MVP).")

# -----------------------------
# 2) Midway Check-in (Sustaining)
# -----------------------------
elif st.session_state.screen == "midway_progress":
    header_panel(assignment_name, deadline_dt, f"Midway check-in (deadline in ~{mock_days_to_deadline} days)")
    card(
        "⏳ Midway Check-In",
        f"The deadline is in **{mock_days_to_deadline} days**. "
        "How much progress have you made?"
    )

    progress = st.radio("Select one:", ["0%", "25%", "50%", "75%", "Almost done"], index=1)

    if st.button("Continue →"):
        st.session_state.midway_progress = progress
        # Branch
        if progress in ["0%", "25%"]:
            st.session_state.screen = "midway_low_progress"
            st.session_state.progress_bar = 30
        else:
            st.session_state.screen = "midway_good_progress"
            st.session_state.progress_bar = 55
        st.rerun()

elif st.session_state.screen == "midway_low_progress":
    header_panel(assignment_name, deadline_dt, "Midway: Reset plan (low progress)")
    card(
        "Progress is still early.",
        "Let’s figure out what’s slowing you down and reset the next step."
    )

    barrier = st.radio(
        "What is currently slowing you down?",
        [
            "Other assignments",
            "Not sure where to start next",
            "Task feels difficult",
            "Forgot about it",
            "Other"
        ],
        index=0
    )
    barrier_other = ""
    if barrier == "Other":
        barrier_other = st.text_input("Other (please specify)")

    next_action = st.text_input("What is the next small action? (e.g., 'write methods paragraph')")
    reset_date = st.date_input("When will you do it? (date)", value=date.today())
    reset_time = st.time_input("Time", value=time(19, 0))

    colA, colB = st.columns(2)
    with colA:
        save = st.button("Save Reset Plan ✅")
    with colB:
        back = st.button("← Back")

    if back:
        st.session_state.screen = "midway_progress"
        st.rerun()

    if save:
        reset_dt = datetime.combine(reset_date, reset_time)
        barrier_final = barrier_other.strip() if barrier == "Other" else barrier

        row = {
            "timestamp": now_iso(),
            "student_id": student_id,
            "course_id": course_id,
            "assignment_name": assignment_name,
            "trigger_type": "midway_checkin_low_progress",
            "deadline": deadline_dt.isoformat(timespec="minutes"),
            "input_progress": st.session_state.get("midway_progress"),
            "input_barrier": barrier_final,
            "input_next_action": next_action.strip(),
            "input_next_action_time": reset_dt.isoformat(timespec="minutes"),
        }
        append_to_csv(row)
        st.session_state.last_saved = row
        st.session_state.progress_bar = 65
        st.session_state.screen = "midway_confirm"
        st.rerun()

elif st.session_state.screen == "midway_good_progress":
    header_panel(assignment_name, deadline_dt, "Midway: Keep momentum (good progress)")
    card(
        "You're making progress.",
        "Want to schedule your next work session to protect your goal from distractions?"
    )
    sched_date = st.date_input("Next session date", value=date.today())
    sched_time = st.time_input("Next session time", value=time(19, 0))
    duration = st.radio("Estimated duration", ["20 min", "45 min", "60+ min"], index=1)

    colA, colB = st.columns(2)
    with colA:
        save = st.button("Schedule Session ✅")
    with colB:
        back = st.button("← Back")

    if back:
        st.session_state.screen = "midway_progress"
        st.rerun()

    if save:
        sched_dt = datetime.combine(sched_date, sched_time)
        row = {
            "timestamp": now_iso(),
            "student_id": student_id,
            "course_id": course_id,
            "assignment_name": assignment_name,
            "trigger_type": "midway_checkin_good_progress",
            "deadline": deadline_dt.isoformat(timespec="minutes"),
            "input_progress": st.session_state.get("midway_progress"),
            "input_next_session_time": sched_dt.isoformat(timespec="minutes"),
            "input_duration": duration,
        }
        append_to_csv(row)
        st.session_state.last_saved = row
        st.session_state.progress_bar = 70
        st.session_state.screen = "midway_confirm"
        st.rerun()

elif st.session_state.screen == "midway_confirm":
    header_panel(assignment_name, deadline_dt, "Midway: Saved")
    saved = st.session_state.get("last_saved", {})
    card(
        "✔ Check-in Saved",
        f"**Trigger:** {saved.get('trigger_type','')}<br>"
        f"**Progress:** {saved.get('input_progress','')}<br>"
        f"**Next step/session:** {saved.get('input_next_action','') or saved.get('input_next_session_time','')}<br>"
    )
    if st.button("Close"):
        st.session_state.screen = "home"
        st.rerun()

# -----------------------------
# 3) Cramming Reflection (Completing)
# -----------------------------
elif st.session_state.screen == "cramming_summary":
    header_panel(assignment_name, deadline_dt, "Completing: Reflection")
    card(
        "📊 Activity Summary",
        f"Most of your work (**{mock_last24_pct}%**) happened within 24 hours of the deadline."
    )
    # simple visual bar
    st.write("Early activity vs Last 24 hours")
    early = max(0, 100 - mock_last24_pct)
    st.progress(early / 100)
    st.caption(f"Early: {early}%")
    st.progress(mock_last24_pct / 100)
    st.caption(f"Last 24h: {mock_last24_pct}%")

    if st.button("Reflect →"):
        st.session_state.screen = "cramming_reflect"
        st.rerun()

elif st.session_state.screen == "cramming_reflect":
    header_panel(assignment_name, deadline_dt, "Completing: Reflect & Re-plan")
    st.subheader("Reflection")
    planned_start = st.date_input("When did you originally plan to start?", value=date.today())

    barrier = st.radio(
        "What prevented earlier progress?",
        [
            "Other assignments",
            "Underestimated time needed",
            "Didn't know how to begin",
            "Felt overwhelmed",
            "Other"
        ],
        index=0
    )
    barrier_other = ""
    if barrier == "Other":
        barrier_other = st.text_input("Other (please specify)")

    st.divider()
    st.subheader("Re-plan (for next assignment)")
    use_checkpoint = st.radio("Would you like to set a midpoint checkpoint for the next assignment?", ["Yes", "Skip"], index=0)

    suggested = deadline_dt.date()
    # simple suggestion: deadline - 5 days (safe fallback; you can refine later)
    try:
        suggested_checkpoint = suggested.replace(day=suggested.day - 5)
    except ValueError:
        suggested_checkpoint = date.today()

    checkpoint_date = st.date_input("Suggested checkpoint date", value=suggested_checkpoint)
    checkpoint_time = st.time_input("Checkpoint time", value=time(19, 0))

    colA, colB = st.columns(2)
    with colA:
        save = st.button("Save Reflection ✅")
    with colB:
        back = st.button("← Back")

    if back:
        st.session_state.screen = "cramming_summary"
        st.rerun()

    if save:
        barrier_final = barrier_other.strip() if barrier == "Other" else barrier
        checkpoint_dt = datetime.combine(checkpoint_date, checkpoint_time) if use_checkpoint == "Yes" else ""

        row = {
            "timestamp": now_iso(),
            "student_id": student_id,
            "course_id": course_id,
            "assignment_name": assignment_name,
            "trigger_type": "cramming_reflection",
            "deadline": deadline_dt.isoformat(timespec="minutes"),
            "metric_last24h_pct": mock_last24_pct,
            "input_planned_start_date": planned_start.isoformat(),
            "input_barrier": barrier_final,
            "input_set_checkpoint": use_checkpoint,
            "input_checkpoint_time": checkpoint_dt if checkpoint_dt == "" else checkpoint_dt.isoformat(timespec="minutes"),
        }
        append_to_csv(row)
        st.session_state.last_saved = row
        st.session_state.progress_bar = 90
        st.session_state.screen = "cramming_confirm"
        st.rerun()

elif st.session_state.screen == "cramming_confirm":
    header_panel(assignment_name, deadline_dt, "Completing: Saved")
    saved = st.session_state.get("last_saved", {})
    card(
        "✔ Reflection Saved",
        f"**Barrier:** {saved.get('input_barrier','')}<br>"
        f"**Checkpoint set:** {saved.get('input_set_checkpoint','')}<br>"
        f"**Checkpoint time:** {saved.get('input_checkpoint_time','(none)')}",
    )
    if st.button("Close"):
        st.session_state.screen = "home"
        st.rerun()

# -----------------------------
# Footer: show saved data preview (helpful for submission)
# -----------------------------
st.divider()
st.markdown("#### Saved Responses Preview")
try:
    df = pd.read_csv("goal_support_responses.csv")
    st.dataframe(df.tail(10), width="stretch")
    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="goal_support_responses.csv",
        mime="text/csv"
    )
except FileNotFoundError:
    st.caption("No saved responses yet. Complete a flow to generate the CSV.")