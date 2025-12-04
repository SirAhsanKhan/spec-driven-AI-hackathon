from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot Backend is running!"}
