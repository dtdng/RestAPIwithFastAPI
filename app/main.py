from database import SessionLocal
from fastapi import FastAPI, Request, Response
from database import engine, database
import models 
from routers import students, users, login

app = FastAPI()


models.Base.metadata.create_all(engine)


app.include_router(students.router)
app.include_router(users.router)
app.include_router(login.router)


@app.on_event("startup")
async def startup_event():
    await database.connect()
    

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()    


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response 

@app.get("/")
def read_root():
    return {"Hello": "World"}
