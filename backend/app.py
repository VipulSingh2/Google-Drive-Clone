from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from fastapi.responses import FileResponse
import shutil
from models import MetaData
from datetime import datetime
import json
import sqlite3

app = FastAPI()

storage = os.path.join("backend", "storage")
metadata_dir = os.path.join("backend", "metadata")

os.makedirs(storage, exist_ok=True)
os.makedirs(metadata_dir, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to cloud project"}

@app.get("/view")
def view() -> list:
    return os.listdir(storage)

@app.post("/upload")
async def upload_file(file: UploadFile = File(..., description="Upload a file here")):
    if not file:
        raise HTTPException(status_code=400, detail="No file sent")
    
    file_path = os.path.join(storage, file.filename)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    
    metadata = MetaData(
        filename=file.filename,
        size=os.path.getsize(file_path),
        headers=dict(file.headers),
        content_type=file.content_type,
        upload_time=datetime.now()  # optional if you didn't use default_factory in model
    )

    metadata_path = os.path.join(metadata_dir, f"{file.filename}.json")
    with open(metadata_path, "w") as meta_file:
        json.dump(metadata.model_dump(), meta_file, indent=4, default=str)

    return {"message": "{file.filename} saved successfully ✅"}

# download
@app.get("/download/{filename}")
async def download_file(filename:str):
    file_path = os.path.join(storage,filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="File not found")
    return FileResponse(path=file_path,filename=filename)

# delete a file
@app.delete("/delete/{filename}")
async def file_delete(filename:str):
    file_path = os.path.join(storage,filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,detail="File not found")
    os.remove(file_path)
    return {"message":"f{filename} deleted successfully"}