from fastapi import FastAPI

app = FastAPI()


@app.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


@app.get("/tran_demo_1")
def tran_demo_1():
    return {"message": "Hello World from sub API"}


# app.mount("/subapi", subapi)
