import streamlit as st # type: ignore
from main import grade_essay

st.markdown("<h1 style='text-align: center;'>ENEM Essay Evaluator</h1>", unsafe_allow_html=True)
st.subheader("""
             ENEM is Brazil's national high school exam, and its essay requires an argumentative text on a given social issue. The essay is evaluated based on structure, language, and proposed solutions.
             
             There are 5 competencies:
             1. Formal Writing Mastery
             2. Essay Comprehension
             3. Argument Organization
             4. Argumentation Techniques
             5. Intervention Proposal

             Each competency is individually scored from 0 to 200, and the scores are summed to calculate the final grade.
             
             This app is designed to analyze an ENEM essay, considering the theme, grading it, and providing detailed feedback.
            """)


theme = st.text_input("Enter the essay theme: ")
essay = st.text_area("Enter the essay text: ")

if st.button("Evaluate Essay"):
    try:
        # Check if both theme and essay are provided
        if not theme.strip():
            raise ValueError("The theme is missing. Please provide a valid theme.")
        if not essay.strip():
            raise ValueError("The essay is missing. Please provide a valid essay.")

        result = grade_essay(essay, theme)
        
        # Display results
        st.write(f"**Competence 1 (Formal Writing Mastery):** {result['formal_writing_mastery']}")
        st.write(f"**Competence 2 (Essay Comprehension):** {result['essay_comprehension']}")
        st.write(f"**Competence 3 (Argument Organization):** {result['argument_organization']}")
        st.write(f"**Competence 4 (Argumentation Mechanisms):** {result['argumentation_mechanisms']}")
        st.write(f"**Competence 5 (Intervention Proposal):** {result['intervention_proposal']}")
        st.write(f"**Final Score:** {result['final_score']}")
        st.write(f"**Score Explanation:** {result['score_explanation']}")
        
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
