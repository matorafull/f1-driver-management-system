from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from src.database import Base

race_results = Table(
    "race_results",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("driver_id", Integer, ForeignKey("drivers.id")),
    Column("team_id", Integer, ForeignKey("teams.id")),
    Column("race_name", String),
    Column("points_earned", Float),
    Column("race_date", Date)
)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    base_location = Column(String)
    team_principal = Column(String)
    engine_supplier = Column(String)

    contracts = relationship("Contract", back_populates="team")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    driver_code = Column(String, unique=True)
    nationality = Column(String)
    permanent_number = Column(Integer, unique=True)
    is_active = Column(Boolean, default=True)

    contracts = relationship("Contract", back_populates="driver")

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    salary_m_usd = Column(Float)

    driver = relationship("Driver", back_populates="contracts")
    team = relationship("Team", back_populates="contracts")

class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    race_date = Column(Date, nullable=False)
    season = Column(Integer, nullable=False)
    location = Column(String)