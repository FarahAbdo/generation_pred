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
from investmentt import RealEstateInvestmentAnalyzer
from ml_model import RealEstateMLModel
import plotly.express as px
import plotly.graph_objects as go

def load_ml_models():
    """Load all trained ML models"""
    models = {}
    targets = ['total_investment', 'total_revenue', 'gross_profit', 'annual_rent', 'roi']
    for target in targets:
        try:
            models[target] = RealEstateMLModel.load_model(f'model_{target}.joblib')
        except Exception as e:
            st.warning(f"Could not load model for {target}: {str(e)}")
    return models

def format_currency(value):
    """Format currency values"""
    return f"{value:,.2f} SAR"

def format_percentage(value):
    """Format percentage values"""
    return f"{value:.2f}%"

def create_comparison_chart(formula_values, ml_predictions, differences):
    """Create a comparison chart using plotly"""
    metrics = list(formula_values.keys())
    
    fig = go.Figure()
    
    # Add Formula Values
    fig.add_trace(go.Bar(
        name='Formula Calculations',
        x=metrics,
        y=[formula_values[m] for m in metrics],
        marker_color='rgb(55, 83, 109)'
    ))
    
    # Add ML Predictions
    fig.add_trace(go.Bar(
        name='ML Predictions',
        x=metrics,
        y=[ml_predictions[m] for m in metrics],
        marker_color='rgb(26, 118, 255)'
    ))
    
    fig.update_layout(
        title='Comparison of Formula vs ML Predictions',
        xaxis_title='Metrics',
        yaxis_title='Values (SAR)',
        barmode='group',
        height=500
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Real Estate Investment Analyzer",
        page_icon="🏢",
        layout="wide"
    )
    
    # Title and description
    st.title("🏢 Real Estate Investment Analyzer")
    st.markdown("""
    Compare traditional formula-based calculations with machine learning predictions 
    for real estate investment analysis.
    """)
    
    # Initialize analyzers
    analyzer = RealEstateInvestmentAnalyzer()
    ml_models = load_ml_models()
    
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

                # Prepare input for ML predictions
                ml_input = pd.DataFrame({
                    'property_type': [context_type],
                    'district': [district],
                    'land_area': [land_area],
                    'num_floors': [num_floors]
                })

                # Get ML predictions
                ml_predictions = {}
                for target, model in ml_models.items():
                    try:
                        ml_predictions[target] = model.predict(ml_input)[0]
                    except Exception as e:
                        st.error(f"Error predicting {target}: {str(e)}")
                
                # Extract formula values
                details = formula_result["تقرير_تحليل_الاستثمار"]
                formula_values = {
                    'total_investment': float(details["التكاليف"]["إجمالي_الاستثمار"].split()[0].replace(",", "")),
                    'total_revenue': float(details["الإيرادات"]["إيرادات_البيع"].split()[0].replace(",", "")),
                    'gross_profit': float(details["الإيرادات"]["الربح_الإجمالي"].split()[0].replace(",", "")),
                    'annual_rent': float(details["الإيرادات"]["الإيجار_السنوي"].split()[0].replace(",", "")),
                    'roi': float(details["الإيرادات"]["العائد_على_الاستثمار"].replace("%", ""))
                }

                # Calculate differences
                differences = {
                    key: ((ml_predictions[key] - formula_values[key]) / formula_values[key]) * 100
                    for key in formula_values.keys()
                }

                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["📊 Results", "📈 Visualizations", "📝 Detailed Analysis"])
                
                with tab1:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("Formula Calculations")
                        for key, value in formula_values.items():
                            if key != 'roi':
                                st.metric(key.replace('_', ' ').title(), format_currency(value))
                            else:
                                st.metric(key.upper(), format_percentage(value))
                    
                    with col2:
                        st.subheader("ML Predictions")
                        for key, value in ml_predictions.items():
                            if key != 'roi':
                                st.metric(key.replace('_', ' ').title(), format_currency(value))
                            else:
                                st.metric(key.upper(), format_percentage(value))
                    
                    with col3:
                        st.subheader("Difference (%)")
                        for key, value in differences.items():
                            st.metric(key.replace('_', ' ').title(), format_percentage(value))
                
                with tab2:
                    # Create comparison chart
                    fig = create_comparison_chart(formula_values, ml_predictions, differences)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add more visualizations as needed
                    
                with tab3:
                    st.subheader("Detailed Analysis")
                    
                    # Calculate average absolute difference
                    avg_diff = np.mean(np.abs(list(differences.values())))
                    
                    # Display accuracy metrics
                    st.metric("Average Absolute Difference", format_percentage(avg_diff))
                    
                    # Recommendations based on differences
                    st.subheader("Recommendations")
                    for metric, diff in differences.items():
                        abs_diff = abs(diff)
                        metric_name = metric.replace('_', ' ').title()
                        
                        if abs_diff < 10:
                            st.success(f"✅ {metric_name}: Predictions are very accurate ({format_percentage(abs_diff)} difference)")
                        elif abs_diff < 20:
                            st.warning(f"⚠️ {metric_name}: Moderate difference ({format_percentage(abs_diff)} difference)")
                        else:
                            st.error(f"❌ {metric_name}: Large difference ({format_percentage(abs_diff)} difference)")
                    
                    # Show raw data
                    with st.expander("View Raw Data"):
                        st.json({
                            "Formula Results": formula_result,
                            "ML Predictions": {k: float(v) for k, v in ml_predictions.items()},
                            "Differences (%)": {k: float(v) for k, v in differences.items()}
                        })

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Error details:", str(e))
                import traceback
                st.write("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    main()