# 데이터의 유효성 검사와 직렬화를 위해 Pydantic 모델을 사용
# 이를 통해 데이터의 구조와 유효성을 확인하고 필요한 경우 데이터를 데이터베이스 모델과 상호 변환할 수 있음
# Pydantic 모델은 FastAPI와 함께 사용되는 경우 많이 활용되며, 데이터의 검증과 직렬화에 효과적
from pydantic import BaseModel

# Item 모델의 기본 속성 정의
class ItemBase(BaseModel):
    title: str
    description: str | None = None

# Item 모델의 생성에 필요한 속성 정의
# Item 모델을 상속받아 추가적인 속성 없음
class ItemCreate(ItemBase):
    pass

# Item 모델을 정의하는 class
# ItemBase를 상속받아 id와 owner_id 속성을 추가
class Item(ItemBase):
    id: int
    owner_id: int

    # Config 클래스 내에 orm_mode = True로 설정되어있어 SQLAlchemy 모델과의 상호 변환을 가능하게 함
    class Config:
        orm_mode = True

# User 모델의 기본 속성 정의
class UserBase(BaseModel):
    email: str

# User 모델의 생성에 필요한 속성 정의
# UserBase를 상속받아 password 속성을 추가
class UserCreate(UserBase):
    password: str

# User 모델을 정의하는 class
# UserBase를 상속받아 id, is_active, items 속성을 추가
# items 속성은 list[Item] 타입으로 정의되어있으며, 기본값으로 빈 리스트를 설정
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    # Config 클래스 내에 orm_mode = True로 설정되어있어 SQLAlchemy 모델과의 상호 변환을 가능하게 함
    class Config:
        orm_mode = True