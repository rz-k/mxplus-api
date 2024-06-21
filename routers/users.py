from fastapi import APIRouter, Body, Depends
from schema.input_ import UserInputRegister, UserUpdate
from database import UserDB, get_user_db

router = APIRouter()


@router.post("/register")
async def register(data:UserInputRegister=Body(), db: UserDB = Depends(get_user_db)):

    await db.create_user(
        username=data.username,
        email=data.email,
        passwd=data.passwd,
        token=data.token,
        expire_in=data.expire_in,
        transfer_enable=data.transfer_enable
    )
    return data

@router.post("/update/{email}")
async def update(email, data: UserUpdate=Body(), db: UserDB = Depends(get_user_db)):
    await db.update(
        email=email,
        expire_in=data.expire_in,
        transfer_enable=data.transfer_enable
    )
    return data

@router.get("/get/{email}/")
async def get_user(email:str, db: UserDB = Depends(get_user_db)):
    user = await db.select(email=email)
    return user
