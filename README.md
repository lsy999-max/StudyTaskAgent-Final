# StudyTask Agent: General Assignment Planning Agent

## Overview

StudyTask Agent is a small intelligent software agent prototype built with Python and Streamlit. It helps students turn assignment instructions into a structured work plan.

The user pastes assignment instructions into the web interface. The agent then observes the input text, analyses the assignment requirements, makes planning decisions, generates a task plan, saves the result to memory, and allows the user to download the generated plan.

This project was developed as a prototype for an intelligent software agent assignment.

---

## Agent Goal

The goal of StudyTask Agent is to help students understand and organise assignment requirements more effectively.

Given an assignment brief, the agent can:

- identify assignment components;
- detect deadlines and constraints;
- infer required skills;
- estimate priority and workload;
- generate a task breakdown;
- create a phased work plan;
- identify planning risks;
- generate a completion checklist;
- save previous plans in local memory;
- export the generated plan as a text file.

---

## Agent Workflow

The system follows this agent loop:

```text
observe -> analyse -> decide -> act -> remember
```

### Observe

The agent receives assignment instructions from the user through the Streamlit interface.

### Analyse

The agent analyses the text and extracts assignment components, deadlines, constraints, and required skills.

### Decide

The agent estimates the priority level, workload level, and possible planning risks.

### Act

The agent generates a task breakdown, phased work plan, completion checklist, and downloadable assignment plan.

### Remember

The agent saves generated plans to local memory using a JSON file.

---

## Features

- Streamlit web interface
- Rule-based assignment analysis
- Deadline and constraint detection
- Workload and priority estimation
- Planning risk detection
- Completion checklist generation
- Local memory storage
- Downloadable assignment plan
- Example assignment input

---

## Project Structure

```text
StudyTaskAgent-Final/
├── app.py
├── agent.py
├── memory.py
├── exporter.py
├── requirements.txt
├── README.md
├── DESIGN_EVOLUTION.md
├── screenshots/
└── .gitignore
```

| File | Purpose |
|---|---|
| `app.py` | Streamlit interface and main application logic |
| `agent.py` | Core agent logic for observing, analysing, deciding, and planning |
| `memory.py` | Saves and loads previous assignment plans |
| `exporter.py` | Builds a downloadable text version of the generated plan |
| `requirements.txt` | Lists required Python packages |
| `screenshots/` | Contains screenshots of the working prototype |
| `DESIGN_EVOLUTION.md` | Records the design evolution, testing process, and improvements made during development |

---

## Installation

Clone this repository:

```bash
git clone https://github.com/lsy999-max/StudyTaskAgent-Final.git
cd StudyTaskAgent-Final
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal. It is usually:

```text
http://localhost:8501
```

---

## Example Input

```text
Analyse the provided CSV dataset about student study habits. Produce at least three charts and write a maximum 4-page report discussing the main trends, limitations, and implications.
```

---

## Example Output

The agent generates:

- detected assignment components;
- detected deadlines;
- detected constraints;
- required skills;
- priority and workload estimation;
- task breakdown;
- phased work plan;
- planning risks;
- completion checklist;
- saved memory record;
- downloadable assignment plan.

---

## Screenshots

Screenshots of the working system are included in the `screenshots/` folder.

The screenshots show:

1. the agent workflow;
2. assignment input;
3. analysis output;
4. generated planning output;
5. memory and export functions.

---

## Limitations

This prototype uses a rule-based approach. It does not use an external LLM API. This makes the system easier to run and reproduce, but it also means the agent may not understand every possible wording of an assignment brief.

The current version works best with assignment instructions that clearly mention deliverables, deadlines, constraints, or task types.

---

## Future Work

Future improvements could include:

- integrating an LLM API for more flexible natural-language understanding;
- improving deadline parsing;
- supporting calendar export;
- supporting more assignment categories;
- adding a richer user interface;
- allowing users to edit and prioritise generated tasks.

---

## Technologies Used

- Python
- Streamlit
- JSON-based local memory
- Rule-based text processing

---

## Demo Video

Demo video link: https://drive.google.com/file/d/1nZ24f5CRpo90q3KI_RFMUvPwAtu4A5sx/view?usp=sharing

---

## Author

Siyun Liu  
This project was developed as an intelligent software agent prototype.
