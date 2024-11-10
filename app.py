# import streamlit as st
# import json
# from investmentt import RealEstateInvestmentAnalyzer  # This imports your existing class

# def main():
#     st.set_page_config(page_title="Real Estate Investment Analyzer", layout="wide")
    
#     # Title and description
#     st.title("Real Estate Investment Analyzer")
#     st.markdown("Analyze different types of real estate investments in Saudi Arabia")

#     # Initialize analyzer
#     analyzer = RealEstateInvestmentAnalyzer()

#     # Create columns for input
#     col1, col2 = st.columns(2)

#     with col1:
#         # Input fields
#         context_type = st.selectbox(
#             "Property Type",
#             ["tower", "hotel", "administrative_building", "residential_compound", 
#              "villa", "villas", "commercial_mall"]
#         )

#         district = st.selectbox(
#             "District",
#             ["النرجس", "الملقا", "القيروان", "الياسمين", "العارض", "حطين"]
#         )

#     with col2:
#         land_area = st.number_input(
#             "Land Area (sq meters)",
#             min_value=100,
#             max_value=100000,
#             value=5000
#         )

#         num_floors = st.number_input(
#             "Number of Floors",
#             min_value=1,
#             max_value=20,
#             value=5
#         )

#     # Analysis button
#     if st.button("Generate Analysis"):
#         try:
#             # Use your existing analyzer class
#             result = analyzer.generate_investment_report(
#                 land_area=land_area,
#                 district=district,
#                 num_floors=num_floors,
#                 context_type=context_type
#             )

#             # Display results
#             st.header("Investment Analysis Report")

#             # Project Details
#             st.subheader("Project Details")
#             details = result["تقرير_تحليل_الاستثمار"]["تفاصيل_المشروع"]
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.metric("Location", details["الموقع"])
#                 st.metric("Land Area", details["مساحة_الأرض"])
#             with col2:
#                 st.metric("Effective Building Area", details["مساحة_البناء_الفعالة"])

#             # Costs
#             st.subheader("Costs")
#             costs = result["تقرير_تحليل_الاستثمار"]["التكاليف"]
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Land Cost", costs["تكلفة_الأرض"])
#             with col2:
#                 st.metric("Construction Cost", costs["تكلفة_البناء"])
#             with col3:
#                 st.metric("Total Investment", costs["إجمالي_الاستثمار"])

#             # Revenue and Returns
#             st.subheader("Revenue and Returns")
#             revenue = result["تقرير_تحليل_الاستثمار"]["الإيرادات"]
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Sales Revenue", revenue["إيرادات_البيع"])
#                 st.metric("Gross Profit", revenue["الربح_الإجمالي"])
#             with col2:
#                 st.metric("Annual Rent", revenue["الإيجار_السنوي"])
#                 st.metric("Net Annual Rent", revenue["صافي_الإيجار_السنوي"])
#             with col3:
#                 st.metric("Profit Margin", revenue["هامش_الربح"])
#                 st.metric("ROI (Rental)", revenue["العائد_على_الاستثمار"])

#             # Raw JSON data (expandable)
#             with st.expander("View Raw Data"):
#                 st.json(result)

#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import numpy as np
import os
from investmentt import RealEstateInvestmentAnalyzer
from ml_model import RealEstateMLModel, train_and_save_models

if not os.path.exists('./.streamlit/models'):
    os.makedirs('./.streamlit/models', exist_ok=True)

# Update model paths to use the Streamlit shared folder
MODEL_DIR = './.streamlit/models'

@st.cache_resource
def load_ml_models():
    """Load all trained ML models or train new ones if missing"""
    models = {}
    targets = ['total_investment', 'total_revenue', 'gross_profit', 'annual_rent', 'roi']
    
    try:
        # Always train new models in cloud environment
        st.info("Training ML models...")
        train_and_save_models(model_dir=MODEL_DIR)
        st.success("Models trained successfully!")
        
        # Load the trained models
        for target in targets:
            try:
                model_path = os.path.join(MODEL_DIR, f'model_{target}.joblib')
                models[target] = RealEstateMLModel.load_model(model_path)
            except Exception as e:
                st.warning(f"Could not load model for {target}: {str(e)}")
    except Exception as e:
        st.error(f"Error training models: {str(e)}")
        return {}
    
    return models


def main():
    st.set_page_config(
        page_title="Real Estate Investment Analyzer",
        page_icon="🏢",
        layout="wide"
    )
    
    # Title and description
    st.title("🏢 Real Estate Investment Analyzer")
    
    # Add mode selection
    analysis_mode = st.radio(
        "Select Analysis Mode",
        ["Formula Only", "Formula + ML Predictions"],
        help="Choose whether to use only formula calculations or include ML predictions"
    )
    
    # Initialize analyzers
    analyzer = RealEstateInvestmentAnalyzer()
    ml_models = load_ml_models() if analysis_mode == "Formula + ML Predictions" else {}
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Input Parameters")
        
        context_type = st.selectbox(
            "Property Type",
            ["tower", "hotel", "administrative_building", 
             "residential_compound", "villa", "villas", "commercial_mall"]
        )
        
        district = st.selectbox(
            "District",
            ["النرجس", "الملقا", "القيروان", "الياسمين", "العارض", "حطين"]
        )
        
        land_area = st.number_input(
            "Land Area (sq meters)",
            min_value=500,
            max_value=15000,
            value=5000,
            step=100
        )
        
        num_floors = st.number_input(
            "Number of Floors",
            min_value=1,
            max_value=20,
            value=5
        )
        
        analyze_button = st.button("Analyze Investment", type="primary")
    
    
    if analyze_button:
        with st.spinner("Analyzing investment..."):
            try:
                # Get formula-based calculations
                formula_result = analyzer.generate_investment_report(
                    land_area=land_area,
                    district=district,
                    num_floors=num_floors,
                    context_type=context_type
                )

                # Extract formula values
                details = formula_result["تقرير_تحليل_الاستثمار"]
                formula_values = {
                    'total_investment': float(details["التكاليف"]["إجمالي_الاستثمار"].split()[0].replace(",", "")),
                    'total_revenue': float(details["الإيرادات"]["إيرادات_البيع"].split()[0].replace(",", "")),
                    'gross_profit': float(details["الإيرادات"]["الربح_الإجمالي"].split()[0].replace(",", "")),
                    'annual_rent': float(details["الإيرادات"]["الإيجار_السنوي"].split()[0].replace(",", "")),
                    'roi': float(details["الإيرادات"]["العائد_على_الاستثمار"].replace("%", ""))
                }

                # Only do ML predictions if in ML mode and models are available
                if analysis_mode == "Formula + ML Predictions" and ml_models:
                    ml_input = pd.DataFrame({
                        'property_type': [context_type],
                        'district': [district],
                        'land_area': [land_area],
                        'num_floors': [num_floors]
                    })

                    ml_predictions = {}
                    for target, model in ml_models.items():
                        try:
                            ml_predictions[target] = model.predict(ml_input)[0]
                        except Exception as e:
                            st.error(f"Error predicting {target}: {str(e)}")
                            ml_predictions[target] = formula_values[target]

                    differences = {
                        key: ((ml_predictions[key] - formula_values[key]) / formula_values[key]) * 100
                        for key in formula_values.keys()
                    }
                else:
                    ml_predictions = formula_values.copy()
                    differences = {k: 0 for k in formula_values.keys()}

                # Display results based on mode
                if analysis_mode == "Formula Only":
                    display_formula_results(formula_values)
                else:
                    display_comparison_results(formula_values, ml_predictions, differences)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Error details:", str(e))
                import traceback
                st.write("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    main()
