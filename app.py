import streamlit as st
import pickle
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Health Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .input-container {
        background-color: #f8fafc;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #3b82f6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prediction-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .info-box {
        background-color: #e0f2fe;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0284c7;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<h1 class="main-header">🏥 Health Insurance Premium Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Get an instant estimate of your health insurance premium based on your personal details</p>', unsafe_allow_html=True)

# Sidebar with information
st.sidebar.markdown("## 📊 About This Tool")
st.sidebar.info("""
This AI-powered tool predicts your health insurance premium based on:
- **Age**: Your current age
- **Gender**: Male or Female
- **BMI**: Body Mass Index
- **Children**: Number of dependents
- **Smoking Status**: Whether you smoke or not

The model uses machine learning algorithms trained on historical insurance data to provide accurate predictions.
""")

st.sidebar.markdown("## 🎯 BMI Reference")
bmi_info = pd.DataFrame({
    'Category': ['Underweight', 'Normal', 'Overweight', 'Obese'],
    'BMI Range': ['< 18.5', '18.5 - 24.9', '25 - 29.9', '≥ 30']
})
st.sidebar.table(bmi_info)

# Load model
@st.cache_resource
def load_model():
    return pickle.load(open('model.pkl', 'rb'))

model = load_model()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    
    st.markdown("### 📝 Enter Your Details")
    
    # Create two columns for inputs
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        age = st.number_input('🎂 Age:', min_value=18, max_value=100, value=30, help="Enter your age (18-100)")
        bmi = st.number_input('⚖️ BMI (Body Mass Index):', min_value=10.0, max_value=50.0, value=25.0, step=0.1, 
                             help="Calculate: weight(kg) / height(m)²")
        
    with input_col2:
        sex = st.selectbox('👤 Gender:', ['Male', 'Female'], help="Select your gender")
        children = st.number_input('👶 Number of Children:', min_value=0, max_value=10, step=1, value=0,
                                 help="Number of children/dependents")
    
    smoker = st.selectbox('🚬 Smoking Status:', ['No', 'Yes'], help="Do you smoke?")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction section
    st.markdown("### 🔮 Get Your Premium Estimate")
    
    predict_col1, predict_col2, predict_col3 = st.columns([1, 1, 1])
    
    with predict_col2:
        predict_button = st.button('🎯 Predict Premium', type="primary", use_container_width=True)
    
    # Clear button
    with predict_col1:
        if st.button('🔄 Reset Form', use_container_width=True):
            st.experimental_rerun()
    
    # Info button
    with predict_col3:
        if st.button('ℹ️ How it works', use_container_width=True):
            st.info("""
            Our machine learning model analyzes multiple factors to predict your insurance premium:
            
            **Key Factors:**
            - Age: Older individuals typically have higher premiums
            - BMI: Higher BMI may indicate health risks
            - Smoking: Significantly increases premium costs
            - Children: More dependents can affect coverage costs
            - Gender: Statistical differences in healthcare usage
            """)

with col2:
    st.markdown("### 📊 Your Input Summary")

    # Custom CSS for better readability
    st.markdown(
        """
        <style>
        .info-box {
            background-color: #1E293B; /* Dark slate background */
            color: #F8FAFC;            /* Light text */
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            line-height: 1.6;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .info-box strong {
            color: #38BDF8; /* Highlighted cyan title */
            font-size: 17px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display current inputs in styled box
    if age and bmi:
        st.markdown(f"""
        <div class="info-box">
        <strong>Current Details:</strong><br>
        🎂 Age: {age} years<br>
        👤 Gender: {sex}<br>
        ⚖️ BMI: {bmi}<br>
        👶 Children: {children}<br>
        🚬 Smoker: {smoker}
        </div>
        """, unsafe_allow_html=True)

        
        # BMI Category
        if bmi < 18.5:
            bmi_category = "Underweight"
            bmi_color = "#fbbf24"
        elif bmi < 25:
            bmi_category = "Normal"
            bmi_color = "#10b981"
        elif bmi < 30:
            bmi_category = "Overweight"
            bmi_color = "#f59e0b"
        else:
            bmi_category = "Obese"
            bmi_color = "#ef4444"
        
        st.markdown(f"""
        <div style="background-color: {bmi_color}20; padding: 1rem; border-radius: 10px; border-left: 4px solid {bmi_color};">
        <strong>BMI Category:</strong> {bmi_category}
        </div>
        """, unsafe_allow_html=True)

# Prediction logic
if predict_button:
    if age and bmi:
        with st.spinner('🔄 Calculating your premium...'):
            gender = 1 if sex == 'Female' else 0
            smoker_encoded = 1 if smoker == 'Yes' else 0
            premiums = [[age, gender, bmi, children, smoker_encoded]]
            prediction = model.predict(premiums)[0]
            
            st.markdown(f"""
            <div class="prediction-result">
            💰 Estimated Annual Premium<br>
            <span style="font-size: 2.5rem;">${prediction:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional insights
            st.markdown("### 📈 Premium Breakdown Insights")
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                age_impact = "High" if age > 50 else "Medium" if age > 35 else "Low"
                st.metric("Age Impact", age_impact, f"{age} years")
            
            with insight_col2:
                bmi_impact = "High" if bmi > 30 else "Medium" if bmi > 25 else "Low"
                st.metric("BMI Impact", bmi_impact, f"{bmi:.1f}")
            
            with insight_col3:
                smoker_impact = "Very High" if smoker == 'Yes' else "None"
                st.metric("Smoking Impact", smoker_impact)
            
            # Tips section
            if smoker == 'Yes' or bmi > 25:
                st.markdown("### 💡 Ways to Potentially Lower Your Premium")
                tips = []
                if smoker == 'Yes':
                    tips.append("🚭 Quit smoking - This is the single biggest factor in reducing premiums")
                if bmi > 25:
                    tips.append("🏃‍♀️ Maintain a healthy weight through diet and exercise")
                if age > 40:
                    tips.append("🩺 Regular health check-ups can help maintain good health")
                
                for tip in tips:
                    st.markdown(f"- {tip}")
    else:
        st.error("⚠️ Please fill in all required fields to get your prediction!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem;">
💡 <strong>Disclaimer:</strong> This prediction is for estimation purposes only. Actual premiums may vary based on insurance company policies, coverage options, and other factors.
</div>
""", unsafe_allow_html=True)