from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# https://apis.data.go.kr/6260000/AttractionService/getAttractionKr?serviceKey=L4O6Jd5locofQV0Sa674EwMQ4GyHi380DNlzkWVMQLw8O2LvzNMvBKe1RxTj4jssgmQKPrDvinJFtSOIs9KmbA%3D%3D&pageNo=1&numOfRows=10&resultType=json


class ResponseDTO(BaseModel):
    code: int
    message: str
    data: object | None


class Cat(BaseModel):
    name: str
    id: int = 0


app = FastAPI()


origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/first/{id}")
async def root(id: int):
    return {"message": "Hello World", "id": id}


@app.get("/second")
async def second(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.post("/cat")
async def cat(cat: Cat):
    return cat


@app.get("/error")
async def error():
    dto = ResponseDTO(
        code=0,
        message="페이지가 없습니다.",
        data=None
    )
    return JSONResponse(status_code=404, content=jsonable_encoder(dto))


@app.get("/error1")
async def error1():
    raise HTTPException(status_code=404, detail={"message": "Item not found"})


@app.post("/files/")
async def check_file(
    uploadFile: UploadFile = File(), token: str = Form()
):
    return {
        "token": token,
        # "uploadFileSize": len(await upload_file.read()),
        "uploadFileName": uploadFile.filename,
        "uploadFileContentType": uploadFile.content_type,
    }
