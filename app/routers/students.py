from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database, oauth2


router = APIRouter(
    prefix="/student",
    tags=["Students"],
    dependencies=None,
    responses=None
)
get_db = database.get_db


@router.get('/{id}')
def search_by_id(id: int, db: Session = Depends(get_db), verify: schemas.User = Depends(oauth2.verify_user)):
    student_info = db.query(models.Student).filter(models.Student.id==id).first()
    if student_info is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_info


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_student(request: schemas.Student, db: Session = Depends(get_db), verify: schemas.User = Depends(oauth2.verify_user)):
    new_student = models.Student(
        name=request.name, 
        age=request.age, 
        )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


@router.get('/', response_model=schemas.Student)
def search_by_name(name: str, db: Session = Depends(get_db), verify: schemas.User = Depends(oauth2.verify_user)):
    student_info = db.query(models.Student).filter(models.Student.name==name).first()
    if student_info is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_info


@router.put('/{id}')
def update(id: int, request: schemas.Student, db: Session = Depends(get_db), verify_user: schemas.User = Depends(oauth2.verify_user)):
    db.query(models.Student).filter(models.Student.id==id).update(synchronize_session=False)
    return 'update successfully'


@router.delete('/{id}')
def delete_db(id: int, db: Session = Depends(get_db), verify_user: schemas.User = Depends(oauth2.verify_user)):
    db.query(models.Student).filter(models.Student.id==id).delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=204, detail="Deleted")
