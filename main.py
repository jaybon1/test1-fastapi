from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ResponseDTO(BaseModel):
    code: int
    message: str
    data: object | None


class Cat(BaseModel):
    name: str
    id: int = 0


app = FastAPI()


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
