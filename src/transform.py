import pandas as pd
import os

def transform_data():
    os.makedirs('data/processed', exist_ok=True)
    
    dim_files = [
        "Product_Dim.csv",
        "Store_Dim.csv",
        "Employee_Dim.csv",
        "Customer_Dim.csv"
    ]
    
    fact_file = "Sales_Fact.csv"
    
    # Diccionario para almacenar los IDs válidos de las dimensiones
    valid_ids = {}
    
    print("--- 1. Procesando Dimensiones (Maestros) ---")
    
    for file_name in dim_files:
        raw_path = f"data/raw/{file_name}"
        processed_path = f"data/processed/{file_name}"
        
        if not os.path.exists(raw_path):
            print(f"Advertencia: El archivo {file_name} no existe en data/raw/.")
            continue
            
        df = pd.read_csv(raw_path)
        
        print(f"--- Procesando y limpiando: {file_name} ---")
        print(f"  Filas iniciales: {len(df)}")
        
        df_no_dupes = df.drop_duplicates()
        df_cleaned = df_no_dupes.dropna()
        
        # Extraer el ID de la dimensión
        id_col = file_name.replace("_Dim.csv", "_ID")
        
        if id_col in df_cleaned.columns:
            valid_ids[id_col] = set(df_cleaned[id_col])
        
        df_cleaned.to_csv(processed_path, index=False)
        print(f"  -> Guardado en {processed_path}\n{'-'*50}")

    # --- Procesamiento de Tabla de Hechos ---
    print("\n--- 2. Procesando Tabla de Hechos (Transacciones) ---")
    
    raw_fact_path = f"data/raw/{fact_file}"
    processed_fact_path = f"data/processed/{fact_file}"
    
    if os.path.exists(raw_fact_path):
        df_fact = pd.read_csv(raw_fact_path)
        
        print(f"--- Procesando y limpiando: {fact_file} ---")
        
        df_no_dupes_fact = df_fact.drop_duplicates()
        df_cleaned_fact = df_no_dupes_fact.dropna()
        
        # Validar integridad referencial
        for id_col, valid_set in valid_ids.items():
            if id_col in df_cleaned_fact.columns:
                df_cleaned_fact = df_cleaned_fact[df_cleaned_fact[id_col].isin(valid_set)]
        
       # ==============================================================
        # CORRECCIÓN: ESTANDARIZACIÓN DE FECHAS "MODO ESTRICTO"
        # ==============================================================
        if 'Sale_Date' in df_cleaned_fact.columns:
            # 1. Convertimos a fecha, forzando a que lo que no se entienda se vuelva nulo (NaT)
            df_cleaned_fact['Sale_Date'] = pd.to_datetime(df_cleaned_fact['Sale_Date'], format='mixed', errors='coerce')
            
            # 2. Eliminamos las filas donde la fecha era pura basura y no se pudo convertir
            df_cleaned_fact = df_cleaned_fact.dropna(subset=['Sale_Date'])
            
            # 3. Le damos el formato SQL perfecto a toda la columna
            df_cleaned_fact['Sale_Date'] = df_cleaned_fact['Sale_Date'].dt.strftime('%Y-%m-%d')
        # ==============================================================
        # REDONDEO DE DECIMALES
        # ==============================================================
        if 'Quantity' in df_cleaned_fact.columns and 'Unit_Price' in df_cleaned_fact.columns:
            df_cleaned_fact['Total_Amount'] = round(df_cleaned_fact['Quantity'] * df_cleaned_fact['Unit_Price'], 2)
            
        if 'Total_Price' in df_cleaned_fact.columns:
            df_cleaned_fact['Total_Price'] = round(df_cleaned_fact['Total_Price'], 2)
            
        if 'Shipping_Cost' in df_cleaned_fact.columns:
            df_cleaned_fact['Shipping_Cost'] = round(df_cleaned_fact['Shipping_Cost'], 2)
        
        # Guardar la tabla de hechos procesada
        df_cleaned_fact.to_csv(processed_fact_path, index=False)
        print(f"  -> Hechos limpios, fechas corregidas y validados en: {processed_fact_path}")
        
    else:
        print(f"Advertencia: El archivo {fact_file} no existe en data/raw/.")
        
    print("--- Transformación Finalizada ---")

if __name__ == "__main__":
    transform_data()