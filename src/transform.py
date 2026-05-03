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
        
        # Análisis detallado que tenías anteriormente
        print(f"--- Procesando y limpiando: {file_name} ---")
        print(f"  Filas iniciales: {len(df)}")
        print(f"  Valores nulos por columna:\n{df.isnull().sum()}")
        
        df_no_dupes = df.drop_duplicates()
        dupes_removed = len(df) - len(df_no_dupes)
        
        df_cleaned = df_no_dupes.dropna()
        nulls_removed = len(df_no_dupes) - len(df_cleaned)
        
        print(f"  Filas finales después de limpiar: {len(df_cleaned)}")
        print(f"  > Filas eliminadas por duplicados: {dupes_removed}")
        print(f"  > Filas eliminadas por valores nulos: {nulls_removed}")
        print(f"  > Total de filas eliminadas: {dupes_removed + nulls_removed}")
        
        # Extraer el ID de la dimensión
        id_col = file_name.replace("_Dim.csv", "_ID")
        
        if id_col in df_cleaned.columns:
            # Guardamos los IDs válidos para comprobarlos en la tabla de hechos
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
        print(f"  Filas iniciales: {len(df_fact)}")
        print(f"  Valores nulos por columna:\n{df_fact.isnull().sum()}")
        
        df_no_dupes_fact = df_fact.drop_duplicates()
        dupes_removed = len(df_fact) - len(df_no_dupes_fact)
        
        df_cleaned_fact = df_no_dupes_fact.dropna()
        nulls_removed = len(df_no_dupes_fact) - len(df_cleaned_fact)
        
        # Validar integridad referencial (elimina transacciones con IDs que no existen en dimensiones)
        for id_col, valid_set in valid_ids.items():
            if id_col in df_cleaned_fact.columns:
                df_cleaned_fact = df_cleaned_fact[df_cleaned_fact[id_col].isin(valid_set)]
        
        # Transformación adicional (ej. calcular monto total si están las columnas)
        if 'Quantity' in df_cleaned_fact.columns and 'Unit_Price' in df_cleaned_fact.columns:
            df_cleaned_fact['Total_Amount'] = df_cleaned_fact['Quantity'] * df_cleaned_fact['Unit_Price']
        
        # Guardar la tabla de hechos procesada
        df_cleaned_fact.to_csv(processed_fact_path, index=False)
        print(f"  -> Hechos limpios y validados en: {processed_fact_path}")
        print(f"  > Filas eliminadas por duplicados: {dupes_removed}")
        print(f"  > Filas eliminadas por valores nulos: {nulls_removed}")
        print(f"  -> Filas finales en la tabla de hechos: {len(df_cleaned_fact)}")
        
    else:
        print(f"Advertencia: El archivo {fact_file} no existe en data/raw/.")
        
    print("--- Transformación Finalizada ---")

if __name__ == "__main__":
    transform_data()