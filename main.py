import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
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

def header_panel(assignment_name: str, deadline_dt: datetime, progress_label: str, progress_value: float):
    st.markdown("### Goal Support Panel")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"**Assignment:** {assignment_name}")
        st.markdown(f"**Deadline:** {deadline_dt.strftime('%a, %b %d, %I:%M %p')}")
    with c2:
        st.markdown("**Progress**")
        st.progress(progress_value)
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
# Fixed demo values
# -----------------------------
student_id = "S001"
course_id = "BIO101"
assignment_name = "Genetics Lab Report"
deadline_dt = datetime.combine(date.today() + timedelta(days=2), time(23, 59))

st.title("Goal Support System")
st.caption("Three time-point supports based on assumed student log-data patterns.")

if st.button("Reset Demo"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]

    if os.path.exists("goal_support_responses.csv"):
        os.remove("goal_support_responses.csv")

    st.rerun()

tab1, tab2, tab3 = st.tabs(["Initiating", "Sustaining", "Completing"])

with tab1:
    header_panel(assignment_name, deadline_dt, "Initiation support", 0.15)

    card(
        "⚠ Delayed Initiation Detected",
        "This demo assumes that 3 days have passed since the assignment was released, "
        "but the student has not yet started. The system prompts goal planning for the first step."
    )

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
        key="init_first_action"
    )

    other_action = ""
    if first_action == "Other":
        other_action = st.text_input("Other (please specify)", key="init_other_action")

    st.subheader("STEP 2: Schedule It")
    plan_date = st.date_input("When will you do this?", value=date.today(), key="init_date")
    plan_time = st.time_input("Time", value=time(19, 0), key="init_time")
    duration = st.radio(
        "How long will the first session be?",
        ["10 minutes", "20 minutes", "30+ minutes"],
        key="init_duration"
    )

    if st.button("Save Initiation Plan", key="save_init"):
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
        st.success("Initiation plan saved.")

with tab2:
    header_panel(assignment_name, deadline_dt, "Sustaining support", 0.45)

    card(
        "⏳ Low Midway Progress Detected",
        "This demo assumes the assignment follows a 7-day window and the student is now at day 5 "
        "with limited progress. The system prompts the student to reset the next step."
    )

    progress = st.radio(
        "How much progress have you made so far?",
        ["0%", "25%", "50%", "75%", "Almost done"],
        index=1,
        key="sustain_progress"
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
        key="sustain_barrier"
    )

    barrier_other = ""
    if barrier == "Other":
        barrier_other = st.text_input("Other (please specify)", key="sustain_other")

    next_action = st.text_input(
        "What is the next small action?",
        key="sustain_next_action"
    )
    reset_date = st.date_input("When will you do it?", value=date.today(), key="sustain_date")
    reset_time = st.time_input("Time", value=time(19, 0), key="sustain_time")

    if st.button("Save Sustaining Plan", key="save_sustain"):
        reset_dt = datetime.combine(reset_date, reset_time)
        barrier_final = barrier_other.strip() if barrier == "Other" else barrier

        row = {
            "timestamp": now_iso(),
            "student_id": student_id,
            "course_id": course_id,
            "assignment_name": assignment_name,
            "trigger_type": "midway_checkin_low_progress",
            "deadline": deadline_dt.isoformat(timespec="minutes"),
            "input_progress": progress,
            "input_barrier": barrier_final,
            "input_next_action": next_action.strip(),
            "input_next_action_time": reset_dt.isoformat(timespec="minutes"),
        }
        append_to_csv(row)
        st.success("Sustaining plan saved.")

with tab3:
    header_panel(assignment_name, deadline_dt, "Completing support", 0.85)

    card(
        "📊 Prior Last-Minute Pattern Detected",
        "This demo assumes that 72% of the student's activity on the previous assignment "
        "occurred within the last 24 hours before the deadline. The system prompts reflection "
        "and forward planning for the next assignment."
    )

    mock_last24_pct = 72
    early = 100 - mock_last24_pct

    st.write("Previous assignment activity pattern")
    st.progress(early / 100)
    st.caption(f"Early activity: {early}%")
    st.progress(mock_last24_pct / 100)
    st.caption(f"Last 24 hours: {mock_last24_pct}%")

    st.subheader("Reflection")
    planned_start = st.date_input(
        "When did you originally plan to start?",
        value=date.today() - timedelta(days=3),
        key="complete_planned_start"
    )

    barrier = st.radio(
        "What prevented earlier progress?",
        [
            "Other assignments",
            "Underestimated time needed",
            "Didn't know how to begin",
            "Felt overwhelmed",
            "Other"
        ],
        key="complete_barrier"
    )

    barrier_other = ""
    if barrier == "Other":
        barrier_other = st.text_input("Other (please specify)", key="complete_other")

    st.divider()
    st.subheader("Plan for the Next Assignment")

    improvement_focus = st.radio(
        "What would you like to do differently on the next assignment?",
        [
            "Start earlier",
            "Break the task into smaller steps",
            "Plan my work sessions in advance",
            "Ask for help sooner",
            "Manage distractions better",
            "Other"
        ],
        key="complete_improvement_focus"
    )

    improvement_other = ""
    if improvement_focus == "Other":
        improvement_other = st.text_input(
            "Other (please specify)",
            key="complete_improvement_other"
        )

    next_action = st.text_input(
        "What is one specific action you will take for the next assignment?",
        key="complete_next_action"
    )

    next_plan_date = st.date_input(
        "When will you take this first step?",
        value=date.today(),
        key="complete_next_date"
    )

    next_plan_time = st.time_input(
        "Time",
        value=time(19, 0),
        key="complete_next_time"
    )

    if st.button("Save Reflection", key="save_complete"):
        barrier_final = barrier_other.strip() if barrier == "Other" else barrier
        improvement_final = (
            improvement_other.strip() if improvement_focus == "Other" else improvement_focus
        )
        next_step_dt = datetime.combine(next_plan_date, next_plan_time)

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
            "input_improvement_focus": improvement_final,
            "input_next_assignment_action": next_action.strip(),
            "input_next_assignment_start_time": next_step_dt.isoformat(timespec="minutes"),
        }
        append_to_csv(row)
        st.success("Reflection saved.")

st.divider()
st.markdown("#### Saved Responses Preview")

try:
    df = pd.read_csv("goal_support_responses.csv")
    st.dataframe(df.tail(10), width="stretch")
except FileNotFoundError:
    st.caption("No saved responses yet.")

