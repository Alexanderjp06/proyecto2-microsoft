import pandas as pd
import os

def extract_data():
    files = [
        "Sales_Fact.csv",
        "Product_Dim.csv",
        "Store_Dim.csv",
        "Employee_Dim.csv",
        "Customer_Dim.csv"
    ]
    
    for file_name in files:
        raw_path = f"data/raw/{file_name}"
        if not os.path.exists(raw_path):
            print(f"Advertencia: El archivo {file_name} no existe en data/raw/.")
            continue
        
        df = pd.read_csv(raw_path)
        print(f"Extrayendo archivo: {file_name} | Total filas: {len(df)}")
        
        # Mostrar las columnas del archivo actual
        print(f"Columnas: {list(df.columns)}")
        print("-" * 50) # Línea divisoria para mayor legibilidad

if __name__ == "__main__":
    extract_data()