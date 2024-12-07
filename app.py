import streamlit as st
import openai
from datetime import datetime
from dotenv import load_dotenv
import os

# Set Streamlit page config first (this should be the first Streamlit command)
st.set_page_config(page_title="Legal Adviser", page_icon=":guardsman:", layout="wide")

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
openai.api_key = os.getenv('API_KEY')

if openai.api_key:
    st.write("API Key successfully loaded!")
else:
    st.write("API Key not found.")

# State and city mapping for dropdown population
STATE_CITY_MAP = {
    "Maharashtra": ["Mumbai", "Pune", "Nashik"],
    "Goa": ["Panaji", "Mapusa", "Madgaon"],
    "Gujarat": ["Ahmedabad", "Vadodara"],
    "Kerala": ["Kozhikode"]
}

# Function to generate a GPT-4 case scenario
def generate_case(category, state, city, country, timeline):
    prompt = f"""
    Create a realistic case scenario for a law student or advocate for the specified category and ask the user for their solution. 
    Category: {category} 
    Place: {city}, {state}, {country} 
    Timeline: {timeline}.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Indian law related and legal case studies."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


# Function to analyze a user-provided solution
def analyze_solution(scenario, user_solution):
    prompt = f"""
    Scenario: {scenario}
    User Solution: {user_solution}

    Analyze the user's solution. Highlight strong points and identify flaws. Provide constructive feedback to improve their approach.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in critiquing solutions based on Indian Laws and rule"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


# Main function to handle navigation and app rendering
def main():
    st.set_page_config(page_title="Legal Help Case Assistant", layout="wide")
    st.title("Legal Help Case Assistant")
    menu = st.sidebar.selectbox("Menu", ["Home", "Case", "Analysis"], key="main_menu")

    if menu == "Home":
        homepage()
    elif menu == "Case":
        case_page()
    elif menu == "Analysis":
        analysis_page()


# Home Page
# Home Page with dynamic dropdowns for State and City
def homepage():
    st.header("Welcome to Legal Help")
    st.write(
        "Select a category to generate a case scenario and submit your solution for GPT's analysis."
    )

    # Dropdowns for the user to input state and dynamically populated city
    state = st.selectbox(
        "Select State",
        list(STATE_CITY_MAP.keys()),
        key="state_home"
    )

    city = st.selectbox(
        "Select City",
        STATE_CITY_MAP[state],
        key="city_home"
    )

    # Other input fields
    category = st.selectbox(
        "Select Category",
        ["Fraudulent practices and scams", "Pollution and contamination cases",
         "Trademark registration and infringement", "Harassment claims (e.g., sexual harassment)"],
        key="category_home"
    )

    # Timeline input field with validation
    timeline = st.text_input("Enter timeline (format YYYY-MM-DD)", key="timeline_home")

    if st.button("Continue", key="continue_home"):
        # Validate timeline
        try:
            datetime.strptime(timeline, "%Y-%m-%d")
        except ValueError:
            st.error("Invalid date format. Please use the format YYYY-MM-DD.")
            return

        if not state or not city or not timeline:
            st.error("Please fill out all fields to generate the case scenario.")
        else:
            with st.spinner("Generating case scenario..."):
                scenario = generate_case(category, state, city, "India", timeline)  # Updated country field to default "India"

            # Save the scenario into session state for continuity
            st.session_state.scenario = scenario
            st.session_state.user_solution = ""
            st.session_state.analysis_feedback = ""
            st.success("Case scenario generated successfully. Select Case Menu")
            st.query_params.update({"page": "Case"})
# def homepage():
#     st.header("Welcome to Legal Help")
#     st.write(
#         "Select a category to generate a case scenario and submit your solution for GPT's analysis."
#     )

#     # Dropdowns for the user to input state, city, country, timeline
#     category = st.selectbox(
#         "Select Category",
#         ["Fraudulent practices and scams", "Pollution and contamination cases",
#          "Trademark registration and infringement", "Harassment claims (e.g., sexual harassment)"],
#         key="category_home"
#     )
#     state = st.text_input("Enter State", key="state_home")
#     city = st.text_input("Enter City", key="city_home")
#     country = st.text_input("Enter Country", key="country_home")
#     timeline = st.text_input("Enter timeline (format YYYY-MM-DD)", key="timeline_home")

#     # Button to proceed to generate the case
#     if st.button("Continue", key="continue_home"):
#         # Validate timeline
#         try:
#             # Attempt to parse the date to check if it's valid
#             datetime.strptime(timeline, "%Y-%m-%d")
#         except ValueError:
#             st.error("Invalid date format. Please use the format YYYY-MM-DD.")
#             return

#         if not state or not city or not country or not timeline:
#             st.error("Please fill out all fields to generate the case scenario.")
#         else:
#             with st.spinner("Generating case scenario..."):
#                 scenario = generate_case(category, state, city, country, timeline)

#             # Save the scenario into session state for continuity
#             st.session_state.scenario = scenario
#             st.session_state.user_solution = ""
#             st.session_state.analysis_feedback = ""
#             st.success("Case scenario generated successfully.")
#             st.experimental_set_query_params(page="Case")


# Placeholder for the Case Page
def case_page():
    st.header("Case Scenario")
    st.write("Generated Case Scenario:")
    if 'scenario' in st.session_state:
        st.info(st.session_state.scenario)
    else:
        st.error("No case scenario found. Please return to Home and generate one.")
    
    user_solution = st.text_area("Submit Your Solution:", key="user_solution_case")
    if st.button("Submit Solution", key="submit_solution_case"):
        if user_solution:
            with st.spinner("Analyzing your solution..."):
                feedback = analyze_solution(st.session_state.scenario, user_solution)
                st.session_state.analysis_feedback = feedback
                st.success("Solution analyzed. Go to Analysis Menu.")
        else:
            st.error("You must enter a solution before submitting.")


# Analysis Page
def analysis_page():
    st.header("Analysis Results")
    if 'analysis_feedback' in st.session_state and st.session_state.analysis_feedback:
        st.write("GPT's Analysis/Feedback:")
        st.info(st.session_state.analysis_feedback)
    else:
        st.error("No analysis feedback available. Go back and submit a solution first.")

    if st.button("Close", key="close_analysis"):
        st.write("Thank you for using Legal Help Case Assistant.")


# Run the main navigation menu
if __name__ == "__main__":
    main()
