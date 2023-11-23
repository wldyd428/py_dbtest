# SQLAlchemy 엔진을 생성하는데 사용
# SQLAlchemy 엔진은 데이터베이스와의 연결을 생성하고 관리하는 역할(통신 담당)
from sqlalchemy import create_engine
# SQLAlchemy 모델을 정의할 때 사용되는 기본 클래스를 생성하는데 사용
from sqlalchemy.ext.declarative import declarative_base
# 데이터베이스 세션을 생성하는데 사용
from sqlalchemy.orm import sessionmaker

# MySQL 데이터베이스 연결 URL 정의
# mysql+pymysql 드라이버를 사용
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://사용자명:비밀번호@localhost:3306/데이터베이스명"

# SQLAlchemy 엔진을 생성
engine = create_engine(
    # 연결 URL을 사용하고, pool_pre_ping=True 옵션으로 데이터베이스 연결 유지와 관련된 기능 활성화
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
# SQLAlchemy 세션을 생성하기위한 sessionmaker 객체를 생성
# autocommit=False, autoflush=False 옵션 설정으로 세션을 수동으로 커밋하고, 필요한 경우에만 데이터베이스와의 상호작용을 수행하도록 설정
# 앞서 생성한 SQLAlchemy 엔진을 바인딩
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델을 정의할 때 사용할 기본 클래스를 생성
# 이 클래스는 모든 SQLAlchemy 모델 클래스의 부모 클래스로 사용되며, 데이터베이스 테이블과의 매핑 및 기타 기능을 제공
Base = declarative_base()
