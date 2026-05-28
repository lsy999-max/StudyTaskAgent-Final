from typing import Dict


def build_task_plan_text(assignment_text: str, result: Dict) -> str:
    """Build a downloadable plain-text task plan."""

    lines = []

    lines.append("StudyTask Agent: Generated Assignment Plan")
    lines.append("=" * 50)
    lines.append("")

    lines.append("Original Assignment Instructions")
    lines.append("-" * 35)
    lines.append(assignment_text.strip())
    lines.append("")

    lines.append("Agent Observation")
    lines.append("-" * 35)
    lines.append(f"Word count: {result['observation']['word_count']}")
    lines.append(f"Sentence count: {result['observation']['sentence_count']}")
    lines.append("")

    lines.append("Detected Assignment Components")
    lines.append("-" * 35)
    if result["assignment_components"]:
        for item in result["assignment_components"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No clear assignment components detected.")
    lines.append("")

    lines.append("Detected Deadlines")
    lines.append("-" * 35)
    if result["deadlines"]:
        for item in result["deadlines"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No clear deadline detected.")
    lines.append("")

    lines.append("Detected Constraints")
    lines.append("-" * 35)
    if result["constraints"]:
        for item in result["constraints"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No clear constraints detected.")
    lines.append("")

    lines.append("Required Skills")
    lines.append("-" * 35)
    if result["required_skills"]:
        for item in result["required_skills"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No specific skills detected.")
    lines.append("")

    lines.append("Agent Decision")
    lines.append("-" * 35)
    lines.append(f"Priority level: {result['priority']}")
    lines.append(f"Estimated workload: {result['workload']}")
    lines.append("")

    lines.append("Task Breakdown")
    lines.append("-" * 35)
    for index, task in enumerate(result["task_breakdown"], start=1):
        lines.append(f"{index}. {task}")
    lines.append("")

    lines.append("Phased Work Plan")
    lines.append("-" * 35)
    for phase, tasks in result["phased_plan"].items():
        lines.append(phase)
        for task in tasks:
            lines.append(f"- {task}")
        lines.append("")

    lines.append("Planning Risks")
    lines.append("-" * 35)
    for risk in result["planning_risks"]:
        lines.append(f"- {risk}")
    lines.append("")

    lines.append("Completion Checklist")
    lines.append("-" * 35)
    for item in result["completion_checklist"]:
        lines.append(f"[ ] {item}")
    lines.append("")

    lines.append("Agent Workflow")
    lines.append("-" * 35)
    lines.append("observe -> analyse -> decide -> act -> remember")

    return "\n".join(lines)