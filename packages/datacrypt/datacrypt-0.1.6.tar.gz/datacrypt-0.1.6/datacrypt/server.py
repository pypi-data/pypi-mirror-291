# general
import sys
import os
import pathlib
import uvicorn
from typing import Union

# FastApi
from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from pydantic import BaseModel

# local
import utils

# auth2
from codeme import auth2

# cmd: `datacrypt server` inside the desired directory
CWD = utils.CWD
PATH_HERE = pathlib.Path(__file__).parent.resolve()
PARENT_PATH_HERE = pathlib.Path(__file__).parent.parent.resolve()
PUBLIC_DIR_PATH = directory = os.path.join(PATH_HERE, "web/public")
STATIC_DIR_PATH = directory = os.path.join(PATH_HERE, "web/static")
TEMPLATES_DIR_PATH = directory = os.path.join(PATH_HERE, "web/templates")
FAVICON_PATH = os.path.join(PUBLIC_DIR_PATH, 'favicon.ico')
MANIFEST_PATH = os.path.join(PUBLIC_DIR_PATH, 'manifest.json')
sys.path.append(CWD)


# DI instance
DI = None


def mainlet():
    global DI
    if(DI == None):
        DI = utils.getInstance()
    else:
        pass


# Web Server Below
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount('/static',
          StaticFiles(directory=STATIC_DIR_PATH), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR_PATH)


@app.get('/favicon.ico')
async def favicon():
    return FileResponse(FAVICON_PATH)


@app.get('/manifest.json')
async def manifest():
    return FileResponse(MANIFEST_PATH)


@app.get("/")
@app.get("/dashboard/")
@app.get("/documentation/")
def read_root(request: Request):
    global CWD
    return templates.TemplateResponse("index.html", {"request": request, "cwd": CWD})


class Action(BaseModel):
    param1: str
    param2: Union[str, None] = None
    param3: Union[str, None] = None
    param4: Union[str, None] = None
    param5: Union[str, None] = None


FORBIDDEN = { "message": "Un-Authorized" }


@app.get("/actions")
def actionsGet(param1: str = '', param2: str = None, param3: str = None, request: Request = {}):
    mainlet()
    token = request.headers.get('token')
    if(auth2.authorizeToken(DI, token)):
        pass
    else:
        return FORBIDDEN
    diResponse = DI.run(param1, param2)
    response = {'param1': param1,
                'param2': param2, 'response': diResponse}
    return response


class Status(BaseModel):
    pageNumber: int
    pageSize: int
    orderType: str


@app.get("/status")
def actionsGet(request: Request = {}):
    mainlet()
    token = request.headers.get('token')
    # print("token: ", token)
    if(auth2.authorizeToken(DI, token)):
        pass
    else:
        return FORBIDDEN
    diResponse = DI.run('status')
    response = {'response': diResponse}
    return response


@app.post("/actions")
def actionsPost(action: Action, request: Request):
    mainlet()
    token = request.headers.get('token')
    if(auth2.authorizeToken(DI, token)):
        pass
    else:
        return FORBIDDEN
    response = DI.run(action.param1, action.param2,
                      action.param3, action.param4, action.param5)
    return {'param1': action.param1, 'param2': action.param2, 'response': response}


class Authenticate(BaseModel):
    origin: str


@app.post("/authenticate")
def authenticatePost(action: Authenticate):
    mainlet()
    return DI.authenticate(action.origin)


if __name__ == "__main__":
    VARIANT=4 # default

    if(VARIANT == 3):
        print("VARIANT:", 3, " ", "Multiple File Run")
        # web app run
        uvicorn.run('server:app', host="127.0.0.1",
                    port=int('8675'),
                    workers=1,
                    reload=True,
                    # reload_includes=[
                    #     '.', '/home/un5/gitlab/programmingToolsOrg/pypi/sankethosalli/datacrypt/vs/datacrypt/datacrypt/']
                    )
        
    elif(VARIANT == 4):
        print("VARIANT:", 4, " ", "Single Folder Run")
