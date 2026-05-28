import json
import os
from datetime import datetime
from typing import Dict, List


MEMORY_FILE = "outputs/memory.json"


def ensure_memory_file() -> None:
    """Create the outputs folder and memory file if they do not exist."""
    os.makedirs("outputs", exist_ok=True)

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def save_memory(assignment_text: str, result: Dict) -> None:
    """Save one agent run to long-term memory."""
    ensure_memory_file()

    memory_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "assignment_text": assignment_text,
        "assignment_components": result.get("assignment_components", []),
        "deadlines": result.get("deadlines", []),
        "constraints": result.get("constraints", []),
        "required_skills": result.get("required_skills", []),
        "priority": result.get("priority", "Unknown"),
        "workload": result.get("workload", "Unknown"),
        "task_breakdown": result.get("task_breakdown", []),
        "phased_plan": result.get("phased_plan", {}),
        "planning_risks": result.get("planning_risks", []),
        "completion_checklist": result.get("completion_checklist", []),
    }

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        memory_data = json.load(file)

    memory_data.append(memory_entry)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory_data, file, indent=4, ensure_ascii=False)


def load_memory() -> List[Dict]:
    """Load all saved agent memories."""
    ensure_memory_file()

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def clear_memory() -> None:
    """Clear all saved memory."""
    os.makedirs("outputs", exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)