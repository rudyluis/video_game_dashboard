import pandas as pd
from sqlalchemy import create_engine
import os
import sys
# Agrega el path al directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.model import Base, VideoGameSale
from sqlalchemy.orm import sessionmaker

# Configura tu conexión
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/video_games"  # ← cámbialo
DATABASE_URL = "postgresql://dbgame_sfhn_user:5UEkhDNGJaMQfAa5sNfHlZbPrFkoGCGF@dpg-d0llaopr0fns738g24og-a.oregon-postgres.render.com/dbgame_sfhn"
# Crear engine y sesión
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Crear tablas si no existen
Base.metadata.create_all(engine)

# Leer el CSV con pandas
CSV_URL = "https://raw.githubusercontent.com/rudyluis/DashboardJS/refs/heads/main/video_games_sales.csv"

df = pd.read_csv(CSV_URL)

# Limpieza / transformación si es necesario
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Convertir DataFrame en lista de objetos VideoGameSale
records = [
    VideoGameSale(
        rank=int(row['Rank']),
        name=row['Name'],
        platform=row['Platform'],
        year=int(row['Year']) if not pd.isna(row['Year']) else None,
        genre=row['Genre'],
        publisher=row['Publisher'],
        na_sales=row['NA_Sales'],
        eu_sales=row['EU_Sales'],
        jp_sales=row['JP_Sales'],
        other_sales=row['Other_Sales'],
        global_sales=row['Global_Sales']
    )s
    for index, row in df.iterrows()
]

# Insertar en la base de datos
session.bulk_save_objects(records)
session.commit()
print("✅ Migración de datos completada")
session.close()
