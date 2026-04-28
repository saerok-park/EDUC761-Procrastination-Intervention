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

def header_panel(assignment_name: str, deadline_dt: datetime, progress_label: str, progress_value: float):
    st.markdown("### Goal Support Panel")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown(f"**Current Assignment:** {assignment_name}")
        st.markdown(f"**Deadline:** {deadline_dt.strftime('%a, %b %d, %I:%M %p')}")

    with c2:
        st.markdown("**Progress**")
        st.progress(progress_value)
        st.caption(progress_label)

    st.divider()

def semester_flow(assignments, current_assignment):
    st.markdown("### Semester Assignment Flow")
    st.caption("This overview shows where the current assignment fits within the larger course assignment sequence.")

    cols = st.columns(len(assignments))

    for i, assignment in enumerate(assignments):
        with cols[i]:
            is_current = assignment["name"] == current_assignment
            border = "2px solid #4a90e2" if is_current else "1px solid #dddddd"
            bg = "#eef6ff" if is_current else "#ffffff"

            st.markdown(
                f"""
                <div style="
                    border:{border};
                    background-color:{bg};
                    border-radius:12px;
                    padding:10px;
                    min-height:110px;
                    text-align:center;
                    margin-bottom:8px;">
                    <div style="font-weight:700;font-size:14px;">{assignment['short']}</div>
                    <div style="font-size:12px;margin-top:6px;">{assignment['deadline_label']}</div>
                    <div style="font-size:11px;margin-top:8px;color:#666;">
                        {'Current' if is_current else assignment['status']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

def next_assignment_panel(next_assignment_name, next_assignment_deadline, next_assignment_details):
    st.markdown("### Next Assignment Information")
    st.caption("This information is provided to help you connect reflection from the previous assignment to planning for the upcoming assignment.")

    card(
        f"Upcoming Assignment: {next_assignment_name}",
        f"""
        <b>Deadline:</b> {next_assignment_deadline.strftime('%a, %b %d, %I:%M %p')}<br>
        <b>Assignment Details:</b> {next_assignment_details}
        """
    )

def initiation_feedback(first_action, duration):
    if first_action == "Open the assignment page":
        return (
            "Good first step. Opening the assignment page reduces uncertainty and helps you move from avoiding the task "
            "to engaging with it. After opening it, identify one requirement you need to complete first."
        )
    elif first_action == "Read the instructions carefully":
        return (
            "This is a strong starting point. Reading the instructions carefully can help you understand the task demands "
            "and make a more realistic plan. After reading, write down one concrete subtask to complete next."
        )
    elif first_action == "Gather materials/resources":
        return (
            "Good plan. Gathering resources can make the task feel more manageable because you are preparing the conditions "
            "for focused work. After gathering materials, decide which part of the assignment you will work on first."
        )
    elif first_action == "Create an outline / draft document":
        return (
            "Creating an outline is a useful strategy because it turns a large assignment into smaller parts. "
            "After your first session, try to label the sections that still need more work."
        )
    else:
        return (
            "Nice job identifying a first action. Starting with a small, specific step can reduce procrastination by making "
            "the task feel less overwhelming and easier to begin."
        )

def sustaining_feedback(progress, barrier, next_action):
    if barrier == "Other assignments":
        return (
            "It sounds like competing deadlines are making it harder to sustain progress. A useful next step is to protect "
            "a short work session for this assignment, even if it is only 20–30 minutes, so progress does not stop completely."
        )
    elif barrier == "Not sure where to start next":
        return (
            "Uncertainty can make it difficult to continue. Your next action should be small and concrete. Instead of trying "
            "to finish the whole assignment, focus on identifying the next section, question, or paragraph to complete."
        )
    elif barrier == "Task feels difficult":
        return (
            "When a task feels difficult, breaking it into smaller steps can help rebuild momentum. Start with one manageable "
            "part and use that progress to decide what support or resources you may need next."
        )
    elif barrier == "Forgot about it":
        return (
            "Forgetting about the assignment is a sign that external reminders may help. Scheduling your next action now can "
            "support monitoring and help you re-engage before the deadline gets too close."
        )
    else:
        return (
            "Your response shows that you are monitoring your progress. The next step is to turn that reflection into a specific "
            "action so you can regain momentum before the deadline."
        )

def completing_feedback(barrier, improvement_focus, next_assignment_name):
    if barrier == "Underestimated time needed":
        return (
            f"This reflection is useful because underestimating time can lead to last-minute work. For {next_assignment_name}, "
            "try scheduling an earlier first session and a midway check-in so you can adjust your plan before the deadline."
        )
    elif barrier == "Didn't know how to begin":
        return (
            f"If beginning was difficult, the next assignment should start with a very small first step. For {next_assignment_name}, "
            "begin by reading the instructions and identifying one concrete task you can complete first."
        )
    elif barrier == "Felt overwhelmed":
        return (
            f"Feeling overwhelmed often means the task needs to be broken into smaller parts. For {next_assignment_name}, "
            "try creating a short task list and choosing only the first step to complete in your first work session."
        )
    elif barrier == "Other assignments":
        return (
            f"Competing assignments can make it easy to delay progress. For {next_assignment_name}, schedule one early work session "
            "before other deadlines become urgent, so you have a starting point already in place."
        )
    else:
        return (
            f"Your reflection can help you make a better plan for {next_assignment_name}. The goal is to use what happened in the "
            "previous assignment to choose a more specific and realistic first action next time."
        )

# -----------------------------
# Fixed demo values
# -----------------------------
student_id = "S001"
course_id = "BIO101"

assignment_name = "Genetics Lab Report"
deadline_dt = datetime.combine(date.today() + timedelta(days=2), time(23, 59))

next_assignment_name = "Evolution Lab Report"
next_assignment_deadline = datetime.combine(date.today() + timedelta(days=9), time(23, 59))
next_assignment_details = (
    "Write a 3–4 page lab report explaining evolutionary patterns using class data. "
    "The assignment includes data interpretation, a short methods section, and a discussion section."
)

assignments = [
    {"name": "Cell Structure Lab", "short": "Lab 1", "deadline_label": "Week 2", "status": "Completed"},
    {"name": "Enzyme Activity Lab", "short": "Lab 2", "deadline_label": "Week 4", "status": "Completed"},
    {"name": "Genetics Lab Report", "short": "Lab 3", "deadline_label": "Week 6", "status": "Current"},
    {"name": "Evolution Lab Report", "short": "Lab 4", "deadline_label": "Week 8", "status": "Upcoming"},
    {"name": "Ecology Data Report", "short": "Lab 5", "deadline_label": "Week 10", "status": "Upcoming"},
    {"name": "Final Research Report", "short": "Final", "deadline_label": "Week 14", "status": "Upcoming"},
]

# -----------------------------
# App
# -----------------------------
st.title("Goal Support System")

st.caption(
    "This prototype provides goal support at three time points based on students' log-data patterns: "
    "Initiating, Sustaining, and Completing."
)

semester_flow(assignments, assignment_name)

if st.button("Reset Demo"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]

    if os.path.exists("goal_support_responses.csv"):
        os.remove("goal_support_responses.csv")

    st.rerun()

tab1, tab2, tab3 = st.tabs(["Initiating", "Sustaining", "Completing"])

# -----------------------------
# Initiating Tab
# -----------------------------
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
        st.markdown("#### Recommended Next Step")
        st.info(initiation_feedback(action_final, duration))

        st.markdown("#### Why this matters")
        st.write(
            "Planning a small first action can reduce the gap between intention and action. "
            "This helps students move from delayed initiation to concrete task engagement."
        )

# -----------------------------
# Sustaining Tab
# -----------------------------
with tab2:
    header_panel(assignment_name, deadline_dt, "Sustaining support", 0.45)

    card(
        "⏳ Low Midway Progress Detected",
        "This demo assumes the assignment follows a 7-day window and the student is now at day 5 "
        "with limited progress. The system prompts the student to monitor their progress and reset the next step."
    )

    st.subheader("STEP 1: Monitor Current Progress")

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

    st.subheader("STEP 2: Reset the Next Action")

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
        st.markdown("#### Recommended Next Step")
        st.info(sustaining_feedback(progress, barrier_final, next_action))

        st.markdown("#### Why this matters")
        st.write(
            "Midway check-ins help students monitor whether their current progress matches the time remaining. "
            "When progress is lower than expected, resetting a small next action can support continued engagement."
        )

# -----------------------------
# Completing Tab
# -----------------------------
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

    st.divider()

    next_assignment_panel(
        next_assignment_name,
        next_assignment_deadline,
        next_assignment_details
    )

    st.subheader("STEP 1: Reflect on the Previous Assignment")

    planned_start = st.date_input(
        "When did you originally plan to start the previous assignment?",
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

    st.subheader("STEP 2: Plan for the Next Assignment")

    improvement_focus = st.radio(
        f"What would you like to do differently for {next_assignment_name}?",
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
        f"What is one specific action you will take for {next_assignment_name}?",
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

    if st.button("Save Reflection and Plan", key="save_complete"):
        barrier_final = barrier_other.strip() if barrier == "Other" else barrier

        improvement_final = (
            improvement_other.strip() if improvement_focus == "Other" else improvement_focus
        )

        next_step_dt = datetime.combine(next_plan_date, next_plan_time)

        row = {
            "timestamp": now_iso(),
            "student_id": student_id,
            "course_id": course_id,
            "previous_assignment_name": assignment_name,
            "next_assignment_name": next_assignment_name,
            "trigger_type": "cramming_reflection",
            "previous_assignment_deadline": deadline_dt.isoformat(timespec="minutes"),
            "next_assignment_deadline": next_assignment_deadline.isoformat(timespec="minutes"),
            "metric_last24h_pct": mock_last24_pct,
            "input_planned_start_date": planned_start.isoformat(),
            "input_barrier": barrier_final,
            "input_improvement_focus": improvement_final,
            "input_next_assignment_action": next_action.strip(),
            "input_next_assignment_start_time": next_step_dt.isoformat(timespec="minutes"),
        }

        append_to_csv(row)

        st.success("Reflection and next-assignment plan saved.")

        st.markdown("#### Personalized Feedback")
        st.info(
            completing_feedback(
                barrier_final,
                improvement_final,
                next_assignment_name
            )
        )

        st.markdown("#### Recommended Next Action")
        st.write(
            f"Your planned first step for **{next_assignment_name}** is:"
        )

        st.markdown(
            f"""
            <div style="border:1px solid #d6e9d6;border-radius:12px;padding:14px;margin:8px 0;background-color:#f7fff7;">
              <b>Action:</b> {next_action.strip() if next_action.strip() else "No action entered yet."}<br>
              <b>Scheduled time:</b> {next_step_dt.strftime('%a, %b %d, %I:%M %p')}<br>
              <b>Focus:</b> {improvement_final}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### Why this matters")
        st.write(
            "Reflection is most useful when it leads to a concrete adjustment. "
            "By connecting your previous last-minute pattern to a specific next action, "
            "you can use reflection to improve planning, monitoring, and time management for the next assignment."
        )

# -----------------------------
# Saved Responses Preview
# -----------------------------
st.divider()
st.markdown("#### Saved Responses Preview")

try:
    df = pd.read_csv("goal_support_responses.csv")
    st.dataframe(df.tail(10), width="stretch")
except FileNotFoundError:
    st.caption("No saved responses yet.")
