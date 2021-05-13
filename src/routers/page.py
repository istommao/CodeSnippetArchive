"""routers."""
from typing import Optional

import jinja2

from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory='html')


@router.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/snippet/{tool_name}/')
async def tb_page(request: Request, tool_name: str):
    print(tool_name)
    tpl_name = 'snippet/detail.html'
    try:
        resp = templates.TemplateResponse(tpl_name, {'request': request})
    except jinja2.exceptions.TemplateNotFound:
        return templates.TemplateResponse('home.html', {'request': request})
    else:
        return resp
