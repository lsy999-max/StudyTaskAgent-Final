# Design Evolution and Improvements

## Initial Design

The first version of StudyTask Agent focused on a simple assignment-to-task planning workflow. The user could paste assignment instructions into a Streamlit interface, and the system generated a basic task plan.

## Agent Loop Design

The system was then structured around an explicit agent loop: observe, analyse, decide, act, and remember. The agent observes assignment instructions, analyses requirements, makes planning decisions, generates planning outputs, and saves previous plans in memory.

## Improvements

The analysis module was improved to detect different assignment components, including written reports, presentations, coding tasks, data analysis tasks, design work, group work, testing evidence, peer evaluation, and submission requirements.

## Testing

The agent was tested with several assignment types, including essays, coding projects, data analysis reports, group presentations, design tasks, research proposals, and lab reports. These tests helped identify and fix false positives, such as confusing peer-reviewed academic sources with group work or confusing data flow in a design task with data analysis.

## Final Version

The final version includes cleaner constraint detection, improved workload estimation, local JSON memory, downloadable text output, screenshots, README documentation, and a demo video link. The prototype remains rule-based, which makes it easy to reproduce, but future work could add LLM-based language understanding and editable generated tasks.
