from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from router import router

app = FastAPI()
app.include_router(router)

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

# @app.exception_handler(RequestValidationError)
# def custom_handler(request: Request, exc: RequestValidationError):
#     errors = exc.errors()
#     for error in errors:
#         del error["loc"]
#         del error["ctx"]
#         del error["url"]
#     print(errors)
#     return JSONResponse(jsonable_encoder({"details": errors}), status_code=422)
