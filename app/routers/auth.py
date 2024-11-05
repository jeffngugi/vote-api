from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, Oath2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
   tags=["Authentication"]
)

@router.post('/login')
def login(user_credential: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credential.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    
    # create a token
    access_token = Oath2.create_access_token(data={
        "user_id":user.id
    })
    
    return {"access_token" : access_token, "token_type": "bearer"}
    #return token
    return "Correct credentionas"
    # pass