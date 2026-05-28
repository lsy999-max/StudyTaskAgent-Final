import streamlit as st
from agent import StudyTaskAgent
from memory import save_memory, load_memory, clear_memory
from exporter import build_task_plan_text


EXAMPLE_ASSIGNMENT = (
    "Write a 1500-word report about how artificial intelligence is used in education. "
    "The report should include at least five academic sources and proper references. "
    "Prepare a 5-minute presentation summarising your main findings. "
    "Submit the report and slides by Friday."
)


st.set_page_config(
    page_title="StudyTask Agent",
    page_icon="📝",
    layout="wide"
)


# Sidebar
with st.sidebar:
    st.title("StudyTask Agent")

    st.markdown(
        """
        **Purpose**

        This agent helps students convert assignment instructions into a practical work plan.

        **Agent loop**

        1. Observe the assignment text  
        2. Analyse requirements  
        3. Decide workload and risks  
        4. Act by generating a plan  
        5. Remember previous plans  
        """
    )

    st.divider()

    st.markdown(
        """
        **Example input**

        Write a 1500-word report about AI in education, include five sources, 
        prepare a 5-minute presentation, and submit by Friday.
        """
    )


st.title("StudyTask Agent: General Assignment Planning Agent")

st.write(
    "This prototype helps students turn assignment instructions into a clear work plan. "
    "The agent observes the input text, analyses assignment components, detects deadlines "
    "and constraints, estimates workload, identifies planning risks, stores the result in memory, "
    "and generates a practical completion plan."
)


with st.expander("Agent Workflow", expanded=True):
    st.markdown(
        """
        **observe → analyse → decide → act → remember**

        - **Observe:** read the assignment instructions provided by the user.
        - **Analyse:** identify assignment components, deadlines, constraints, and required skills.
        - **Decide:** estimate priority, workload, and possible planning risks.
        - **Act:** generate a task breakdown, phased work plan, and completion checklist.
        - **Remember:** save the generated plan to local memory.
        """
    )


st.subheader("Input")

if "assignment_text" not in st.session_state:
    st.session_state.assignment_text = ""

if st.button("Use Example Assignment"):
    st.session_state.assignment_text = EXAMPLE_ASSIGNMENT

assignment_text = st.text_area(
    "Paste assignment instructions here:",
    value=st.session_state.assignment_text,
    height=250,
    placeholder=(
        "Example: Write a 1500-word report and prepare a 5-minute presentation. "
        "Use at least five academic sources and submit the work by Friday."
    ),
)


if st.button("Generate Assignment Plan"):
    if assignment_text.strip() == "":
        st.warning("Please paste some assignment instructions first.")

    elif len(assignment_text.split()) < 15:
        st.warning(
            "The input is too short for reliable planning. "
            "Please provide more assignment details, such as required outputs, deadline, "
            "word limit, presentation length, or marking requirements."
        )

    else:
        agent = StudyTaskAgent(assignment_text)
        result = agent.run()
        save_memory(assignment_text, result)

        st.success("Assignment plan generated successfully and saved to memory.")

        st.divider()
        st.subheader("Agent Output")

        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown("### 1. Agent Observation")
            st.write(f"Word count: {result['observation']['word_count']}")
            st.write(f"Sentence count: {result['observation']['sentence_count']}")

            st.markdown("### 2. Detected Assignment Components")
            if result["assignment_components"]:
                for item in result["assignment_components"]:
                    st.write(f"- {item}")
            else:
                st.write("No clear assignment components detected.")

            st.markdown("### 3. Detected Deadlines")
            if result["deadlines"]:
                for item in result["deadlines"]:
                    st.write(f"- {item}")
            else:
                st.write("No clear deadline detected.")

            st.markdown("### 4. Detected Constraints")
            if result["constraints"]:
                for item in result["constraints"]:
                    st.write(f"- {item}")
            else:
                st.write("No clear constraints detected.")

        with right_column:
            st.markdown("### 5. Required Skills")
            if result["required_skills"]:
                for item in result["required_skills"]:
                    st.write(f"- {item}")
            else:
                st.write("No specific skills detected.")

            st.markdown("### 6. Agent Decision")
            st.write(f"Priority level: **{result['priority']}**")
            st.write(f"Estimated workload: **{result['workload']}**")

        st.divider()

        st.markdown("### 7. Task Breakdown")
        for index, task in enumerate(result["task_breakdown"], start=1):
            st.write(f"{index}. {task}")

        st.markdown("### 8. Phased Work Plan")
        for phase, tasks in result["phased_plan"].items():
            with st.expander(phase, expanded=True):
                for task in tasks:
                    st.write(f"- {task}")

        st.markdown("### 9. Planning Risks")
        for risk in result["planning_risks"]:
            st.write(f"- {risk}")

        st.markdown("### 10. Completion Checklist")
        for item in result["completion_checklist"]:
            st.checkbox(item, value=False)

        task_plan_text = build_task_plan_text(assignment_text, result)

        st.download_button(
            label="Download Assignment Plan",
            data=task_plan_text,
            file_name="assignment_plan.txt",
            mime="text/plain",
        )

else:
    st.info("Paste assignment instructions and click the button to start.")


st.divider()

st.subheader("Agent Memory")

memory_data = load_memory()

if memory_data:
    st.write(f"Saved assignment plans: {len(memory_data)}")

    for index, item in enumerate(reversed(memory_data[-5:]), start=1):
        with st.expander(f"Memory {index}: {item['timestamp']}"):
            st.write(f"Priority: {item['priority']}")
            st.write(f"Workload: {item['workload']}")

            st.write("Assignment Components:")
            components = item.get("assignment_components", item.get("deliverables", []))

            if components:
                for component in components:
                    st.write(f"- {component}")
            else:
                st.write("- No clear assignment components detected.")

            st.write("Task Breakdown:")
            for task_index, task in enumerate(item.get("task_breakdown", []), start=1):
                st.write(f"{task_index}. {task}")

            st.write("Planning Risks:")
            risks = item.get("planning_risks", item.get("risks", []))
            if risks:
                for risk in risks:
                    st.write(f"- {risk}")
            else:
                st.write("- No planning risks saved.")

    if st.button("Clear Memory"):
        clear_memory()
        st.success("Agent memory has been cleared. Please refresh the page.")
else:
    st.info("No memory saved yet.")