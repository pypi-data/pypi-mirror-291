from fastapi import FastAPI

app = FastAPI()


@app.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


# app.mount("/subapi", subapi)
