import pandas as pd
import os

def transform_data():
    files = [
        "Sales_Fact.csv",
        "Product_Dim.csv",
        "Store_Dim.csv",
        "Employee_Dim.csv",
        "Customer_Dim.csv"
    ]
    
    for file_name in files:
        raw_path = f"data/raw/{file_name}"
        processed_path = f"data/processed/{file_name}"
        
        if not os.path.exists(raw_path):
            print(f"Advertencia: El archivo {file_name} no existe en data/raw/.")
            continue
            
        print(f"--- Procesando y limpiando: {file_name} ---")
        df = pd.read_csv(raw_path)
        
        # 1. Reporte inicial de los datos
        print(f"  Filas iniciales: {len(df)}")
        print(f"  Valores nulos por columna:\n{df.isnull().sum()}")
        
        # 2. Paso A: Eliminar duplicados y contar cuántos se eliminaron
        df_no_dupes = df.drop_duplicates()
        dupes_removed = len(df) - len(df_no_dupes)
        
        # 3. Paso B: Eliminar nulos y contar cuántos se eliminaron
        df_cleaned = df_no_dupes.dropna()
        nulls_removed = len(df_no_dupes) - len(df_cleaned)
        
        # 4. Reporte final detallado
        print(f"  Filas iniciales para limpiar: {len(df_cleaned)}")
        print(f"  > Filas eliminadas por duplicados: {dupes_removed}")
        print(f"  > Filas eliminadas por valores nulos: {nulls_removed}")
        print(f"  > Total de filas eliminadas: {dupes_removed + nulls_removed}")
        
        # 5. Asegurar que el directorio de salida existe y guardar
        os.makedirs('data/processed', exist_ok=True)
        df_cleaned.to_csv(processed_path, index=False)
        print(f"  -> Guardado en {processed_path}\n{'-'*50}")

if __name__ == "__main__":
    transform_data()