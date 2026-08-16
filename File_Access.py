from fastapi import FastAPI, File, UploadFile, HTTPException, Depends


app = FastAPI(title = "File Access API", description = "API for accessing files securely", version = "1.0.0")

'''class File(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    filename : str 
    file_type : str '''

@app.post("/files/uploads")
async def upload_file(file: UploadFile= File(...)):
    with open(f"uploads/{file.filename}" , "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "message": "File uploaded successfully"}
        
    