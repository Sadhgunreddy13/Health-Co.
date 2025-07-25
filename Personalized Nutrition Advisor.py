import streamlit as st
import google.generativeai as genai
import base64
import os


# Configure Google Gemini AI
GENAI_API_KEY = "AIzaSyAgLTzLRE9fRVH5aaLeaKCYDgcNVt-2UWw"  # Replace with your actual API key
genai.configure(api_key=GENAI_API_KEY)

# Set Streamlit page configuration
st.set_page_config(page_title="Health and Co", page_icon="🩺", layout="wide")

# Function to set background image and font color
def set_background(image_file):
    """
    Uses Streamlit's built-in markdown function to set a background image and font color.
    """
    page_bg_img = f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{image_file}") no-repeat center center fixed;
        background-size: cover;
        color: black;  /* Set default font color to black */
    }}
    /* Change font color for form labels and user questions */
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {{
        color: black !important;  /* Make user question labels black */
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to encode an image file to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load and apply the background image (Ensure background.png exists)
image_base64 = get_base64_image("background.png")  # Change to your PNG file
set_background(image_base64)

# Display the logo (Make sure logo.png exists)
st.image("logo.png", width=150)  # You can also use PNG for the logo

# App title and description
st.title("Health & Co - Personalized Nutrition Advisor")
st.markdown("### Your AI-powered nutrition companion for a healthier life \n ### Welcome to HEALTH & CO")

# Function to calculate BMI
def calculate_bmi(weight, height_in_feet):
    height_in_meters = height_in_feet * 0.3048
    try:
        bmi = weight / (height_in_meters ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return "Height cannot be zero."

# Function to determine nutrition problem based on BMI
def determine_nutrition_problem(bmi, age, gender):
    if bmi < 18.5:
        return "Malnutrition (underweight)"
    elif 18.5 <= bmi < 24.9:
        return "Healthy weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    elif bmi >= 30:
        return "Obesity"
    
    if age >= 65:
        return "Potential age-related malnutrition"
    return "Undetermined nutrition problem"

# Function to determine dietary habits
def determine_dietary_habits(dietary_habits):
    fruits = int(dietary_habits["fruits"])
    vegetables = int(dietary_habits["vegetables"])
    protein_sources = int(dietary_habits["protein_sources"])
    whole_grains = int(dietary_habits["whole_grains"])
    micronutrient_deficiency = dietary_habits["micronutrient_deficiency"]

    if fruits < 3 or vegetables < 3 or protein_sources < 2 or whole_grains < 2:
        return "Poor dietary diversity"

    if micronutrient_deficiency.lower() != "none":
        return f"Possible micronutrient deficiency (e.g., {micronutrient_deficiency})"

    return "Balanced diet"

# Function to get personalized nutrition advice
def get_nutrition_advice(category, age, gender, health_issues, weight, height_in_feet, bmi, dietary_habits):
    prompts = {
        "Malnutrition (underweight)": "Explain how to prevent and treat malnutrition, including essential nutrients and diet recommendations.",
        "Healthy weight": "Provide general health and nutrition advice for maintaining a healthy weight.",
        "Overweight": "Provide expert advice on managing overweight, including diet, exercise, and healthy lifestyle changes.",
        "Obesity": "Give expert advice on managing obesity, including diet, exercise, and healthy lifestyle changes.",
        "Potential age-related malnutrition": "Provide nutrition advice for elderly individuals, focusing on preventing age-related malnutrition.",
        "Poor dietary diversity": "Provide advice on how to improve dietary diversity, including incorporating more food groups.",
        "Possible micronutrient deficiency": "Provide advice on addressing micronutrient deficiencies, including food sources and supplementation recommendations.",
        "Balanced diet": "Give general advice on maintaining a balanced and healthy diet."
    }

    user_prompt = (
        f"{prompts[category]} Consider a {gender}, {age} years old, with a weight of {weight} kg, "
        f"height of {height_in_feet} feet (BMI: {bmi}). The individual has the following health concerns: {health_issues}. "
        f"Dietary habits: {dietary_habits}. Make the advice specific to this individual's needs."
    )

    model = genai.GenerativeModel("gemini-pro")

    try:
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Function to answer general questions from users
def ask_ai_question(question):
    """
    Sends the user's question to the AI model and returns the response.
    """
    prompt = f"Answer the following question: {question}"

    model = genai.GenerativeModel("gemini-pro")

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Input fields for user details
st.subheader("Enter Your Details")
age = st.number_input("Enter your age:", min_value=1, max_value=120)
gender = st.selectbox("Enter your gender:", ["Male", "Female", "Other"])
weight = st.number_input("Enter your weight (kg):", min_value=1.0)
height_in_feet = st.number_input("Enter your height (feet):", min_value=1.0)
health_issues = st.text_input("List any health conditions (e.g., diabetes, hypertension) or type 'None'")

# Input fields for dietary habits
st.subheader("Dietary Habits")
fruits = st.number_input("How many times per week do you eat fruits?", min_value=0)
vegetables = st.number_input("How many times per week do you eat vegetables?", min_value=0)
protein_sources = st.number_input("How many times per week do you consume protein sources (e.g., meat, legumes)?", min_value=0)
whole_grains = st.number_input("How many times per week do you consume whole grains (e.g., oats, brown rice)?", min_value=0)
micronutrient_deficiency = st.text_input("Do you have any known micronutrient deficiencies (e.g., iron, vitamin D, calcium)? If none, type 'None'")

# Button to generate nutrition advice
if st.button("Get Nutrition Advice"):
    dietary_habits = {
        "fruits": fruits,
        "vegetables": vegetables,
        "protein_sources": protein_sources,
        "whole_grains": whole_grains,
        "micronutrient_deficiency": micronutrient_deficiency
    }

    # Calculate BMI
    bmi = calculate_bmi(weight, height_in_feet)

    # Determine nutrition problem based on BMI and age
    nutrition_problem = determine_nutrition_problem(bmi, age, gender)

    # Determine dietary issue based on dietary habits
    dietary_problem = determine_dietary_habits(dietary_habits)

    # Combine nutrition problem and dietary problem
    overall_problem = nutrition_problem if nutrition_problem != "Healthy weight" else dietary_problem

    # Display results
    st.subheader(f"Your Nutrition Problem: {overall_problem}")

    # Get personalized nutrition advice
    advice = get_nutrition_advice(overall_problem, age, gender, health_issues, weight, height_in_feet, bmi, dietary_habits)
    st.subheader("Personalized Nutrition Advice:")
    st.write(advice)

# Section for users to ask any question
st.subheader("Ask Any Question:")
user_question = st.text_input("Type your question here:")

# When the user asks a question
if st.button("Get Answer"):
    if user_question:
        ai_response = ask_ai_question(user_question)
        st.subheader("AI's Answer:")
        st.write(ai_response)
    else:
        st.write("Please type a question to ask the AI.")
