from fastapi import FastAPI
from data.database import engine, Base
from api.endpoints import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Distribution CRM", version="1.0.0")
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Lead Distribution CRM API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)