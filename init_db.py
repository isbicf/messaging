from messaging.db.base import Base
from messaging.db.conn import engine

def init_db():
    print('Creating database tables if they do not exist...')
    Base.metadata.create_all(bind=engine)
    print('Database is ready.')

if __name__ == '__main__':
    init_db()
