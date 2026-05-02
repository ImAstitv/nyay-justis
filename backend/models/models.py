from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True)
    cnr_number = Column(String, unique=True)
    status = Column(String, default="Active", nullable=False)
    case_type = Column(String, default="General")
    petitioner = Column(String)
    respondent = Column(String)
    citizen_username = Column(String, nullable=True)
    filed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    under_acts = Column(String)
    under_sections = Column(String)
    filing_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    first_hearing_date = Column(DateTime)
    current_stage = Column(String, default="Pre-Trial")
    establishment_code = Column(String, default="BRPA20")
    primary_case_nature = Column(String, default="Civil")
    custody_status = Column(String, default="None")
    immediate_risk = Column(String, default="None")
    financial_stake = Column(Boolean, default=False)
    estimated_severity = Column(String, default="Low")
    is_undertrial = Column(Boolean, default=False)
    days_in_custody = Column(Integer, default=0)
    priority_score = Column(Float, default=0)
    aging_factor = Column(Float, default=0)
    friction_index = Column(Integer, default=0)
    vulnerability = Column(Float, default=1.0)
    stage_coeff = Column(Float, default=1.0)
    omega_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hearings = relationship("Hearing", back_populates="case", cascade="all, delete")

class Hearing(Base):
    __tablename__ = "hearings"
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    judge_id = Column(Integer, ForeignKey("users.id"))
    business_on_date = Column(DateTime)
    next_hearing_date = Column(DateTime)
    purpose_of_hearing = Column(String)
    adjournment_reason = Column(String)
    adjourned_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    case = relationship("Case", back_populates="hearings")

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    action = Column(String)
    performed_by_role = Column(String)
    old_value = Column(Text)
    new_value = Column(Text)
    detail = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
