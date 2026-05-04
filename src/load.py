import os
import pandas as pd
from sqlalchemy import create_engine
import urllib

def load_data_to_azure():
    # 1. Configuración de conexión a Azure SQL
    server = 'servidor-etl-estudiante.database.windows.net' 
    database = 'tienda_db' 
    
    # Obtener credenciales desde las variables de entorno de GitHub
    username = os.environ.get('AZURE_SQL_USER')
    password = os.environ.get('AZURE_SQL_PASSWORD')
    
    # Cadena de conexión usando SQLAlchemy y pyodbc
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    
    # Lista de archivos limpios y sus nombres de tablas en SQL Server
    files_to_load = [
        ("Product_Dim.csv", "Product_Dim"),
        ("Store_Dim.csv", "Store_Dim"),
        ("Employee_Dim.csv", "Employee_Dim"),
        ("Customer_Dim.csv", "Customer_Dim"),
        ("Sales_Fact.csv", "Sales_Fact")
    ]
    
    print("--- Iniciando carga de datos a Azure SQL ---")
    
    # 2. Iterar y cargar cada archivo a la base de datos
    for file_name, table_name in files_to_load:
        processed_path = f"data/processed/{file_name}"
        
        if os.path.exists(processed_path):
            print(f"\nCargando {file_name} en la tabla {table_name}...")
            df = pd.read_csv(processed_path)
            
            # Subir a Azure SQL
            df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=10000)
            print(f" -> Tabla {table_name} cargada con éxito.")
        else:
            print(f" Advertencia: El archivo procesado {file_name} no existe.")

    print("\n--- Carga de datos finalizada ---")

if __name__ == "__main__":
    load_data_to_azure()