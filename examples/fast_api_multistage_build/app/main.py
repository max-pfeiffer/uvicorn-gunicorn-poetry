from typing import Optional, Dict
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test_items/{item_id}")
def read_item(item_id: str):
    items: Dict[str, str] = {
        "1": "sausage",
        "2": "ham",
        "3": "tofu"
    }
    return items[item_id]