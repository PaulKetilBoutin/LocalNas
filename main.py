from fastapi import FastAPI, File, UploadFile
from os import listdir
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/", response_class=HTMLResponse)
def read_items():
    disp = "<html><body><ul>"
    for i in listdir("/home/corino/NAS/"):
        disp += "<li><a href='/dowloads/"+i+"' download='"+i"'>"+i+"</a></li>"
    disp += "</ul>"
    disp += """<form action='/uploadfile/' method='post' enctype='multipart/form-data'>
    Select file to upload:
    <input type='file' name='file' id='file' accept='*/*'>
    <input type='submit' value='submit'></form>"""
    disp += "</body></html>"
    return disp

@app.get("/dowloads/{item_path}")
def return_doc(item_path):
    def file_transf():
        with open("/home/corino/NAS/"+item_path, mode="rb") as file_buf:
            yield from file_buf
    return StreamingResponse(file_transf())
    
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        with open("/home/corino/NAS/"+file.filename, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception as e:
        return {"message": e.args}
    await file.close()
    return {"filename": file.filename}
