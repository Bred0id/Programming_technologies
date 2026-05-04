from base import Base, engine, SessionLocal, User


Base.metadata.create_all(bind=engine)


db = SessionLocal()

try:
    db.add(User(login="pavel", email="a@gmail.com"))
    db.add(User(login="yura", email="b@gmail.com"))
    db.commit()
finally:
    db.close()