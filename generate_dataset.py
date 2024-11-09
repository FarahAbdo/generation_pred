import pandas as pd
import numpy as np
from investmentt import RealEstateInvestmentAnalyzer

def generate_synthetic_data(num_samples=5000):
    analyzer = RealEstateInvestmentAnalyzer()
    data = []
    
    # Define possible values with realistic constraints
    property_types = ["tower", "hotel", "administrative_building", 
                     "residential_compound", "villa"]
    districts = ["النرجس", "الملقا", "القيروان", "الياسمين", "العارض", "حطين"]
    
    # Define realistic ranges for different property types
    area_ranges = {
        "tower": (2000, 8000),
        "hotel": (3000, 10000),
        "administrative_building": (1500, 7000),
        "residential_compound": (4000, 15000),
        "villa": (500, 2000)
    }
    
    floor_ranges = {
        "tower": (10, 20),
        "hotel": (8, 15),
        "administrative_building": (5, 12),
        "residential_compound": (4, 8),
        "villa": (2, 4)
    }
    
    for _ in range(num_samples):
        # Generate property type first
        context_type = np.random.choice(property_types)
        
        # Generate realistic values based on property type
        land_area = np.random.uniform(*area_ranges[context_type])
        num_floors = np.random.randint(*floor_ranges[context_type])
        district = np.random.choice(districts)
        
        try:
            result = analyzer.generate_investment_report(
                land_area=land_area,
                district=district,
                num_floors=num_floors,
                context_type=context_type
            )
            
            details = result["تقرير_تحليل_الاستثمار"]
            
            data_point = {
                'property_type': context_type,
                'district': district,
                'land_area': land_area,
                'num_floors': num_floors,
                'total_investment': float(details["التكاليف"]["إجمالي_الاستثمار"].split()[0].replace(",", "")),
                'total_revenue': float(details["الإيرادات"]["إيرادات_البيع"].split()[0].replace(",", "")),
                'gross_profit': float(details["الإيرادات"]["الربح_الإجمالي"].split()[0].replace(",", "")),
                'annual_rent': float(details["الإيرادات"]["الإيجار_السنوي"].split()[0].replace(",", "")),
                'roi': float(details["الإيرادات"]["العائد_على_الاستثمار"].replace("%", ""))
            }
            
            data.append(data_point)
            
        except Exception as e:
            print(f"Error generating data point: {e}")
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating dataset...")
    df = generate_synthetic_data(5000)
    df.to_csv('real_estate_data.csv', index=False)
    print("Dataset generated and saved!")
    
    # Print some basic statistics
    print("\nDataset Statistics:")
    print(f"Total samples: {len(df)}")
    print("\nNumerical columns summary:")
    print(df.describe())