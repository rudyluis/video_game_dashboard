import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Agrega el path al directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el modelo y Base
from models.model import Base, PatientCancerData  # ← Asegúrate de tener definido este modelo

# Configura tu conexión
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/video_games"  # Local (puedes comentarlo si no lo usas)
DATABASE_URL = "postgresql://dbgame_sfhn_user:5UEkhDNGJaMQfAa5sNfHlZbPrFkoGCGF@dpg-d0llaopr0fns738g24og-a.oregon-postgres.render.com/dbgame_sfhn"

# Crear engine y sesión
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Crear tablas si no existen
Base.metadata.create_all(engine)

# URL del CSV de cáncer global
CSV_URL = "https://raw.githubusercontent.com/rudyluis/DashboardJS/refs/heads/main/global_cancer.csv"

# Leer el CSV
df = pd.read_csv(CSV_URL)

# Renombrar columnas para que coincidan con el modelo (opcional si usas nombres ya limpios)
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

# Convertir tipos
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Convertir a lista de objetos PatientCancerData
records = [
    PatientCancerData(
        patient_id=row['patient_id'],
        age=int(row['age']) if not pd.isna(row['age']) else None,
        gender=row['gender'],
        country_region=row['country_region'],
        year=int(row['year']) if not pd.isna(row['year']) else None,
        genetic_risk=row['genetic_risk'],
        air_pollution=row['air_pollution'],
        alcohol_use=row['alcohol_use'],
        smoking=row['smoking'],
        obesity_level=row['obesity_level'],
        cancer_type=row['cancer_type'],
        cancer_stage=row['cancer_stage'],
        treatment_cost_usd=row['treatment_cost_usd'],
        survival_years=row['survival_years'],
        target_severity_score=row['target_severity_score']
    )
    for _, row in df.iterrows()
]

# Insertar en la base de datos
session.bulk_save_objects(records)
session.commit()
print("✅ Migración de datos completada:", len(records))
session.close()
