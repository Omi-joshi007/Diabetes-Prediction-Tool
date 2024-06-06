# Importing required libraries
import streamlit as st
import joblib
import numpy as np
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

# Define a boolean variable to track if all inputs are provided
all_inputs_provided = False

# Initialize variables to store user inputs
glucose_level = None
body_mass_index = None
age = None
number_of_pregnancies = None

# Load the trained model
model = joblib.load('random_forest_model.pkl')

# Top horizontal navigation bar
selected = option_menu(
    menu_title=None,  # required
    options=["Home", "About Diabetes", "Healthy Tips"],  # required
    icons=["house", "info-circle", "heart"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal"
)

# Define the Streamlit app
def main():
    # Access the global variables
    global all_inputs_provided, glucose_level, body_mass_index, age, number_of_pregnancies
    # Home page content
    if selected == "Home":  
        st.title('Diabetes Predictor')
        st.write("This tool will predict your risk of diabetes based on your health metrics.")
        # Add input widgets for user inputs
        glucose_level = st.number_input('Glucose Level', min_value=0.0,value=None, placeholder='Enter your Glucose Level')
        body_mass_index = st.number_input('Body Mass Index (BMI)', min_value=0.0, value=None, placeholder='Enter your Body Mass Index')
        age = st.number_input('Age', min_value=0.0, value=None, placeholder="Enter your Age")
        number_of_pregnancies = st.number_input('Number of pregnancies', min_value=0.0, value=None, placeholder="How many times your been pregrant ?")
        blood_pressure = 0
        skin_thickness = 0
        insulin = 0
        DiabetesPedigreeFunction = 0

        # Check if all inputs are provided
        if glucose_level is not None and body_mass_index is not None and age is not None and number_of_pregnancies is not None:
            all_inputs_provided = True
        else:
            all_inputs_provided = False

        prediction = 0
        # Make predictions when a button is clicked
        if st.button('Predict', disabled=not all_inputs_provided):
            # Prepare the user inputs as a feature array
            user_inputs = np.array([[number_of_pregnancies,glucose_level,blood_pressure,skin_thickness,
                                    insulin, body_mass_index, DiabetesPedigreeFunction, age]])  # Replace with appropriate test values
            # Use the trained model to make predictions
            prediction = model.predict(user_inputs)
            
            #Display the prediction
            if prediction == 1:
                st.write('Prediction:', ":red[Opps!! You are at risk for diabetes.]")
                
            else:
                st.write('Prediction:', ":green[Congrats!! You are not at risk for diabetes.]")

            def plot_glucose_level(glucose):
                normal_range = [70, 100]  # Normal range for glucose level
                fig, ax = plt.subplots()
                
                # Plot normal range
                ax.plot([0, 1], [normal_range[0], normal_range[0]], color='green', linestyle='dashed', label='Normal Range')
                ax.plot([0, 1], [normal_range[1], normal_range[1]], color='green', linestyle='dashed')
                
                # Plot user's glucose level
                ax.plot([0.5], [glucose], marker='o', color='red' if glucose > normal_range[1] else 'blue', label='Your Glucose value')
                
                ax.set_xlim(0, 1)
                ax.set_ylim(0, max(glucose, normal_range[1]) + 20)
                ax.set_xticks([])
                ax.set_ylabel('Glucose Level (mg/dL)')
                ax.set_title('Glucose Level Comparison')
                ax.legend()
                
                return fig

            # Function to plot BMI comparison
            def plot_bmi(bmi):
                normal_range = [18.5, 24.9]  # Normal range for BMI
                fig, ax = plt.subplots()
                
                # Plot normal range
                ax.plot([0, 1], [normal_range[0], normal_range[0]], color='green', linestyle='dashed', label='Normal Range')
                ax.plot([0, 1], [normal_range[1], normal_range[1]], color='green', linestyle='dashed')
                
                # Plot user's BMI
                ax.plot([0.5], [bmi], marker='o', color='red' if bmi > normal_range[1] else 'blue', label='Your BMI value')
                
                ax.set_xlim(0, 1)
                ax.set_ylim(0, max(bmi, normal_range[1]) + 5)
                ax.set_xticks([])
                ax.set_ylabel('BMI')
                ax.set_title('BMI Comparison')
                ax.legend()
                
                return fig


            # Display graphs
            st.write("Health Metrics Comparison")
            st.write("1. Your glucose level is - "+str(glucose_level))
            st.write("Normal glucose level should be between - 70 to 100")
            st.write("\n")
            st.write("2. Your BMI is - "+str(body_mass_index))
            st.write("Normal BMI should be between - 18 to 25")

            st.subheader("Glucose Level")
            st.pyplot(plot_glucose_level(glucose_level))

            st.subheader("BMI")
            st.pyplot(plot_bmi(body_mass_index))

            #st.write('The scikit-learn version is {}.'.format(sklearn.__version__))

    # About Diabetes page content
    elif selected == "About Diabetes":
        st.title("About Diabetes")
        st.write("""
        Diabetes is a chronic condition characterized by high levels of sugar in the blood. 
        It occurs when the body is unable to produce enough insulin or effectively use the insulin it produces. 
        Understanding your risk factors can help you take preventive measures.
        """)
        st.write("Types of diabetes:") 
        st.write("Type 1 diabetes: Autoimmune condition causing insulin deficiency in early life stages.")
        st.write("Type 2 diabetes: Metabolic disorder characterized by insulin resistance, often lifestyle-related.")
        st.image('diabetes-symptoms.jpg')

    # Healthy Tips page content
    elif selected == "Healthy Tips":
        st.title("Healthy Tips")
        st.write("1. Maintain a balanced diet with moderate carbohydrate intake.")
        st.write("2. Engage in regular physical activity or exercise sessions.")
        st.write("3. Choose low glycemic index foods to manage blood sugar levels.")
        st.write("4. Control portion sizes to avoid overeating and weight gain.")
        st.write("5. Limit consumption of sugary beverages and processed foods.")
        st.image('diabetes-food-list.jpg')
        
        
if __name__ == '__main__':
    main()