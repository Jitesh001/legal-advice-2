import streamlit as st
import openai
from datetime import datetime
from dotenv import load_dotenv
import os

# Set Streamlit page config first (outside the main function)
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
    "Maharashtra": ["Mumbai", "Pune", "Nashik", "Nagpur", "Aurangabad", "Thane"],
    "Goa": ["Panaji", "Mapusa", "Madgaon", "Vasco da Gama", "Margao"],
    "Gujarat": ["Ahmedabad", "Vadodara", "Surat", "Rajkot", "Bhavnagar", "Gandhinagar"],
    "Kerala": ["Kozhikode", "Thiruvananthapuram", "Kochi", "Kottayam", "Thrissur", "Kollam"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Allahabad", "Gorakhpur", "Meerut"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Munger"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Tirunelveli", "Erode"],
    "West Bengal": ["Kolkata", "Siliguri", "Asansol", "Durgapur", "Howrah", "Kolkata"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Kota", "Ajmer", "Bikaner", "Bhilwara"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar"],
    "Punjab": ["Chandigarh", "Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
    "Haryana": ["Gurugram", "Faridabad", "Hisar", "Ambala", "Karnal"],
    "Delhi": ["New Delhi", "Delhi Cantonment", "Dwarka", "Karol Bagh", "Connaught Place"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kakinada"],
    "Telangana": ["Hyderabad", "Warangal", "Khammam", "Karimnagar", "Nizamabad"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore", "Hubli", "Belagavi"],
    "Uttarakhand": ["Dehradun", "Nainital", "Haridwar", "Rishikesh", "Roorkee"],
    "Himachal Pradesh": ["Shimla", "Manali", "Kullu", "Dharamshala", "Kangra"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Korba", "Durg", "Jagdalpur"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Hazaribagh", "Bokaro Steel City"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Berhampur", "Rourkela", "Puri"],
    "Assam": ["Guwahati", "Dibrugarh", "Jorhat", "Silchar", "Nagaon"],
    "Nagaland": ["Kohima", "Dimapur"],
    "Meghalaya": ["Shillong", "Tura", "Jowai"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
    "Tripura": ["Agartala", "Udaipur", "Ambassa"],
    "Manipur": ["Imphal", "Thoubal", "Churachandpur"],
    "Sikkim": ["Gangtok", "Namchi", "Jorethang"],
    "Goa": ["Panaji", "Mapusa", "Madgaon", "Vasco da Gama", "Margao"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Minicoy"],
    "Andaman and Nicobar Islands": ["Port Blair", "Diglipur", "Havelock"],
    "Bengal": ["Kolkata", "Siliguri", "Asansol", "Durgapur"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla"],
    "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
    "Chandigarh": ["Chandigarh"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Munger"],
    "Sikkim": ["Gangtok", "Namchi", "Jorethang"]
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
    case_categories = [
    "Adoption and surrogacy law",
    "Alternative dispute resolution (ADR) and arbitration",
    "Antitrust and competition law",
    "Banking and financial regulations",
    "Bankruptcy and insolvency cases",
    "Civil rights violations (Discrimination, Police brutality)",
    "Consumer credit and debt collection",
    "Consumer protection and unfair trade practices",
    "Contract disputes and breaches",
    "Criminal defense and prosecution",
    "Cybercrime and data protection laws",
    "Cybersecurity laws and hacking cases",
    "Defamation and libel",
    "Employment law (Wages, Employee rights, Workplace discrimination)",
    "Environmental law and regulations",
    "Family law (Divorce, Child custody, Alimony)",
    "Fraudulent practices and scams",
    "Freedom of speech and expression (Censorship)",
    "Harassment claims (e.g., sexual harassment)",
    "Immigration law and visas",
    "Insurance claims and disputes",
    "Intellectual property (Patents, copyrights, trade secrets)",
    "Land acquisition and compensation issues",
    "Medical malpractice and negligence claims",
    "Pollution and contamination cases",
    "Personal injury and compensation claims",
    "Pollution and environmental contamination cases",
    "Public international law (Treaties, Diplomatic immunity)",
    "Real estate disputes (Property rights, Landlord-tenant issues)",
    "Securities and investment fraud",
    "Sports law (Contracts, Player disputes)",
    "Tax law and disputes",
    "Trademark registration and infringement",
    "Wills, trusts, and estate planning",
    "Workplace discrimination and employment claims",
    "Whistleblower claims and retaliation",
    "Consumer fraud and deceptive practices",
    "Product liability and safety claims",
    "Medical ethics and malpractice",
    "Negotiation and settlement law",
    "Mergers and acquisitions law",
    "Privacy law and data breach",
    "Regulatory compliance (industry-specific)",
    "Real estate law (Zoning, Property disputes)",
    "Debt recovery and collections",
    "Foreign investments and cross-border disputes",
    "Landlord-tenant disputes",
    "Legal malpractice and ethics violations",
    "Municipal law (Local governance, Zoning laws)",
    "Criminal appeals and post-conviction cases",
    "International arbitration and dispute resolution",
    "Social justice and civil liberties",
    "Consumer rights in e-commerce"
]

    category = st.selectbox(
        "Select Category",
        case_categories,
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
