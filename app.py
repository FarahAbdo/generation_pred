import streamlit as st
import pandas as pd
import numpy as np
import os
from investmentt import RealEstateInvestmentAnalyzer
from ml_model import RealEstateMLModel, train_and_save_models, generate_synthetic_data
import plotly.graph_objects as go

# Create a cache directory in the Streamlit shared folder
MODEL_DIR = './.streamlit/models'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR, exist_ok=True)

def format_currency(value):
    """Format currency values"""
    return f"{value:,.2f} SAR"

def format_percentage(value):
    """Format percentage values"""
    return f"{value:.2f}%"

def create_comparison_chart(formula_values, ml_predictions):
    """Create a comparison chart using plotly"""
    metrics = list(formula_values.keys())
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Formula Calculations',
        x=metrics,
        y=[formula_values[m] for m in metrics],
        marker_color='rgb(55, 83, 109)'
    ))
    
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

def display_formula_results(formula_values):
    """Display formula-only results"""
    st.header("Investment Analysis Results")
    
    for key, value in formula_values.items():
        if key != 'roi':
            st.metric(key.replace('_', ' ').title(), format_currency(value))
        else:
            st.metric(key.upper(), format_percentage(value))

def display_comparison_results(formula_values, ml_predictions, differences):
    """Display comparison results"""
    st.header("Investment Analysis Results")
    
    # Create three columns for display
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
    
    # Add comparison chart
    st.plotly_chart(create_comparison_chart(formula_values, ml_predictions), use_container_width=True)
    
    # Add analysis section
    st.header("Analysis")
    avg_diff = np.mean(np.abs(list(differences.values())))
    
    if avg_diff < 10:
        st.success(f"Average difference: {format_percentage(avg_diff)} - ML predictions are very accurate!")
    elif avg_diff < 20:
        st.warning(f"Average difference: {format_percentage(avg_diff)} - ML predictions show moderate deviation.")
    else:
        st.error(f"Average difference: {format_percentage(avg_diff)} - ML predictions show significant deviation.")

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

                # Display full report in expandable section
                with st.expander("View Full Investment Report"):
                    st.json(formula_result)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Error details:", str(e))
                import traceback
                st.write("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    main()
