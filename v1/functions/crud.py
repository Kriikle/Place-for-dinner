from sqlalchemy.orm import Session
from pydantic import BaseModel
from config.connection import Base


def get_all_(model: Base, db: Session):
    return db.query(model).all()


def get_one_(model: Base, item_id: int, db: Session):
    return db.get(model, item_id)


def create_(model: Base, new_row: BaseModel, db: Session):
    db_new_row = model(**dict(new_row))
    db.add(db_new_row)
    db.commit()
    db.refresh(db_new_row)
    return db_new_row


def update_(model: Base, new_row: BaseModel, item_id: int, db: Session, row=None):
    if row is None:
        row = db.get(model, item_id)
    if row is None:
        return row
    row_dict = new_row.dict(exclude_unset=True)
    for key, value in row_dict.items():
        if value is not None:
            setattr(row, key, value)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def delete_(model: Base, item_id: int, db: Session, row=None):
    if row is None:
        row = db.get(model, item_id)
    if row is None:
        return row
    db.delete(row)
    db.commit()
    return True
