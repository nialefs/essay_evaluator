# ENEM Essay Evaluator

ENEM is Brazil's national high school exam, and its essay requires an argumentative text on a given social issue. The essay is evaluated based on structure, language, and proposed solutions.
             
There are 5 competencies:
1. Formal Writing Mastery
2. Essay Comprehension
3. Argument Organization
4. Argumentation Techniques
5. Intervention Proposal

Each competency is individually scored from 0 to 200, and the scores are summed to calculate the final grade. This app is designed to analyze an ENEM essay, considering the theme, grading it, and providing detailed feedback.

## Features

- **Essay Evaluation:** Input your essay and its theme, and the app will automatically evaluate the essay across five competences.
- **LLM Integration:** Utilizes OpenAI's language models to perform the evaluation.
- **Real-time Feedback:** View detailed scores and explanations for each competence instantly after evaluation.
- **User-friendly Interface:** Built with Streamlit, providing a simple and clean UI.

## Competences Evaluated

- **Competence 1:** Formal Writing Mastery (Grammar, spelling, punctuation, coherence, and vocabulary usage).
- **Competence 2:** Essay Comprehension (Understanding the essay prompt and effectively using knowledge from different fields).
- **Competence 3:** Argument Organization (Selecting, organizing, and interpreting information to defend a point of view).
- **Competence 4:** Argumentation Mechanisms (Using linguistic tools to construct arguments).
- **Competence 5:** Intervention Proposal (Proposing a solution to the problem discussed in the essay).

## Project structure

.
├── essay_evaluator
│   └── __init__.py
├── evaluator_frontend.py
├── graph_essay_evaluator.png
├── main.py
├── poetry.lock
├── __pycache__
│   └── main.cpython-312.pyc
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nialefs/essay_evaluator.git
   cd essay_evaluator
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up environment variables. Create a `.env` file in the project root with the following contents:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```

4. Run your streamlit app with
    ```bash
    streamlit run evaluator_frontend.py
    ```

5. Install [ngrok]([https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://ngrok.com/&ved=2ahUKEwi07b63u46JAxWappUCHcPoGssQFnoECAgQAQ&usg=AOvVaw0qg9kSksx3M4uUIoIqmJI3]) following the steps provided in the website and add the link provided by streamlit:
    ```bash
    ngrok http http://192.168.1.104:8501
    ```

6. A link will be generated and you can share with other people

## Key dependencies:
- python = "^3.12"
- langgraph = "^0.2.35"
- langchain-openai = "^0.2.2"
- langchain-core = "^0.3.10"
- python-dotenv = "^1.0.1"
- streamlit = "^1.39.0"

## Acknowledgments
- [OpenAI](https://openai.com/) for GPT-4o-mini.
- [Streamlit](https://streamlit.io/) for front-end.
- [LangGraph](https://www.langchain.com/langgraph) for the LLM libraries.
- [Scoras Academy](https://www.linkedin.com/company/scoras-academy/posts/?feedView=all) and [Anderson Amaral](https://www.linkedin.com/in/andersonlamaral/) for the excellent content provided.
