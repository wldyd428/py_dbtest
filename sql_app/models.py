from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# users라는 테이블과 매핑되는 사용자 모델
class User(Base):
    # 테이블 이름 정의
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    # 계정의 활성화 상태
    is_active = Column(Boolean, default=True)

    # 사용자와 아이템 간의 일대다 관계를 나타내는 관계속성
    # Item 클래스와 owner 속성을 통해 연결
    items = relationship("Item", back_populates="owner")

# items라는 테이블과 매핑되는 아이템 모델
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="items")