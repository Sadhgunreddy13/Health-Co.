import google.generativeai as genai

# Configure Gemini AI
GENAI_API_KEY = "AIzaSyAgLTzLRE9fRVH5aaLeaKCYDgcNVt-2UWw"
genai.configure(api_key=GENAI_API_KEY)

def calculate_bmi(weight, height_in_feet):
    """
    Calculates BMI based on weight (kg) and height in feet.
    """
    # Convert height from feet to meters (1 foot = 0.3048 meters)
    height_in_meters = height_in_feet * 0.3048
    try:
        bmi = weight / (height_in_meters ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return "Height cannot be zero."

def determine_nutrition_problem(bmi, age, gender):
    """
    Determines the likely nutrition problem based on BMI, age, and gender.
    """
    # Nutrition problem based on BMI
    if bmi < 18.5:
        return "Malnutrition (underweight)"
    elif 18.5 <= bmi < 24.9:
        return "Healthy weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    elif bmi >= 30:
        return "Obesity"
    
    # If BMI falls in the healthy range, check for age-related factors (e.g., elderly)
    if age >= 65:
        return "Potential age-related malnutrition"
    return "Undetermined nutrition problem"

def determine_dietary_habits(dietary_habits):
    """
    Determines the likelihood of poor dietary diversity or micronutrient deficiency based on user input.
    """
    fruits = int(dietary_habits["fruits"])  # Number of times per week
    vegetables = int(dietary_habits["vegetables"])
    protein_sources = int(dietary_habits["protein_sources"])
    whole_grains = int(dietary_habits["whole_grains"])
    micronutrient_deficiency = dietary_habits["micronutrient_deficiency"]

    if fruits < 3 or vegetables < 3 or protein_sources < 2 or whole_grains < 2:
        return "Poor dietary diversity"

    if micronutrient_deficiency.lower() != "none":
        return f"Possible micronutrient deficiency (e.g., {micronutrient_deficiency})"

    return "Balanced diet"

def get_nutrition_advice(category, age, gender, health_issues, weight, height_in_feet, bmi, dietary_habits):
    """
    Fetches personalized nutrition advice based on category, age, gender, health issues, weight, height, BMI, and dietary habits.
    """
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

if __name__ == "__main__":
    print("Welcome to the Personalized Nutrition Advisor!")
    print("Let's start by gathering your details.")

    while True:
        age = input("Enter your age: ")
        gender = input("Enter your gender (Male/Female/Other): ")
        weight = float(input("Enter your weight in kilograms: "))
        height_in_feet = float(input("Enter your height in feet: "))
        health_issues = input("List any health conditions (e.g., diabetes, hypertension) or type 'None': ")

        # Collecting dietary habits
        print("\nPlease provide the following information about your dietary habits:")
        fruits = input("How many times per week do you eat fruits? ")
        vegetables = input("How many times per week do you eat vegetables? ")
        protein_sources = input("How many times per week do you consume protein sources (e.g., meat, legumes)? ")
        whole_grains = input("How many times per week do you consume whole grains (e.g., oats, brown rice)? ")
        micronutrient_deficiency = input("Do you have any known micronutrient deficiencies (e.g., iron, vitamin D, calcium)? If none, type 'None': ")

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

        print(f"\nBased on the information provided, your nutrition problem is likely: {overall_problem}\n")

        # Get personalized nutrition advice
        advice = get_nutrition_advice(overall_problem, age, gender, health_issues, weight, height_in_feet, bmi, dietary_habits)
        print("\nPersonalized Nutrition Advice:\n", advice)

        exit_choice = input("\nWould you like to check for another user? (yes/no): ").strip().lower()
        if exit_choice == 'no':
            print("Goodbye!")
            break
