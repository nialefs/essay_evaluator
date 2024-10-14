from typing import TypedDict
from langgraph.graph import StateGraph, START, END # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import re

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "essay_evaluator"

# Defining the State
class State(TypedDict):
    """Represents the status of the writing evaluation process"""
    essay: str
    theme: str
    formal_writing_mastery: int
    essay_comprehension: int
    argument_organization: int
    argumentation_mechanisms: int
    intervention_proposal: int
    score_explanation: str
    final_score: int

# Initializes the ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Defining the functions used in the grading process, including score extraction and individual grading components
def extract_score_and_explanation(content: str, competence_number:int) -> int:
    """Extracts both the score and explanation from the LLM response"""
    score_match = re.search(rf'Pontuação - Competência {competence_number}:\s*(\d+(\.\d+)?)', content)
    score_explanation = content.split(f'Pontuação - Competência {competence_number}: ')[-1]
    
    score = int(score_match.group(1)) if score_match else 0
    return score, score_explanation

def check_formal_writing_mastery(state: State) -> State:
    """Checks competence 1: Demonstrate mastery of the formal written form of the Portuguese language"""
    prompt = ChatPromptTemplate.from_template(
        """
        Analise a redação com base na capacidade do candidato de usar corretamente a modalidade formal da língua portuguesa em sua redação.
        Observe principalmente: gramática, ortografia, pontuação, coerência gramatical e vocabulário adequado.
        Erros podem diminuir a pontuação conforme sua gravidade.
        Se o candidato cometer muitos erros ou usar uma linguagem muito informal, pode perder mais pontos.
        O ideal é que a redação seja clara, objetiva e gramaticalmente correta.
        Forneça uma pontuação de 0 a 200.
        Explique sua linha de racioncínio antes de calcular a nota.
        Sua resposta deve começar com 'Pontuação - Competência 1: ' seguida da pontuação numérica.\n\nRedação: {essay}
        """
    )
    result = llm.invoke(prompt.format(essay=state['essay']))
    try:
        score, score_explanation = extract_score_and_explanation(result.content, 1)
        state['formal_writing_mastery'] = score
        state['score_explanation'] += f"\n**Competência 1:** {score_explanation}\n"
    except ValueError as e:
        print(f"Error in formal_writing_mastery: {e}")
        state['formal_writing_mastery'] = 0

    return state

def check_essay_comprehension(state: State) -> State:
    """Checks competence 2: Understand the writing proposal and apply concepts from various fields of knowledge to develop the topic, within the structural limits of a discursive-argumentative prose text"""
    prompt = ChatPromptTemplate.from_template(
        """
        Analise a redação com base na capacidade do candidato de compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, respeitando os limites estruturais do texto dissertativo-argumentativo em prosa.
        Isso significa que o candidato precisa demonstrar que entendeu o tema proposto na redação e que sabe utilizar conteúdos de diversas disciplinas para elaborar uma argumentação coerente e bem fundamentada sobre o tema, dentro do formato exigido (dissertação argumentativa).
        O tema proposto da redação é: {theme}.
        Forneça uma pontuação de 0 a 200.
        Explique sua linha de racioncínio antes de calcular a nota.
        Sua resposta deve começar com 'Pontuação - Competência 2: ' seguida da pontuação numérica.\n\nRedação: {essay}
        """
    )
    result = llm.invoke(prompt.format(theme=state['theme'], essay=state['essay']))
    try:
        score, score_explanation = extract_score_and_explanation(result.content, 2)
        state['essay_comprehension'] = score
        state['score_explanation'] += f"\n**Competência 2:** {score_explanation}\n"
    except ValueError as e:
        print(f"Error in essay_comprehension: {e}")
        state['essay_comprehension'] = 0

    return state

def check_argument_organization(state: State) -> State:
    """Checks competence 3: Select, relate, organize, and interpret information, facts, opinions, and arguments in defense of a point of view"""
    prompt = ChatPromptTemplate.from_template(
        """
        Avalie a capacidade do candidato de construir e sustentar uma argumentação coerente e bem fundamentada em seu texto dissertativo-argumentativo.
        Para isso, é necessário saber interpretar corretamente as informações e selecionar dados relevantes, organizando-os de forma a defender uma ideia ou ponto de vista.
        Forneça uma pontuação de 0 a 200.
        Explique sua linha de racioncínio antes de calcular a nota.
        Sua resposta deve começar com 'Pontuação - Competência 3: ' seguida da pontuação numérica.\n\nRedação: {essay}
        """
    )
    result = llm.invoke(prompt.format(essay=state['essay']))
    try:
        score, score_explanation = extract_score_and_explanation(result.content, 3)
        state['argumentation_mechanisms'] = score
        state['score_explanation'] += f"\n**Competência 3:** {score_explanation}\n"
    except ValueError as e:
        print(f"Error in argument_organization: {e}")
        state['argument_organization'] = 0

    return state


def check_argumentation_mechanisms(state: State) -> State:
    """Checks competence 4: Demonstrate knowledge of the linguistic mechanisms necessary for constructing an argument"""
    prompt = ChatPromptTemplate.from_template("""
    Avalie o texto do candidato com base na demonstração de conhecimento dos mecanismos linguísticos necessários para a construção da argumentação.
    O candidato deve ser capaz de usar os recursos linguísticos (como coesão, coerência, conectores, e outros elementos de organização textual) de forma adequada para estruturar suas ideias e argumentos no texto, promovendo a clareza e a fluidez na comunicação escrita.
    Forneça uma pontuação de 0 a 200.
    Explique sua linha de racioncínio antes de calcular a nota.
    Sua resposta deve começar com 'Pontuação - Competência 4: ' seguida da pontuação numérica.\n\nRedação: {essay}
    """)
    result = llm.invoke(prompt.format(essay=state['essay']))
    try:
        score, score_explanation = extract_score_and_explanation(result.content, 4)
        state['argumentation_mechanisms'] = score
        state['score_explanation'] += f"\n**Competência 4:** {score_explanation}\n"
    except ValueError as e:
        print(f"Error in argumentation_mechanisms: {e}")
        state['argumentation_mechanisms'] = 0

    return state


def check_intervention_proposal(state: State) -> State:
    """Develop an intervention proposal for the addressed issue, respecting human rights"""
    prompt = ChatPromptTemplate.from_template("""
    Avalie a forma que o candidato apresenta uma solução viável e detalhada para o problema discutido no seu texto dissertativo-argumentativo, considerando princípios como inclusão social, igualdade e respeito à dignidade humana.
    A proposta de intervenção deve ser clara e estar relacionada com o tema central da redação.
    O tema proposto da redação é: {theme}.
    Forneça uma pontuação de 0 a 200.
    Explique sua linha de racioncínio antes de calcular a nota.
    Sua resposta deve começar com 'Pontuação - Competência 5: ' seguida da pontuação numérica.\n\nRedação: {essay}
    """)
    
    result = llm.invoke(prompt.format(theme=state['theme'], essay=state['essay']))
    try:
        score, score_explanation = extract_score_and_explanation(result.content, 5)
        state['intervention_proposal'] = score
        state['score_explanation'] += f"\n**Competência 5:** {score_explanation}\n"
    except ValueError as e:
        print(f"Error in intervention_proposal: {e}")
        state['intervention_proposal'] = 0

    return state

def calculate_final_score(state: State) -> State:
    """Calcula a pontuação final com base nas pontuações das competências individuais"""
    state['final_score'] = (
        state["formal_writing_mastery"] +
        state["essay_comprehension"] +
        state["argument_organization"] +
        state["argumentation_mechanisms"] +
        state["intervention_proposal"]
    )

    return state

# Defining the avaliation flow using StateGraph

workflow = StateGraph(State)

# Adding the nodes
workflow.add_node("check_formal_writing_mastery", check_formal_writing_mastery)
workflow.add_node("check_essay_comprehension", check_essay_comprehension)
workflow.add_node("check_argument_organization", check_argument_organization)
workflow.add_node("check_argumentation_mechanisms", check_argumentation_mechanisms)
workflow.add_node("check_intervention_proposal", check_intervention_proposal)
workflow.add_node("calculate_final_score", calculate_final_score)

# Adding the edges
workflow.add_edge(START, "check_formal_writing_mastery")
workflow.add_edge("check_formal_writing_mastery", "check_essay_comprehension")
workflow.add_edge("check_essay_comprehension", "check_argument_organization")
workflow.add_edge("check_argument_organization", "check_argumentation_mechanisms")
workflow.add_edge("check_argumentation_mechanisms", "check_intervention_proposal")
workflow.add_edge("check_intervention_proposal", "calculate_final_score")
workflow.add_edge("calculate_final_score", END)

app = workflow.compile()

# with open("./graph_essay_evaluator.png", "wb") as image: 
#     image.write(app.get_graph().draw_mermaid_png())

def grade_essay(essay: str, theme: str) -> dict:
    """Evaluate the provided essay using the defined workflow"""
    initial_state = State(
        essay=essay,
        theme=theme,
        explanation='',
        formal_writing_mastery=0,
        essay_comprehension=0,
        argument_organization=0,
        argumentation_mechanisms=0,
        intervention_proposal=0,
        score_explanation="",
        final_score=0
    )
    result = app.invoke(initial_state)
    return result