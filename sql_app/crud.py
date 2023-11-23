from sqlalchemy.orm import Session

from . import models, schemas

# 주어진 사용자 id에 해당하는 사용자를 데이터베이스에서 조회
def get_user(db: Session, user_id: int):
    # User 모델을 쿼리(데이터베이스에서 User 테이블에 대한 조회작업 수행)
    # 해당 사용자를 필터링
    # first() 함수를 호출하여 첫번째 결과를 반환
    return db.query(models.User).filter(models.User.id == user_id).first()

# 주어진 email 에 해당하는 사용자를 데이터베이스에서 조회
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 데이터베이스에서 사용자들을 조회
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # offset(skip) : 데이터베이스에서 처음 skip 개의 경과를 건너뛰도록 지정
    # limit(limit) : 최대 limit 개수의 결과를 가져옴
    return db.query(models.User).offset(skip).limit(limit).all()

# 새로운 사용자를 데이터베이스에 생성
def create_user(db: Session, user: schemas.UserCreate):
    # User 모델의 인스턴스를 생성하고 주어진 사용자 정보를 사용하여 해당 인스턴스의 속성을 초기화
    db_user = models.User(email=user.email, hashed_password=user.password)
    # 새로운 사용자를 데이터베이스에 추가
    db.add(db_user)
    # 변경사항을 커밋
    db.commit()
    # 데이터베이스에서 생성된 사용자의 최신 정보를 가져옴
    db.refresh(db_user)
    # 최종적으로 생성된 사용자를 반환
    return db_user

# 데이터베이스에서 아이템들을 조회
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 새로운 아이템을 데이터베이스에 생성
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # Item 모델의 인스턴스를 생성하고, 주어진 아이템 정보와 사용자id를 사용하여 해당 인스턴스의 속성을 초기화
    # **item.dict() : item 객체의 속성들을 딕셔너리 형태로 반환하는 메서드
    # item은 schemas.ItemCreate 클래스의 인스턴스로 아이템 생성에 필요한 속성들을 가지고 있음
    # ex) title이 example item인 경우 : title : str => 'title': 'example item'
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item