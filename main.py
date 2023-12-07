from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from router import router

app = FastAPI()
app.include_router(router)


# @app.exception_handler(RequestValidationError)
# def custom_handler(request: Request, exc: RequestValidationError):
#     errors = exc.errors()
#     for error in errors:
#         del error["loc"]
#         del error["ctx"]
#         del error["url"]
#     print(errors)
#     return JSONResponse(jsonable_encoder({"details": errors}), status_code=422)
