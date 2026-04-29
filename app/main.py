from fastapi import FastAPI

app = FastAPI(title="Grupo Solar Chatbot API")


@app.get("/")
def root():
    return {"status": "ok", "message": "Chatbot online"}
