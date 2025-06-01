from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence, DateTime, SmallInteger,func, Float

from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
Base= declarative_base()



class VideoGameSale(Base):
    __tablename__ = 'video_game_sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    platform = Column(String(50), nullable=False)
    year = Column(Integer)
    genre = Column(String(50))
    publisher = Column(String(100))
    na_sales = Column(Float)
    eu_sales = Column(Float)
    jp_sales = Column(Float)
    other_sales = Column(Float)
    global_sales = Column(Float)

    def __repr__(self):
        return f"<VideoGameSale(name='{self.name}', platform='{self.platform}')>"



class SuperstoreOrder(Base):
    __tablename__ = 'superstore_orders'

    row_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String)
    order_date = Column(Date)
    ship_date = Column(Date)
    ship_mode = Column(String)
    customer_id = Column(String)
    customer_name = Column(String)
    segment = Column(String)
    country = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    region = Column(String)
    product_id = Column(String)
    category = Column(String)
    sub_category = Column(String)
    product_name = Column(String)
    sales = Column(Float)
    quantity = Column(Integer)
    discount = Column(Float)
    profit = Column(Float)


class PatientCancerData(Base):
    __tablename__ = 'patient_cancer_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String)
    age = Column(Integer)
    gender = Column(String)
    country_region = Column(String)
    year = Column(Integer)
    genetic_risk = Column(Float)
    air_pollution = Column(Float)
    alcohol_use = Column(Float)
    smoking = Column(Float)
    obesity_level = Column(Float)
    cancer_type = Column(String)
    cancer_stage = Column(String)
    treatment_cost_usd = Column(Float)
    survival_years = Column(Float)
    target_severity_score = Column(Float)

from flask_login import UserMixin

class Usuario(Base, UserMixin):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
