import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
# Add this import
from investmentt import RealEstateInvestmentAnalyzer
import os

class RealEstateMLModel:
    def __init__(self):
        categorical_features = ['property_type', 'district']
        numeric_features = ['land_area', 'num_floors']
        
        # Use RobustScaler for better handling of outliers
        numeric_transformer = Pipeline([
            ('scaler', RobustScaler())
        ])
        
        categorical_transformer = Pipeline([
            ('onehot', OneHotEncoder(drop='first', sparse_output=False))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # Use GradientBoostingRegressor with optimized parameters
        self.model = Pipeline([
            ('preprocessor', self.preprocessor),
            ('regressor', GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=4,
                min_samples_split=5,
                min_samples_leaf=3,
                subsample=0.8,
                random_state=42
            ))
        ])



    def fit(self, X, y):
        self.model.fit(X, y)
        return self
        
    def predict(self, X):
        return self.model.predict(X)
    
    def save_model(self, filename):
        joblib.dump(self.model, filename)
    
    @classmethod
    def load_model(cls, filename):
        instance = cls()
        instance.model = joblib.load(filename)
        return instance

def generate_synthetic_data(num_samples=5000):
    """Generate more realistic synthetic data based on formula calculations"""
    analyzer = RealEstateInvestmentAnalyzer()
    data = []
    
    property_types = ["tower", "hotel", "administrative_building", 
                     "residential_compound", "villa"]
    districts = ["النرجس", "الملقا", "القيروان", "الياسمين", "العارض", "حطين"]
    
    # Define realistic ranges
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
        try:
            context_type = np.random.choice(property_types)
            district = np.random.choice(districts)
            
            # Get realistic ranges for this property type
            min_area, max_area = area_ranges[context_type]
            min_floors, max_floors = floor_ranges[context_type]
            
            # Generate values within realistic ranges
            land_area = np.random.uniform(min_area, max_area)
            num_floors = np.random.randint(min_floors, max_floors + 1)
            
            # Get formula calculations
            result = analyzer.generate_investment_report(
                land_area=land_area,
                district=district,
                num_floors=num_floors,
                context_type=context_type
            )
            
            details = result["تقرير_تحليل_الاستثمار"]
            
            # Extract values and clean them
            total_investment = float(details["التكاليف"]["إجمالي_الاستثمار"].split()[0].replace(",", ""))
            total_revenue = float(details["الإيرادات"]["إيرادات_البيع"].split()[0].replace(",", ""))
            gross_profit = float(details["الإيرادات"]["الربح_الإجمالي"].split()[0].replace(",", ""))
            annual_rent = float(details["الإيرادات"]["الإيجار_السنوي"].split()[0].replace(",", ""))
            roi = float(details["الإيرادات"]["العائد_على_الاستثمار"].replace("%", ""))
            
            data.append({
                'property_type': context_type,
                'district': district,
                'land_area': land_area,
                'num_floors': num_floors,
                'total_investment': total_investment,
                'total_revenue': total_revenue,
                'gross_profit': gross_profit,
                'annual_rent': annual_rent,
                'roi': roi
            })
            
        except Exception as e:
            print(f"Error generating data point: {e}")
    
    return pd.DataFrame(data)

def train_models():
    # Generate synthetic data
    print("Generating synthetic data...")
    df = generate_synthetic_data(5000)
    
    # Add engineered features
    df['area_per_floor'] = df['land_area'] / df['num_floors']
    df['investment_per_sqm'] = df['total_investment'] / df['land_area']
    
    # Remove outliers using IQR method
    def remove_outliers_iqr(df, columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
        return df
    
    numerical_columns = ['total_investment', 'total_revenue', 'gross_profit', 
                        'annual_rent', 'roi', 'area_per_floor', 'investment_per_sqm']
    df = remove_outliers_iqr(df, numerical_columns)
    
    # Train models for each target
    targets = ['total_investment', 'total_revenue', 'gross_profit', 
              'annual_rent', 'roi']
    
    models = {}
    for target in targets:
        print(f"\nTraining model for {target}...")
        
        # Prepare features
        features = ['property_type', 'district', 'land_area', 'num_floors', 
                   'area_per_floor', 'investment_per_sqm']
        if target == 'total_investment':
            features.remove('investment_per_sqm')
            
        X = df[features]
        y = df[target]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create and train model
        model = RealEstateMLModel()
        
        # Perform grid search for hyperparameter tuning
        param_grid = {
            'regressor__n_estimators': [100, 200],
            'regressor__learning_rate': [0.01, 0.05],
            'regressor__max_depth': [3, 4, 5],
            'regressor__min_samples_split': [5, 10],
            'regressor__min_samples_leaf': [3, 4]
        }
        
        grid_search = GridSearchCV(
            model.model, param_grid, cv=5, scoring='r2', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        # Use best model
        model.model = grid_search.best_estimator_
        
        # Evaluate model
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Training R² score: {r2_score(y_train, train_pred):.4f}")
        print(f"Test R² score: {r2_score(y_test, test_pred):.4f}")
        print(f"Mean absolute percentage error: {np.mean(np.abs((y_test - test_pred) / y_test)) * 100:.2f}%")
        
        # Save model
        model.save_model(f'model_{target}.joblib')
        models[target] = model
    
    return models
def train_and_save_models():
    """Train and save models for all targets"""
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    print("Generating training data...")
    df = generate_training_data(1000)
    
    targets = ['total_investment', 'total_revenue', 'gross_profit', 
              'annual_rent', 'roi']
    
    features = ['property_type', 'district', 'land_area', 'num_floors']
    
    for target in targets:
        print(f"\nTraining model for {target}...")
        
        X = df[features]
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = RealEstateMLModel()
        model.fit(X_train, y_train)
        
        # Save model in models directory
        model_path = os.path.join('models', f'model_{target}.joblib')
        model.save_model(model_path)
        print(f"Model saved as {model_path}")
        
if __name__ == "__main__":
    print("Starting model training process...")
    try:
        train_models()
    except Exception as e:
        print(f"Error during training: {str(e)}")
        import traceback
        print("Traceback:")
        print(traceback.format_exc())