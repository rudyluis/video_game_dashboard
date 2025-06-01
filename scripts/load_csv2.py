import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Agrega el path al directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el modelo y Base
from models.model import Base, SuperstoreOrder  # Asegúrate de tener definido este modelo

# Configura tu conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:123456@localhost:5432/video_games"  # ← cámbialo si es necesario
DATABASE_URL = "postgresql://dbgame_sfhn_user:5UEkhDNGJaMQfAa5sNfHlZbPrFkoGCGF@dpg-d0llaopr0fns738g24og-a.oregon-postgres.render.com/dbgame_sfhn"

# Crear engine y sesión
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Crear tablas si no existen
Base.metadata.create_all(engine)

# URL del CSV del Superstore
CSV_URL = "https://raw.githubusercontent.com/rudyluis/DashboardJS/refs/heads/main/superstore_data.csv"

# Leer el CSV
df = pd.read_csv(CSV_URL)

# Renombrar columnas para que coincidan con el modelo
df.rename(columns={
    'RowID': 'row_id',
    'OrderID': 'order_id',
    'OrderDate': 'order_date',
    'ShipDate': 'ship_date',
    'ShipMode': 'ship_mode',
    'CustomerID': 'customer_id',
    'CustomerName': 'customer_name',
    'Segment': 'segment',
    'Country': 'country',
    'City': 'city',
    'State': 'state',
    'Postal Code': 'postal_code',
    'Region': 'region',
    'ProductID': 'product_id',
    'Category': 'category',
    'Sub-Category': 'sub_category',
    'ProductName': 'product_name',
    'Sales': 'sales',
    'Quantity': 'quantity',
    'Discount': 'discount',
    'Profit': 'profit'
}, inplace=True)

# Convertir fechas a formato date
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce').dt.date
df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce').dt.date

# Convertir a lista de objetos SuperstoreOrder
records = [
    SuperstoreOrder(
        row_id=int(row['row_id']),
        order_id=row['order_id'],
        order_date=row['order_date'],
        ship_date=row['ship_date'],
        ship_mode=row['ship_mode'],
        customer_id=row['customer_id'],
        customer_name=row['customer_name'],
        segment=row['segment'],
        country=row['country'],
        city=row['city'],
        state=row['state'],
        postal_code=str(row['postal_code']) if not pd.isna(row['postal_code']) else None,
        region=row['region'],
        product_id=row['product_id'],
        category=row['category'],
        sub_category=row['sub_category'],
        product_name=row['product_name'],
        sales=row['sales'],
        quantity=row['quantity'],
        discount=row['discount'],
        profit=row['profit']
    )
    for _, row in df.iterrows()
]

# Insertar en la base de datos
session.bulk_save_objects(records)
session.commit()
print("✅ Migración de datos completada ", len(records))
session.close()
