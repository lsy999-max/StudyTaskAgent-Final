import re
from typing import Dict, List


class StudyTaskAgent:
    """
    A general assignment planning agent.

    The agent follows this loop:
    1. observe: read the assignment instructions
    2. analyse: extract assignment components, deadlines, constraints, and required skills
    3. decide: estimate priority, workload, and planning risks
    4. act: generate a task breakdown, phased plan, and completion checklist
    """

    def __init__(self, assignment_text: str):
        self.assignment_text = assignment_text.strip()
        self.lower_text = self.assignment_text.lower()

    def contains_keyword(self, keywords: List[str]) -> bool:
        """Check whether the text contains any keyword as a complete word or phrase."""
        for keyword in keywords:
            keyword = keyword.lower().strip()
            pattern = r"(?<![A-Za-z0-9])" + re.escape(keyword) + r"(?![A-Za-z0-9])"
            if re.search(pattern, self.lower_text):
                return True
        return False

    def observe(self) -> Dict:
        """Observe the assignment text and collect basic information."""
        words = self.assignment_text.split()
        sentences = re.split(r"[.!?\n]+", self.assignment_text)

        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "raw_text": self.assignment_text,
        }

    def extract_deadlines(self) -> List[str]:
        """Extract possible deadline expressions from the assignment text."""
        patterns = [
            r"\bdue\s+on\s+\d{1,2}\s?(January|February|March|April|May|June|July|August|September|October|November|December)\b",
            r"\bdue\s+by\s+\d{1,2}\s?(January|February|March|April|May|June|July|August|September|October|November|December)\b",
            r"\bnext\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            r"\bthis\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            r"\bby\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            r"\bbefore\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(\s+\d{1,2}(:\d{2})?\s?(am|pm)?)?\b",
            r"\bby\s+\d{1,2}(:\d{2})?\s?(am|pm)\s+on\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            r"\b\d{1,2}(:\d{2})?\s?(am|pm)\s+on\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
            r"\b\d{1,2}\s?(January|February|March|April|May|June|July|August|September|October|November|December)\b",
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s?\d{1,2}\b",
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
            r"\bweek\s?\d+\b",
            r"\btomorrow\b",
        ]

        deadlines = []
        for pattern in patterns:
            matches = re.finditer(pattern, self.assignment_text, flags=re.IGNORECASE)
            for match in matches:
                deadlines.append(match.group(0).strip())

        return self.remove_duplicate_items(deadlines)

    def remove_duplicate_items(self, items: List[str]) -> List[str]:
        """Remove duplicated expressions and keep the longer, more informative one."""
        unique_items = []

        for item in items:
            item = item.strip()
            should_add = True

            for existing in unique_items[:]:
                existing_lower = existing.lower()
                item_lower = item.lower()

                if item_lower == existing_lower:
                    should_add = False
                    break

                if item_lower in existing_lower:
                    should_add = False
                    break

                if existing_lower in item_lower:
                    unique_items.remove(existing)

            if should_add:
                unique_items.append(item)

        return unique_items

    def extract_assignment_components(self) -> List[str]:
        """Detect general assignment components."""
        component_keywords = {
            "written report": [
                "report", "essay", "paper", "write-up", "writeup",
                "reflection", "proposal", "document", "explanation",
                "design explanation", "lab report"
            ],
            "written summary": [
                "summary", "one-page summary", "short summary",
                "brief summary", "written summary"
            ],
            "presentation": [
                "presentation", "slides", "ppt", "powerpoint",
                "oral presentation", "speech", "oral pitch", "pitch"
            ],
            "research or reading": [
                "literature review", "reading", "research", "sources",
                "references", "citation", "bibliography", "academic sources",
                "peer-reviewed academic sources", "apa"
            ],
            "coding or implementation": [
                "code", "source code", "program", "java program", "python program",
                "javascript program", "implementation", "prototype", "software prototype",
                "build a program", "develop a program", "write code"
            ],
            "data analysis": [
                "dataset", "csv", "data analysis", "analyse the provided csv",
                "analyze the provided csv", "analyse the provided dataset",
                "analyze the provided dataset", "chart", "charts", "graph", "graphs",
                "visualisation", "visualization", "statistics", "summary statistics",
                "results table", "main trends", "limitations", "implications",
                "experiment results"
            ],
            "design work": [
                "design", "diagram", "architecture", "system architecture",
                "model", "prototype design", "wireframe", "user flow",
                "data flow", "design explanation"
            ],
            "testing evidence": [
                "test cases", "testing evidence", "tests", "unit tests",
                "sample cases", "test results"
            ],
            "media or recording": [
                "video", "recording", "audio", "poster", "demo"
            ],
            "group work": [
                "group", "groups", "team", "collaboration",
                "partner", "partners", "group of", "groups of",
                "group project", "team project", "each group"
            ],
            "peer evaluation": [
                "peer evaluation", "peer evaluation form",
                "peer assessment", "peer feedback"
            ],
            "submission package": [
                "submit", "upload", "file", "files", "link", "appendix",
                "attachment", "submission", "canvas"
            ],
        }

        detected = []
        for component, keywords in component_keywords.items():
            if self.contains_keyword(keywords):
                detected.append(component)

        return detected

    def extract_constraints(self) -> List[str]:
        """Detect assignment constraints such as word limits, page limits, chart requirements, source requirements, and time limits."""
        number_words = (
            "one|two|three|four|five|six|seven|eight|nine|ten|"
            "eleven|twelve|fifteen|twenty"
        )

        patterns = [
            r"\bat least\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+charts?\b",
            r"\bat least\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+graphs?\b",
            r"\bat least\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+tables?\b",
            r"\bat least\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+sources?\b",
            r"\bat least\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+academic sources?\b",
            r"\bat least\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+peer-reviewed academic sources?\b",
            r"\bmaximum\s+\d+\s?[- ]?\s?pages?\b",
            r"\bmaximum\s+\d+\s?[- ]?\s?page\b",
            r"\bmaximum\s+(one|two|three|four|five|six|seven|eight|nine|ten)\s?[- ]?\s?pages?\b",
            r"\bmaximum\s+(one|two|three|four|five|six|seven|eight|nine|ten)\s?[- ]?\s?page\b",
            r"\bno more than\s+\d+\s?[- ]?\s?pages?\b",
            r"\bno more than\s+\d+\s?[- ]?\s?page\b",
            r"\bno more than\s+\d+\s?[- ]?\s?words?\b",
            r"\b\d+\s?[- ]?\s?words?\b",
            r"\b\d+\s?[- ]?\s?pages?\b",
            r"\b\d+\s?[- ]?\s?minutes?\b",
            rf"\b({number_words})[- ]?words?\b",
            rf"\b({number_words})[- ]?pages?\b",
            rf"\b({number_words})[- ]?page\b",
            rf"\b({number_words})[- ]?minutes?\b",
            rf"\b({number_words})[- ]?minute\b",
        ]

        constraints = []
        for pattern in patterns:
            matches = re.finditer(pattern, self.assignment_text, flags=re.IGNORECASE)
            for match in matches:
                constraints.append(match.group(0).strip())

        return self.remove_duplicate_items(constraints)

    def extract_required_skills(self) -> List[str]:
        """Detect broad skills or tools that may be needed."""
        skill_keywords = {
            "academic writing": [
                "report", "essay", "reflection", "proposal",
                "paper", "summary", "document", "explanation",
                "lab report"
            ],
            "presentation skills": [
                "presentation", "slides", "speech", "oral", "pitch"
            ],
            "research skills": [
                "research", "literature", "references", "sources",
                "citation", "academic sources", "peer-reviewed academic sources",
                "apa", "bibliography"
            ],
            "programming skills": [
                "code", "source code", "program", "java program", "python program",
                "javascript program", "implementation", "software prototype",
                "write code"
            ],
            "data analysis skills": [
                "dataset", "csv", "data analysis", "statistics",
                "chart", "charts", "graph", "graphs", "analysis",
                "analyse the provided csv", "analyze the provided csv",
                "analyse the provided dataset", "analyze the provided dataset",
                "results table", "main trends", "experiment results"
            ],
            "design skills": [
                "design", "diagram", "architecture", "wireframe",
                "model", "user flow", "data flow", "design explanation",
                "system architecture"
            ],
            "testing skills": [
                "test cases", "testing evidence", "tests", "unit tests",
                "sample cases", "test results"
            ],
            "team coordination": [
                "group", "groups", "team", "collaboration",
                "partner", "partners", "group project", "team project",
                "each group"
            ],
            "time management": [
                "deadline", "due", "week", "submit", "by", "next",
                "before", "tomorrow"
            ],
        }

        detected = []
        for skill, keywords in skill_keywords.items():
            if self.contains_keyword(keywords):
                detected.append(skill)

        return detected

    def estimate_priority(self, components: List[str], deadlines: List[str], constraints: List[str]) -> str:
        """Estimate assignment priority."""
        if deadlines or len(components) >= 4 or len(constraints) >= 2:
            return "High"
        if len(components) >= 2:
            return "Medium"
        return "Low"

    def estimate_workload(self, word_count: int, components: List[str], constraints: List[str]) -> str:
        """Estimate rough workload level."""
        constraint_text = " ".join(constraints).lower()

        high_word_count_patterns = [
            r"\b1[5-9]\d{2}\s?[- ]?\s?words?\b",
            r"\b[2-9]\d{3}\s?[- ]?\s?words?\b",
        ]

        high_source_patterns = [
            r"\bat least\s+(five|six|seven|eight|nine|ten|\d+)\s+.*sources?\b",
            r"\b(five|six|seven|eight|nine|ten|\d+)\s+.*sources?\b",
            r"\bpeer-reviewed academic sources?\b",
        ]

        chart_requirement_patterns = [
            r"\bat least\s+(three|four|five|six|seven|eight|nine|ten|\d+)\s+charts?\b",
            r"\bat least\s+(three|four|five|six|seven|eight|nine|ten|\d+)\s+graphs?\b",
        ]

        substantive_components = [
            component for component in components
            if component not in ["submission package"]
        ]

        has_high_word_count = any(
            re.search(pattern, constraint_text, flags=re.IGNORECASE)
            for pattern in high_word_count_patterns
        )

        has_high_source_requirement = any(
            re.search(pattern, constraint_text, flags=re.IGNORECASE)
            for pattern in high_source_patterns
        )

        has_chart_requirement = any(
            re.search(pattern, constraint_text, flags=re.IGNORECASE)
            for pattern in chart_requirement_patterns
        )

        if (
            word_count > 180
            or len(substantive_components) >= 5
            or len(constraints) >= 4
            or (has_high_word_count and has_high_source_requirement)
            or ("data analysis" in components and "written report" in components and has_chart_requirement)
        ):
            return "Large"

        if (
            word_count > 80
            or len(substantive_components) >= 3
            or has_high_word_count
            or has_high_source_requirement
            or has_chart_requirement
            or len(constraints) >= 2
        ):
            return "Medium"

        return "Small"

    def generate_task_breakdown(self, components: List[str]) -> List[str]:
        """Generate a practical task breakdown based on detected assignment components."""
        tasks = [
            "Read the assignment instructions carefully.",
            "Identify the main goal, marking criteria, and required outputs.",
        ]

        if "research or reading" in components:
            tasks.extend([
                "Collect relevant sources or course materials.",
                "Take notes and identify useful evidence.",
                "Record source details for referencing."
            ])

        if "written report" in components:
            tasks.extend([
                "Create an outline for the written work.",
                "Draft the main sections.",
                "Revise the writing for clarity and structure."
            ])

        if "written summary" in components:
            tasks.extend([
                "Identify the key points that must be summarised.",
                "Write the required summary in a concise format.",
                "Check that the summary follows the required length or format."
            ])

        if "presentation" in components:
            tasks.extend([
                "Prepare the slide structure.",
                "Write short speaking notes.",
                "Rehearse the presentation timing."
            ])

        if "coding or implementation" in components:
            coding_tasks = [
                "Design the system or program structure.",
                "Implement the core functionality.",
            ]

            if "testing evidence" not in components:
                coding_tasks.append("Test the implementation with sample cases.")

            tasks.extend(coding_tasks)

        if "testing evidence" in components:
            tasks.extend([
                "Prepare test cases for the main functionality.",
                "Run the test cases and record the results.",
                "Check that the testing evidence matches the assignment requirements."
            ])

        if "data analysis" in components:
            tasks.extend([
                "Inspect the dataset and clean obvious issues.",
                "Run the required analysis.",
                "Prepare charts or tables to communicate the findings.",
                "Check whether the analysis results support the written discussion."
            ])

        if "design work" in components:
            tasks.extend([
                "Sketch the design or architecture.",
                "Refine the design based on the assignment requirements."
            ])

        if "media or recording" in components:
            tasks.extend([
                "Prepare the recording or media content.",
                "Check that the final media file is clear and accessible."
            ])

        if "group work" in components:
            tasks.extend([
                "Divide responsibilities among group members.",
                "Schedule a short progress check before the deadline."
            ])

        if "peer evaluation" in components:
            tasks.extend([
                "Complete the required peer evaluation or feedback form.",
                "Check whether peer evaluation is submitted separately."
            ])

        tasks.append("Check the final output against the assignment requirements before submission.")

        return list(dict.fromkeys(tasks))

    def generate_phased_plan(self, components: List[str]) -> Dict[str, List[str]]:
        """Generate a phased work plan that can apply to many types of assignments."""
        phased_plan = {
            "Phase 1: Understand the Assignment": [
                "Read the brief carefully.",
                "Identify the required outputs, constraints, and marking criteria.",
                "Clarify any unclear requirements early."
            ],
            "Phase 2: Prepare Materials": [
                "Collect notes, examples, references, data, or technical resources needed for the task.",
                "Create a simple outline or work structure."
            ],
            "Phase 3: Produce the Main Work": [
                "Complete the main written, technical, analytical, design, or presentation component.",
                "Keep checking that the work matches the assignment requirements."
            ],
            "Phase 4: Review and Finalise": [
                "Proofread or test the work.",
                "Check formatting, file names, links, and required evidence.",
                "Submit only after confirming all required parts are included."
            ],
        }

        if "written summary" in components:
            phased_plan["Phase 3: Produce the Main Work"].append(
                "Write and refine the required summary."
            )

        if "coding or implementation" in components:
            phased_plan["Phase 3: Produce the Main Work"].append(
                "Test the implementation and fix obvious errors."
            )

        if "testing evidence" in components:
            phased_plan["Phase 4: Review and Finalise"].append(
                "Prepare and review testing evidence before submission."
            )

        if "data analysis" in components:
            phased_plan["Phase 3: Produce the Main Work"].append(
                "Clean the data, run the analysis, and prepare charts or tables."
            )

        if "presentation" in components:
            phased_plan["Phase 4: Review and Finalise"].append(
                "Rehearse the presentation and check timing."
            )

        if "group work" in components:
            phased_plan["Phase 2: Prepare Materials"].append(
                "Agree on roles and communication arrangements with the group."
            )

        if "peer evaluation" in components:
            phased_plan["Phase 4: Review and Finalise"].append(
                "Complete the peer evaluation or feedback requirement."
            )

        if "research or reading" in components:
            phased_plan["Phase 2: Prepare Materials"].append(
                "Record source details for later referencing."
            )

        return phased_plan

    def detect_planning_risks(self, components: List[str], deadlines: List[str], constraints: List[str]) -> List[str]:
        """Detect general planning risks for many types of assignments."""
        risks = []

        if not deadlines:
            risks.append("No clear deadline was detected, so the user should manually confirm the due date.")

        if len(components) >= 4:
            risks.append("This assignment contains multiple components, so the workload may be underestimated.")

        if constraints:
            risks.append("The assignment includes constraints such as word, page, source, chart, or time limits, which should be checked before final submission.")

        if "written report" in components or "written summary" in components:
            risks.append("Written work may take longer than expected because outlining, drafting, and editing are separate steps.")

        if "presentation" in components:
            risks.append("Presentation work requires rehearsal time, not only slide preparation.")

        if "coding or implementation" in components:
            risks.append("Technical work may require extra time for testing and debugging.")

        if "testing evidence" in components:
            risks.append("Testing evidence may be incomplete if test cases are not planned before final submission.")

        if "data analysis" in components:
            risks.append("Data analysis work may require extra time for data cleaning, checking results, and preparing clear charts or tables.")

        if "research or reading" in components:
            risks.append("Research-based work requires time to find, evaluate, and reference sources properly.")

        if "group work" in components:
            risks.append("Group work may be delayed if responsibilities and communication are unclear.")

        if "peer evaluation" in components:
            risks.append("Peer evaluation may be missed if it is separate from the main assignment submission.")

        if not risks:
            risks.append("No major planning risk was detected, but the final requirements should still be checked carefully.")

        return risks

    def generate_completion_checklist(self, components: List[str], constraints: List[str]) -> List[str]:
        """Generate a general completion checklist based on detected assignment components."""
        checklist = [
            "Assignment brief reviewed",
            "Main requirements identified",
        ]

        if "research or reading" in components:
            checklist.extend([
                "Relevant sources collected",
                "References or citations checked"
            ])

        if "written report" in components:
            checklist.extend([
                "Written draft completed",
                "Writing revised and proofread"
            ])

        if "written summary" in components:
            checklist.extend([
                "Summary written",
                "Summary length and format checked"
            ])

        if "presentation" in components:
            checklist.extend([
                "Slides or speaking materials prepared",
                "Presentation rehearsed"
            ])

        if "coding or implementation" in components:
            checklist.extend([
                "Core implementation completed",
                "Program tested with sample input"
            ])

        if "testing evidence" in components:
            checklist.extend([
                "Test cases prepared",
                "Testing evidence reviewed"
            ])

        if "data analysis" in components:
            checklist.extend([
                "Dataset checked",
                "Analysis results reviewed",
                "Charts or tables checked"
            ])

        if "design work" in components:
            checklist.append("Design or diagram reviewed")

        if "media or recording" in components:
            checklist.append("Media or recording checked for accessibility")

        if "group work" in components:
            checklist.append("Group contribution and responsibilities confirmed")

        if "peer evaluation" in components:
            checklist.append("Peer evaluation or feedback form completed")

        if constraints:
            checklist.append("Word, page, source, chart, time, or format limits checked")

        checklist.append("Final files and submission requirements checked")

        return list(dict.fromkeys(checklist))

    def run(self) -> Dict:
        """Run the full agent process."""
        observation = self.observe()
        deadlines = self.extract_deadlines()
        components = self.extract_assignment_components()
        constraints = self.extract_constraints()
        skills = self.extract_required_skills()

        priority = self.estimate_priority(components, deadlines, constraints)
        workload = self.estimate_workload(observation["word_count"], components, constraints)
        task_breakdown = self.generate_task_breakdown(components)
        phased_plan = self.generate_phased_plan(components)
        planning_risks = self.detect_planning_risks(components, deadlines, constraints)
        completion_checklist = self.generate_completion_checklist(components, constraints)

        return {
            "observation": observation,
            "deadlines": deadlines,
            "assignment_components": components,
            "constraints": constraints,
            "required_skills": skills,
            "priority": priority,
            "workload": workload,
            "task_breakdown": task_breakdown,
            "phased_plan": phased_plan,
            "planning_risks": planning_risks,
            "completion_checklist": completion_checklist,
        }