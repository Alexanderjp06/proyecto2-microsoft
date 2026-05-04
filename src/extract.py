import pandas as pd
import os

def extract_data():
    # 1. Definir rutas
    source_dir = "data/source"
    raw_dir = "data/raw"
    
    # Asegurarnos de que la carpeta de destino exista
    os.makedirs(raw_dir, exist_ok=True)
    
    files = [
        "Sales_Fact.csv",
        "Product_Dim.csv",
        "Store_Dim.csv",
        "Employee_Dim.csv",
        "Customer_Dim.csv"
    ]
    
    print("--- Iniciando Extracción de Datos ---")
    
    # 2. Extraer del origen y cargar en raw
    for file_name in files:
        source_path = f"{source_dir}/{file_name}"
        raw_path = f"{raw_dir}/{file_name}"
        
        if not os.path.exists(source_path):
            print(f"Advertencia: El archivo {file_name} no existe en {source_dir}/.")
            continue
        
        # Leemos el archivo desde la fuente (simulando la conexión a un sistema externo)
        df = pd.read_csv(source_path)
        print(f"Extrayendo archivo: {file_name} | Total filas: {len(df)}")
        
        # Lo guardamos en nuestra área de trabajo (raw)
        df.to_csv(raw_path, index=False)
        print(f" -> Guardado con éxito en {raw_path}")

    print("\n--- Extracción Finalizada ---")

if __name__ == "__main__":
    extract_data()