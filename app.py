import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---
MODEL_NAME = "gemini-3-flash-preview"

# --- Page Setup ---
st.set_page_config(
    page_title="2025 Recap",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for "Milky White" / Humanistic Theme ---
st.markdown("""
    <style>
    /* Global Background and Font */
    .stApp {
        background-color: #fdfbf7; /* Milky White */
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
        color: #333333;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
        font-weight: normal;
        color: #2c2c2c;
    }

    /* Input Areas */
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
        font-size: 16px;
        color: #333333;
    }
    .stTextInput input {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
        color: #333333;
    }

    /* Buttons */
    .stButton>button {
        background-color: #f4f1ea;
        color: #333333;
        border: 1px solid #dcdcdc;
        font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #e8e5de;
        border-color: #bbbbbb;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Letter Container */
    .letter-box {
        background-color: #ffffff;
        padding: 40px;
        border: 1px solid #eaeaea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-top: 20px;
        line-height: 1.8;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Questions List ---
questions = [
    # Life
    "What was the single most memorable event of 2025 for you?",
    "Which relationship (friend, family, or partner) evolved the most this year?",
    "What is a new habit you formed that you are proud of?",
    "What was the most difficult challenge you faced in your personal life?",
    "What‘s the best thing you’ve ever bought this year?",
    "What makes you feel super excited?",
    
    # Study / Work
    "What was the most significant thing you learned this year?",
    "Did you achieve the academic or professional goals you set for yourself?",
    "What is a subject or topic you discovered a new passion for?",
    "Describe a moment where you felt completely in your element while working or studying.",
    
    # Texture of the Year
    "If you could describe 2025 with a single color (other than white), what would it be and why?",
    "Where did you spend the most time this year? (e.g., A specific library corner, a cafe, your desk, a park)",
    "What song or album will always remind you of this year?",
    "What was the 'flavor' of this year? (e.g., bitter, sweet, spicy, bland)",
    "Which book or movie resonated with you the most?",
    
    # Big Picture
    "How has your worldview changed compared to the beginning of the year?",
    "Who would you like to thank the most this year?",
    "What is something you let go of in 2025?",
    "What are you most grateful for right now?",
    "If you could send a message to yourself from January 1st, 2025, what would it be?",
    "What is the greatest achievement this year?",
    "Do you hate someone you didn‘t hate at this time last year?",
        
    # Future
    "What is your primary word or theme for 2026?",
    "What is one specific fear you want to conquer next year?",
    "Who do you want to spend more time with in the future?",
    "Where do you see yourself exactly one year from today?"
]

# --- App Logic ---

def generate_letter(answers, api_key):
    prompt = f"""
    You are a thoughtful, empathetic writer. Based on the following answers from a user reflecting on their year 2025, write a cohesive, warm, and humanistic summary letter addressed to them. If contain English answers, transform them into Chinese.

    The letter should:
    - Be written in Chinese.
    - Have a calm, reflective, and literary tone.
    - Not use emojis.
    - Synthesize the answers into a narrative flow rather than listing them.
    - Reflect on their life, studies, the 'texture' of their year, and their future hopes.
    - Be formatted beautifully as a letter (Dear [Name]..., Sincerely, Your 2025 Self).
    
    Here are the user's answers:
    {answers}
    """
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while connecting to the essence of your year: {str(e)}"

def main():
    st.title("Recap 2025")
    st.write("A quiet space to reflect on your year.")
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""

    total_questions = len(questions)

    # Introduction & API Key
    if st.session_state.current_step == 0:
        st.markdown(f"Take a moment to breathe. We will ask you {total_questions} questions to help uncover the story of your year.")
        
        st.markdown("---")
        st.write("Please provide your Google Gemini API Key to continue.")
        st.session_state.api_key = st.text_input("Gemini API Key", type="password", value=st.session_state.api_key)
        
        if st.button("Begin Reflection"):
            if st.session_state.api_key:
                st.session_state.current_step = 1
                st.rerun()
            else:
                st.error("Please enter a valid API Key.")

    # Questionnaire
    elif 1 <= st.session_state.current_step <= total_questions:
        q_index = st.session_state.current_step - 1
        question_text = questions[q_index]
        
        st.subheader(f"Question {st.session_state.current_step}/{total_questions}")
        st.write(question_text)
        
        # Use a unique key for each text area to preserve input if navigating back/forth
        # We also want to pre-fill it with the existing answer if they go back
        existing_answer = st.session_state.answers.get(question_text, "")
        answer = st.text_area("Your answer", height=150, value=existing_answer, key=f"q_{st.session_state.current_step}")
        
        col1, col2, col3 = st.columns([1, 1, 5])
        
        with col1:
            if st.button("Back"):
                # Save current answer before going back (optional, but good UX)
                st.session_state.answers[question_text] = answer
                st.session_state.current_step -= 1
                st.rerun()
                
        with col2:
            if st.button("Next"):
                st.session_state.answers[question_text] = answer
                st.session_state.current_step += 1
                st.rerun()
    
    # Generation & Result
    elif st.session_state.current_step == total_questions + 1:
        st.header("Your 2025 Letter")
        st.write("Gathering your thoughts...")
        
        # Format answers for the prompt
        formatted_answers = "\n".join([f"{q}\nAnswer: {a}" for q, a in st.session_state.answers.items()])
        
        with st.spinner("Writing..."):
            letter_content = generate_letter(formatted_answers, st.session_state.api_key)
        
        st.markdown(f'<div class="letter-box">{letter_content.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        
        st.write("")
        st.write("---")
        
        col1, col2 = st.columns([1, 5])
        with col1:
             if st.button("Back"):
                st.session_state.current_step = total_questions
                st.rerun()
        
        with col2:
            if st.button("Start Over"):
                st.session_state.current_step = 0
                st.session_state.answers = {}
                st.rerun()
if __name__ == "__main__":
    main()
