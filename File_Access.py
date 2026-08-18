from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from uuid import uuid4, UUID
from pathlib import Path
#from pydantic import BaseModel, Field 

app = FastAPI(title = "File Access API", description = "API for accessing files securely", version = "1.0.0")

target = Path("uploads")
target.mkdir(exist_ok=True)

files = {}

'''class File(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    filename : str 
    file_type : str'''


@app.post("/files/uploads")
async def upload_file(file: UploadFile= File(...)):
    file_id = uuid4()
    file_path = target/file.filename
    
    with open(file_path , "wb") as f:
        f.write(await file.read())
        files[str(file_id)] = {
            "filename" : file.filename,
            "filetype": file.content_type
        }

    return {
        "file_id" : file_id, 
        "filename": file.filename,
        "message": "File uploaded successfully"
        }
        
@app.get("/file/details")
async def file_detail(name: str ):
    for key, data in files.items():
        filename = Path(data["filename"]).stem
        if filename == name:
            return{
                "file_id" : key,
                "filename" : data["filename"],
                "filetype" : data["filetype"]
            }
    raise HTTPException(status_code=404, detail="file not found")

@app.get("/files/{name}/download")
async def download_file(name: str):
    for item in target.iterdir():
        if item.stem == name:
            return FileResponse(
                path = item,
                filename= item.name      
    )
    raise HTTPException(status_code=404, detail= "File not found")

@app.delete("/files/{name}")
async def delete_file(name: str):
    for i in target.iterdir():
        if i.stem == name:
            i.unlink()
            for key, data in files.items():
                if Path(data["filename"]).stem == name:
                    del files[key]
                    break
            return {"message":"file deleted "}
    raise HTTPException(status_code=404, detail="file not found")


            
    
        