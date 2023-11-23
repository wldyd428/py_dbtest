from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# SQLAlchemy 모델에 정의된 테이블들을 데이터베이스에 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# get_db() 함수는 데이터베이스 세션을 생성하고 관리하기 위한 의존성(Dependency) 함수
def get_db():
    # SessionLocal()을 호출하여 데이터베이스 세션을 생성
    db = SessionLocal()
    # yield db를 통해 생성된 세션을 반환. 이를 통해 FastAPI는 해당 세션을 의존성으로 주입
    try:
        yield db
    # 응답처리가 완료되면 finally 블록에서 세션을 닫음
    finally:
        db.close()

# 메서드로 엔드포인트에 요청이 오면 실행되는 함수
# 반환값이 schemas.User 모델과 일치해야함
@app.post("/users/", response_model=schemas.User)
# schemas.UserCreate 모델로 받은 사용자 정보를 이용하여 사용자를 생성
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 데이터베이스에서 email로 사용자를 조회
    db_user = crud.get_user_by_email(db, email=user.email)
    # 만약 이미 해당 이메일로 등록된 사용자가 존재한다면
    if db_user:
        # HTTPException을 발생시켜 400코드와 메시지 반환
        raise HTTPException(status_code=400, detail="Email already registered")
    # 그렇지 않다면 사용자를 생성하고 반환
    return crud.create_user(db=db, user=user)

# 반환값이 schemas.User 모델의 리스트와 일치해야함
@app.get("/users/", response_model=list[schemas.User])
# 데이터베이스에서 사용자들을 조회
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 데이터베이스에서 사용자들을 조회하고 조회된 사용자들을 반환
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# 주어진 user_id에 해당하는 사용자를 데이터베이스에서 조회하고, 조회된 사용자를 schemas.User 모델로 응답
# {user_id} : 경로 매개변수로, 요청 URL에서 해당 위치의 값을 user_id 변수에 전달
@app.get("/users/{user_id}", response_model=schemas.User)
# 주어진 user_id에 해당하는 사용자를 데이터베이스에서 조회
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    # 만약 조회된 사용자가 없다면 HTTPException를 발생시켜 상태코드와 메시지 반환
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # 그렇지 않다면 조회된 사용자를 반환
    return db_user

# 주어진 user_id에 해당하는 사용자에게 아이템을 생성. 생성된 아이템을 schemas.Item 모델로 응답
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    # 아이템을 생성하고 반환
    return crud.create_user_item(db=db, item=item, user_id=user_id)

# 데이터베이스에서 아이템들을 조회하고, 조회된 아이템들을 schemas.Item 모델의 리스트로 응답
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
