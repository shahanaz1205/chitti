from fastapi import FastAPI
from database import engine, Base
import models.user  
import models.event
import models.registration
from routers import auth, events, registrations


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(registrations.router)

@app.get("/")
def home():
    return {"message": "Hello! My FastAPI server is running!"}