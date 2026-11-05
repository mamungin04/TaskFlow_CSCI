import streamlit as st
import json
import os

# TaskFlow: An Academic Task Management Application
# Created by: Malaysia Mungin

st.set_page_config(
    page_title="TaskFlow",
    page_icon="📚",
    layout="centered"
)

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(st.session_state.tasks, file, indent=4)


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()


st.title("📚 TaskFlow")
st.subheader("Your Academic Task Manager")

st.write(
    "TaskFlow helps college students organize assignments, "
    "exams, projects, and deadlines in one place."
)

st.divider()

st.header("Create a New Task")

with st.form("task_form"):
    title = st.text_input("Task Name")
    course = st.text_input("Course Name")
    due_date = st.date_input("Due Date")
    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if title.strip() and course.strip():
            task = {
                "id": len(st.session_state.tasks) + 1,
                "title": title,
                "course": course,
                "due_date": str(due_date),
                "priority": priority,
                "status": "Incomplete"
            }

            st.session_state.tasks.append(task)
            save_tasks()
            st.success("Task added successfully!")
        else:
            st.warning("Please enter a task name and course.")

st.divider()

st.header("My Academic Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add your first task above!")

for index, task in enumerate(st.session_state.tasks):
    with st.container(border=True):
        st.subheader(task["title"])
        st.write("Course:", task["course"])
        st.write("Due Date:", task["due_date"])
        st.write("Priority:", task["priority"])

        completed = st.checkbox(
            "Mark as complete",
            value=task["status"] == "Complete",
            key=f"complete_{index}"
        )

        if completed:
            task["status"] = "Complete"
            st.success("Completed")
        else:
            task["status"] = "Incomplete"
            st.warning("Incomplete")

        if st.button("Delete Task", key=f"delete_{index}"):
            st.session_state.tasks.pop(index)
            save_tasks()
            st.rerun()

save_tasks()
