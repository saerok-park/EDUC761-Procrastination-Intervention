import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import os

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
            background: linear-gradient(135deg, #f3f7fb 0%, #ffffff 100%);
            border: 1px solid #dbe4ee;
            border-radius: 20px;
            padding: 26px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.035);
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
            font-size: 23px;
            font-weight: 850;
            color: #111827;
            margin-top: 8px;
            margin-bottom: 4px;
        }

        .section-caption {
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 14px;
        }

        .metric-card {
            border-radius: 16px;
            padding: 16px;
            background-color: white;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.035);
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

        .phase-card {
            border-radius: 20px;
            padding: 22px;
            background-color: #ffffff;
            border: 1px solid #dfe7f0;
            box-shadow: 0 4px 14px rgba(0,0,0,0.04);
            min-height: 190px;
            margin-bottom: 12px;
        }

        .phase-number {
            font-size: 13px;
            font-weight: 800;
            color: #64748b;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .phase-title {
            font-size: 23px;
            font-weight: 900;
            color: #111827;
            margin-bottom: 8px;
        }

        .phase-trigger {
            font-size: 14px;
            font-weight: 750;
            color: #334155;
            background-color: #f1f5f9;
            border-radius: 999px;
            display: inline-block;
            padding: 6px 10px;
            margin-bottom: 10px;
        }

        .phase-body {
            font-size: 15px;
            color: #475569;
            line-height: 1.5;
        }

        .flow-card {
            border-radius: 16px;
            padding: 14px;
            min-height: 125px;
            background-color: white;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 8px rgba(0,0,0,0.035);
            text-align: center;
            margin-bottom: 8px;
        }

        .flow-card-current {
            border: 2px solid #64748b;
            background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        }

        .flow-card-completed {
            border: 1px solid #d1fae5;
            background: #f7fefb;
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
            background-color: #e2e8f0;
            color: #334155;
            font-weight: 800;
        }

        .status-completed {
            background-color: #dcfce7;
            color: #166534;
            font-weight: 800;
        }

        .alert-card {
            border-left: 7px solid #d97706;
            background-color: #fffbeb;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.025);
        }

        .alert-title {
            font-size: 19px;
            font-weight: 850;
            color: #78350f;
            margin-bottom: 6px;
        }

        .alert-body {
            font-size: 15px;
            color: #6b4e16;
            line-height: 1.5;
        }

        .context-card {
            border-left: 7px solid #64748b;
            background-color: #f8fafc;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.025);
        }

        .context-title {
            font-size: 19px;
            font-weight: 850;
            color: #334155;
            margin-bottom: 6px;
        }

        .context-body {
            font-size: 15px;
            color: #475569;
            line-height: 1.5;
        }

        .feedback-card {
            border-left: 7px solid #7c8da6;
            background-color: #f4f7fb;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.025);
        }

        .feedback-title {
            font-size: 19px;
            font-weight: 850;
            color: #334155;
            margin-bottom: 6px;
        }

        .feedback-body {
            font-size: 15px;
            color: #475569;
            line-height: 1.5;
        }

        .recommend-card {
            border-left: 7px solid #5f9f86;
            background-color: #f3faf7;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.025);
        }

        .recommend-title {
            font-size: 19px;
            font-weight: 850;
            color: #2f6f5e;
            margin-bottom: 6px;
        }

        .recommend-body {
            font-size: 15px;
            color: #365f53;
            line-height: 1.5;
        }

        .why-card {
            border-left: 7px solid #9a8c98;
            background-color: #faf7fb;
            border-radius: 16px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.025);
        }

        .why-title {
            font-size: 19px;
            font-weight: 850;
            color: #5f5067;
            margin-bottom: 6px;
        }

        .why-body {
            font-size: 15px;
            color: #5b5263;
            line-height: 1.5;
        }

        .saved-card {
            border-left: 7px solid #6aa57b;
            background-color: #f4fbf6;
            border-radius: 16px;
            padding: 16px;
            margin: 16px 0;
            color: #2f6840;
            font-weight: 750;
        }

        div[data-testid="stTabs"] button {
            font-size: 22px;
            font-weight: 900;
            padding: 20px 34px;
            border-radius: 16px 16px 0 0;
        }
        
        div[data-testid="stTabs"] button p {
            font-size: 22px;
            font-weight: 900;
        }
        
        div[data-testid="stTabs"] [role="tablist"] {
            gap: 12px;
            border-bottom: 2px solid #e5e7eb;
        }
        
        div[data-testid="stTabs"] [aria-selected="true"] {
            background-color: #f1f5f9;
            border-bottom: 4px solid #475569;
        }

        div[data-testid="stTabs"] [aria-selected="true"] p {
            color: #111827;
        }

        div[data-testid="stTabs"] [aria-selected="false"] p {
            color: #64748b;
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
    st.markdown(f"""<div class="saved-card">✅ {text}</div>""", unsafe_allow_html=True)


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


# -----------------------------
# Layout components
# -----------------------------
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

    metrics = [
        ("Course", course_id),
        ("Current Assignment", assignment_name),
        ("Current Deadline", deadline_dt.strftime('%b %d, %I:%M %p')),
        ("Next Assignment", f"{next_assignment_name}<br>{next_assignment_deadline.strftime('%b %d')}")
    ]

    for col, (title, value) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
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
# Feedback and recommendation logic
# -----------------------------
def initiation_feedback(first_action):
    if first_action == "Open the assignment page":
        return "Opening the assignment page is a useful way to reduce uncertainty and begin engaging with the task."
    elif first_action == "Read the instructions carefully":
        return "Reading the instructions carefully helps you understand the task demands before committing to a larger plan."
    elif first_action == "Gather materials/resources":
        return "Gathering resources prepares the conditions for focused work and can make the task feel more manageable."
    elif first_action == "Create an outline / draft document":
        return "Creating an outline turns a large assignment into smaller, more manageable parts."
    else:
        return "Identifying a small first action is a productive way to make the task less overwhelming."


def initiation_recommendation(first_action, planned_dt, duration):
    return (
        f"After your scheduled <b>{duration}</b> session, do not stop at simply completing the first action. "
        f"Use that session to identify the next concrete subtask. For example, after you <b>{first_action}</b>, "
        f"write down one thing you need to complete next and when you will do it."
    )


def sustaining_feedback(barrier):
    if barrier == "Other assignments":
        return "Competing deadlines can make it harder to sustain progress because attention is divided across tasks."
    elif barrier == "Not sure where to start next":
        return "Uncertainty about the next step can interrupt progress even after the assignment has already been started."
    elif barrier == "Task feels difficult":
        return "When the task feels difficult, avoidance can increase unless the work is broken into smaller steps."
    elif barrier == "Forgot about it":
        return "Forgetting about the assignment suggests that external reminders or scheduled check-ins may be useful."
    else:
        return "Monitoring your barrier is an important step because it helps you choose a better next action."


def sustaining_recommendation(progress, barrier, next_action, reset_dt):
    if barrier == "Other assignments":
        return (
            f"Protect a short work block for this assignment before switching to other tasks. "
            f"Start with <b>{next_action if next_action else 'one small action'}</b> at "
            f"<b>{reset_dt.strftime('%a, %b %d, %I:%M %p')}</b>, even if the session is brief."
        )
    elif barrier == "Not sure where to start next":
        return (
            f"Before trying to make major progress, spend the first 5 minutes clarifying the next section or question. "
            f"Then complete <b>{next_action if next_action else 'one small action'}</b>."
        )
    elif barrier == "Task feels difficult":
        return (
            f"Choose the easiest meaningful part of the task first. Use <b>{next_action if next_action else 'your next action'}</b> "
            f"as a low-pressure entry point, then decide whether you need help or additional resources."
        )
    else:
        return (
            f"Use your scheduled time to restart momentum. Begin with <b>{next_action if next_action else 'one small action'}</b>, "
            f"then check whether your progress has moved beyond <b>{progress}</b>."
        )


def completing_feedback(barrier, next_assignment_name):
    if barrier == "Underestimated time needed":
        return f"Underestimating time can lead to last-minute work. This reflection can help you plan more realistic work sessions for {next_assignment_name}."
    elif barrier == "Didn't know how to begin":
        return f"Difficulty beginning suggests that the first step for {next_assignment_name} should be very small and concrete."
    elif barrier == "Felt overwhelmed":
        return f"Feeling overwhelmed suggests that {next_assignment_name} should be broken into smaller parts before starting."
    elif barrier == "Other assignments":
        return f"Competing assignments can delay progress, so {next_assignment_name} may need an earlier protected work session."
    else:
        return f"Your reflection can help you make a more intentional plan for {next_assignment_name}."


def completing_recommendation(barrier, improvement_focus, next_action, next_step_dt, next_assignment_name):
    if barrier == "Underestimated time needed":
        return (
            f"For <b>{next_assignment_name}</b>, add one extra early planning session before your first work session. "
            f"Use that time to estimate how long each section will take, then begin with "
            f"<b>{next_action if next_action else 'your first planned action'}</b>."
        )
    elif barrier == "Didn't know how to begin":
        return (
            f"For <b>{next_assignment_name}</b>, begin with a task-understanding step before doing the main work. "
            f"At <b>{next_step_dt.strftime('%a, %b %d, %I:%M %p')}</b>, start by reviewing the instructions and identifying the first section to complete."
        )
    elif barrier == "Felt overwhelmed":
        return (
            f"For <b>{next_assignment_name}</b>, create a short task list with 3 smaller parts. "
            f"Then only focus on the first part: <b>{next_action if next_action else 'your first planned action'}</b>."
        )
    else:
        return (
            f"For <b>{next_assignment_name}</b>, turn your improvement focus, <b>{improvement_focus}</b>, into a concrete scheduled behavior. "
            f"Begin with <b>{next_action if next_action else 'your first planned action'}</b> at "
            f"<b>{next_step_dt.strftime('%a, %b %d, %I:%M %p')}</b>."
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

tab1, tab2, tab3 = st.tabs(["🚀 Initiating", "🔄 Sustaining", "📌 Completing"])

if st.button("Reset Demo"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]

    if os.path.exists("goal_support_responses.csv"):
        os.remove("goal_support_responses.csv")

    st.rerun()



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
            initiation_feedback(action_final)
        )

        recommendation_card(
            "Recommended Next Action",
            initiation_recommendation(action_final, planned_dt, duration)
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
            sustaining_feedback(barrier_final)
        )

        recommendation_card(
            "Recommended Next Action",
            sustaining_recommendation(progress, barrier_final, next_action.strip(), reset_dt)
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

    next_assignment_panel(
        next_assignment_name,
        next_assignment_deadline,
        next_assignment_details
    )

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
            completing_feedback(barrier_final, next_assignment_name)
        )

        recommendation_card(
            "Recommended Next Action",
            completing_recommendation(
                barrier_final,
                improvement_final,
                next_action.strip(),
                next_step_dt,
                next_assignment_name
            )
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
