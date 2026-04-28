import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Goal Support System", layout="wide")


# -----------------------------
# Custom CSS
# -----------------------------
def inject_custom_css():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        .hero-box {
            background: linear-gradient(135deg, #eef6ff 0%, #f8fbff 100%);
            border: 1px solid #d8eaff;
            border-radius: 20px;
            padding: 26px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.04);
        }

        .hero-title {
            font-size: 32px;
            font-weight: 850;
            color: #111827;
            margin-bottom: 8px;
        }

        .hero-subtitle {
            font-size: 16px;
            color: #4b5563;
            line-height: 1.55;
        }

        .section-title {
            font-size: 22px;
            font-weight: 800;
            color: #111827;
            margin-top: 8px;
            margin-bottom: 4px;
        }

        .section-caption {
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 12px;
        }

        .metric-card {
            border-radius: 16px;
            padding: 16px;
            background-color: white;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            text-align: center;
            min-height: 95px;
        }

        .metric-title {
            font-size: 13px;
            color: #6b7280;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .metric-value {
            font-size: 18px;
            color: #111827;
            font-weight: 800;
        }

        .flow-card {
            border-radius: 16px;
            padding: 14px;
            min-height: 125px;
            background-color: white;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            text-align: center;
            margin-bottom: 8px;
        }

        .flow-card-current {
            border: 2px solid #2563eb;
            background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%);
        }

        .flow-card-completed {
            border: 1px solid #bbf7d0;
            background: #f0fdf4;
        }

        .flow-week {
            font-size: 12px;
            font-weight: 800;
            color: #6b7280;
            margin-bottom: 8px;
        }

        .flow-title {
            font-size: 15px;
            font-weight: 850;
            color: #111827;
            margin-bottom: 10px;
        }

        .flow-status {
            font-size: 12px;
            color: #4b5563;
            background-color: #f3f4f6;
            border-radius: 999px;
            padding: 5px 9px;
            display: inline-block;
        }

        .status-current {
            background-color: #dbeafe;
            color: #1d4ed8;
            font-weight: 800;
        }

        .status-completed {
            background-color: #dcfce7;
            color: #15803d;
            font-weight: 800;
        }

        .alert-card {
            border-left: 7px solid #f59e0b;
            background-color: #fffbeb;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .alert-title {
            font-size: 19px;
            font-weight: 850;
            color: #92400e;
            margin-bottom: 6px;
        }

        .alert-body {
            font-size: 15px;
            color: #78350f;
            line-height: 1.5;
        }

        .context-card {
            border-left: 7px solid #6366f1;
            background-color: #eef2ff;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .context-title {
            font-size: 19px;
            font-weight: 850;
            color: #3730a3;
            margin-bottom: 6px;
        }

        .context-body {
            font-size: 15px;
            color: #312e81;
            line-height: 1.5;
        }

        .feedback-card {
            border-left: 7px solid #2563eb;
            background-color: #eff6ff;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .feedback-title {
            font-size: 19px;
            font-weight: 850;
            color: #1d4ed8;
            margin-bottom: 6px;
        }

        .feedback-body {
            font-size: 15px;
            color: #1e3a8a;
            line-height: 1.5;
        }

        .recommend-card {
            border-left: 7px solid #10b981;
            background-color: #ecfdf5;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .recommend-title {
            font-size: 19px;
            font-weight: 850;
            color: #047857;
            margin-bottom: 6px;
        }

        .recommend-body {
            font-size: 15px;
            color: #064e3b;
            line-height: 1.5;
        }

        .why-card {
            border-left: 7px solid #8b5cf6;
            background-color: #f5f3ff;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .why-title {
            font-size: 19px;
            font-weight: 850;
            color: #6d28d9;
            margin-bottom: 6px;
        }

        .why-body {
            font-size: 15px;
            color: #4c1d95;
            line-height: 1.5;
        }

        .saved-card {
            border-left: 7px solid #22c55e;
            background-color: #f0fdf4;
            border-radius: 16px;
            padding: 16px;
            margin: 16px 0;
            color: #166534;
            font-weight: 750;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


inject_custom_css()


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


def saved_message(text):
    st.markdown(
        f"""
        <div class="saved-card">
            ✅ {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def alert_card(title, body):
    st.markdown(
        f"""
        <div class="alert-card">
            <div class="alert-title">{title}</div>
            <div class="alert-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def context_card(title, body):
    st.markdown(
        f"""
        <div class="context-card">
            <div class="context-title">{title}</div>
            <div class="context-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def feedback_card(title, body):
    st.markdown(
        f"""
        <div class="feedback-card">
            <div class="feedback-title">{title}</div>
            <div class="feedback-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def recommendation_card(title, body):
    st.markdown(
        f"""
        <div class="recommend-card">
            <div class="recommend-title">{title}</div>
            <div class="recommend-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def why_card(title, body):
    st.markdown(
        f"""
        <div class="why-card">
            <div class="why-title">{title}</div>
            <div class="why-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def hero_section():
    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">Goal Support System</div>
            <div class="hero-subtitle">
                A prototype designed to reduce procrastination by providing timely support across three learning phases:
                <b>initiating</b>, <b>sustaining</b>, and <b>completing</b>. 
                The system uses assignment context, log-data patterns, reflection prompts, and rule-based adaptive feedback
                to help students move from awareness to concrete action.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_overview(course_id, assignment_name, deadline_dt, next_assignment_name, next_assignment_deadline):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Course</div>
                <div class="metric-value">{course_id}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Current Assignment</div>
                <div class="metric-value">{assignment_name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Current Deadline</div>
                <div class="metric-value">{deadline_dt.strftime('%b %d, %I:%M %p')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Next Assignment</div>
                <div class="metric-value">{next_assignment_name}<br>{next_assignment_deadline.strftime('%b %d')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()


def semester_flow(assignments, current_assignment):
    st.markdown('<div class="section-title">Semester Assignment Flow</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">This overview shows where the current assignment fits within the larger course assignment sequence.</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(len(assignments))

    for i, assignment in enumerate(assignments):
        is_current = assignment["name"] == current_assignment
        is_completed = assignment["status"] == "Completed"

        if is_current:
            card_class = "flow-card flow-card-current"
            status_class = "flow-status status-current"
            status_text = "Current"
        elif is_completed:
            card_class = "flow-card flow-card-completed"
            status_class = "flow-status status-completed"
            status_text = "Completed"
        else:
            card_class = "flow-card"
            status_class = "flow-status"
            status_text = assignment["status"]

        with cols[i]:
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="flow-week">{assignment['deadline_label']}</div>
                    <div class="flow-title">{assignment['short']}</div>
                    <div class="{status_class}">{status_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()


def header_panel(assignment_name, deadline_dt, progress_label, progress_value):
    c1, c2 = st.columns([2.3, 1])

    with c1:
        context_card(
            "Assignment Context",
            f"""
            <b>Assignment:</b> {assignment_name}<br>
            <b>Deadline:</b> {deadline_dt.strftime('%a, %b %d, %I:%M %p')}<br>
            <b>Purpose:</b> Use this support panel to turn your current learning situation into a specific next action.
            """
        )

    with c2:
        st.markdown("#### Progress")
        st.progress(progress_value)
        st.caption(progress_label)


def next_assignment_panel(next_assignment_name, next_assignment_deadline, next_assignment_details):
    context_card(
        f"Upcoming Assignment: {next_assignment_name}",
        f"""
        <b>Deadline:</b> {next_assignment_deadline.strftime('%a, %b %d, %I:%M %p')}<br>
        <b>Assignment Details:</b> {next_assignment_details}
        """
    )


# -----------------------------
# Feedback logic
# -----------------------------
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
# App layout
# -----------------------------
hero_section()

metric_overview(
    course_id,
    assignment_name,
    deadline_dt,
    next_assignment_name,
    next_assignment_deadline
)

semester_flow(assignments, assignment_name)

if st.button("Reset Demo"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]

    if os.path.exists("goal_support_responses.csv"):
        os.remove("goal_support_responses.csv")

    st.rerun()

tab1, tab2, tab3 = st.tabs(["🚀 Initiating", "🔄 Sustaining", "📌 Completing"])


# -----------------------------
# Initiating Tab
# -----------------------------
with tab1:
    header_panel(assignment_name, deadline_dt, "Initiation support", 0.15)

    alert_card(
        "⚠ Delayed Initiation Detected",
        "Three days have passed since the assignment was released, but no activity has been detected yet. "
        "This support message helps you choose a small first step and schedule it."
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

        saved_message("Initiation plan saved.")

        feedback_card(
            "Personalized Feedback",
            initiation_feedback(action_final, duration)
        )

        recommendation_card(
            "Recommended Next Step",
            f"""
            Start with: <b>{action_final if action_final else "your selected first action"}</b><br>
            Scheduled time: <b>{planned_dt.strftime('%a, %b %d, %I:%M %p')}</b><br>
            Planned duration: <b>{duration}</b>
            """
        )

        why_card(
            "Why this matters",
            "Planning a small first action can reduce the gap between intention and action. "
            "This helps students move from delayed initiation to concrete task engagement."
        )


# -----------------------------
# Sustaining Tab
# -----------------------------
with tab2:
    header_panel(assignment_name, deadline_dt, "Sustaining support", 0.45)

    alert_card(
        "⏳ Low Midway Progress Detected",
        "The assignment follows a 7-day work window, and the student is now at day 5 with limited progress. "
        "This check-in helps the student monitor progress, identify barriers, and reset the next action."
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

        saved_message("Sustaining plan saved.")

        feedback_card(
            "Personalized Feedback",
            sustaining_feedback(progress, barrier_final, next_action)
        )

        recommendation_card(
            "Recommended Next Step",
            f"""
            Current progress: <b>{progress}</b><br>
            Main barrier: <b>{barrier_final}</b><br>
            Next action: <b>{next_action.strip() if next_action.strip() else "No action entered yet."}</b><br>
            Scheduled time: <b>{reset_dt.strftime('%a, %b %d, %I:%M %p')}</b>
            """
        )

        why_card(
            "Why this matters",
            "Midway check-ins help students monitor whether their current progress matches the time remaining. "
            "When progress is lower than expected, resetting a small next action can support continued engagement."
        )


# -----------------------------
# Completing Tab
# -----------------------------
with tab3:
    header_panel(assignment_name, deadline_dt, "Completing support", 0.85)

    alert_card(
        "📊 Prior Last-Minute Pattern Detected",
        "The system detected that 72% of the student's activity on the previous assignment occurred within the last 24 hours "
        "before the deadline. This support message prompts reflection and forward planning for the next assignment."
    )

    mock_last24_pct = 72
    early = 100 - mock_last24_pct

    st.markdown("#### Previous Assignment Activity Pattern")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Early activity**")
        st.progress(early / 100)
        st.caption(f"{early}% of activity occurred before the last 24 hours.")

    with c2:
        st.markdown("**Last-minute activity**")
        st.progress(mock_last24_pct / 100)
        st.caption(f"{mock_last24_pct}% of activity occurred within the last 24 hours.")

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

        saved_message("Reflection and next-assignment plan saved.")

        feedback_card(
            "Personalized Feedback",
            completing_feedback(
                barrier_final,
                improvement_final,
                next_assignment_name
            )
        )

        recommendation_card(
            "Recommended Next Action",
            f"""
            Upcoming assignment: <b>{next_assignment_name}</b><br>
            Main reflection: <b>{barrier_final}</b><br>
            Improvement focus: <b>{improvement_final}</b><br>
            First action: <b>{next_action.strip() if next_action.strip() else "No action entered yet."}</b><br>
            Scheduled time: <b>{next_step_dt.strftime('%a, %b %d, %I:%M %p')}</b>
            """
        )

        why_card(
            "Why this matters",
            "Reflection is most useful when it leads to a concrete adjustment. "
            "By connecting the previous last-minute pattern to a specific next action, "
            "students can use reflection to improve planning, monitoring, and time management for the next assignment."
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
