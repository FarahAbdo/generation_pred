import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random

# Villa Data Generator
class VillaDataGenerator:
    def __init__(self):
        self.districts = {
            'District 1': {'price_per_sqm': 3000},
            'District 2': {'price_per_sqm': 2500},
            'District 3': {'price_per_sqm': 2000},
            'District 4': {'price_per_sqm': 1500},
        }

    def generate_synthetic_dataset(self, n_samples):
        data = []
        for _ in range(n_samples):
            district = random.choice(list(self.districts.keys()))
            land_area = random.randint(300, 3000)  # Land area between 300 and 3000 sqm
            num_floors = random.randint(2, 4)       # Floors between 2 and 4
            date = datetime.now().strftime('%Y-%m-%d')

            # Price calculation based on the district and land area
            price_per_sqm = self.districts[district]['price_per_sqm']
            total_price = land_area * price_per_sqm

            data.append({
                'land_area': land_area,
                'district': district,
                'num_floors': num_floors,
                'total_price': total_price,
                'date': date
            })
        return pd.DataFrame(data)

# Villa Data Collector
class VillaDataCollector:
    def __init__(self, filename='villa_data.csv'):
        self.filename = filename
        self.data = pd.DataFrame(columns=['land_area', 'district', 'num_floors', 'total_price', 'date'])

    def initialize_csv(self):
        # Create CSV with headers if it doesn't exist
        self.data.to_csv(self.filename, index=False)

    def add_entry(self, entry):
        # Append new data entry to the DataFrame
        self.data = self.data.append(entry, ignore_index=True)
        self.data.to_csv(self.filename, index=False)

# Villa Investment Predictor
# Villa Investment Predictor
class VillaInvestmentPredictor:
    def __init__(self):
        # Dummy parameters for calculation
        self.base_price = 2000  # Base price per square meter
        self.building_cost_per_sqm = 1500  # Building cost per square meter
        self.additional_costs = 0.1  # 10% additional costs for contingencies

    def predict(self, property_data):
        # Simple prediction logic based on dummy weights
        weight_land_area = 2000  # dummy weight for land area
        weight_num_floors = 15000  # dummy weight for number of floors
        weight_district = {'District 1': 1.5, 'District 2': 1.2, 'District 3': 1.0, 'District 4': 0.8}

        district_value = weight_district[property_data['district'].values[0]]
        land_area = property_data['land_area'].values[0]
        num_floors = property_data['num_floors'].values[0]

        predicted_value = (land_area * weight_land_area) + (num_floors * weight_num_floors * district_value)
        return predicted_value

    def generate_investment_report(self, land_area, district, num_floors):
        # Calculation of costs
        total_land_cost = land_area * self.base_price
        total_build_cost = land_area * self.building_cost_per_sqm
        total_cost = total_land_cost + total_build_cost + (total_build_cost * self.additional_costs)

        # Calculating effective build areas and ratios
        ground_floor_ratio = 0.5  # Example ratio for ground floor
        repeated_floor_ratio = 0.5  # Example ratio for repeated floors
        top_attachment_ratio = 0.5  # Example ratio for top attachment

        ground_build_area = land_area * ground_floor_ratio
        repeated_build_area = land_area * repeated_floor_ratio * (num_floors - 1)
        top_attachment_build_area = land_area * top_attachment_ratio
        total_effective_build_area = ground_build_area + repeated_build_area + top_attachment_build_area

        report = {
            "مقدمة": "هذا التحليل الاستثماري المفصل يقيم جدوى وربحية تطوير مشروع فيلا فاخر في حي النرجس بالرياض. يشمل التحليل استراتيجيات البيع والإيجار، مع النظر في ديناميكيات السوق الحالية وتقديرات التكاليف والإمكانيات الإيرادية.",
            "العنوان": "تقرير استثماري لمشروع فيلا في حي " + district,
            "تقرير_تحليل_الاستثمار": {
                "تفاصيل_المشروع": {
                    "الموقع": f"حي {district}، الرياض",
                    "مساحة_الأرض_الإجمالية": f"{land_area} متر مربع",
                    "نوع_المشروع": "تطوير سكني فردي",
                    "تنظيمات_التخطيط": f"يسمح ببناء حتى {num_floors} طوابق"
                },
                "معايير_التطوير": {
                    "نسبة_البناء_للدور_الأرضي": ground_floor_ratio,
                    "نسبة_البناء_للأدوار_المتكررة": repeated_floor_ratio,
                    "نسبة_البناء_للملحق_العلوي": top_attachment_ratio,
                    "الطوابق_المقترحة": num_floors,
                    "مساحة_البناء_الفعالة_للدور_الأرضي": ground_build_area,
                    "مساحة_البناء_الفعالة_للمتكرر": repeated_build_area,
                    "مساحة_البناء_الفعالة_للملحق_العلوي": top_attachment_build_area,
                    "نتيجة_مساحة_البناء_الفعالة": total_effective_build_area,
                    "معامل_البناء": total_effective_build_area / land_area
                },
                "توقعات_التمويل": {
                    "تكلفة_شراء_الأرض": {
                        "تكلفة_الشراء_لكل_متر_مربع": f"{self.base_price} ريال سعودي",
                        "التكلفة_الكلية": f"{total_land_cost} ريال سعودي"
                    },
                    "تكاليف_البناء": {
                        "تكلفة_البناء_لكل_متر_مربع": f"{self.building_cost_per_sqm} ريال سعودي",
                        "مجموع_تكاليف_البناء": f"{total_build_cost} ريال سعودي",
                        "التكاليف_الإضافية": f"{self.additional_costs * 100}% من تكاليف البناء",
                        "المجموع": f"{total_cost} ريال سعودي"
                    }
                }
            }
        }
        
        return report


# Streamlit App
def main():
    st.title("Data Generation and Investment Prediction")

    # Initialize classes
    data_generator = VillaDataGenerator()
    data_collector = VillaDataCollector()
    investment_predictor = VillaInvestmentPredictor()


    # Generate Synthetic Dataset
    st.header("Generate Synthetic Dataset")
    n_samples = st.number_input("Number of samples to generate:", min_value=1, max_value=5000, value=1000)
    if st.button("Generate Dataset"):
        synthetic_data = data_generator.generate_synthetic_dataset(n_samples)
        st.write("Synthetic dataset generated!")
        st.dataframe(synthetic_data)

        # Save to CSV
        if st.button("Save to CSV"):
            data_collector.initialize_csv()
            for _, entry in synthetic_data.iterrows():
                data_collector.add_entry(entry.to_dict())
            st.success("Data saved to CSV!")

    # Predict Investment Value
    st.header("Predict Villa Investment Value")
    land_area = st.number_input("Enter land area (in sqm):", min_value=300, max_value=3000, value=500)
    district = st.selectbox("Select District:", list(data_generator.districts.keys()))
    num_floors = st.number_input("Number of Floors:", min_value=2, max_value=4, value=2)

    if st.button("Predict Investment Value"):
        property_data = pd.DataFrame({
            'land_area': [land_area],
            'district': [district],
            'num_floors': [num_floors],
            'date': [datetime.now().strftime('%Y-%m-%d')]
        })

        try:
            prediction = investment_predictor.predict(property_data)
            st.success(f"Predicted Investment Value: {prediction:.2f} SAR")
        except ValueError as e:
            st.error(str(e))

    # Generate Investment Report
    st.header("Generate Investment Report")
    if st.button("Generate Report"):
        report = investment_predictor.generate_investment_report(land_area, district, num_floors)
        st.write(report)

if __name__ == "__main__":
    main()
