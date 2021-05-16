"""fake data helper."""
import time
import os
import fnmatch

from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, Request, APIRouter

from src.config import ROOT_DIR

router = APIRouter()


class SnipetForm(BaseModel):
    # 标题
    title: str

    # 语言
    language: str

    # 代码内容
    content: str
    desc: Optional[str] = None


@router.post('/api/snippet/')
async def save_snippet_api(form: SnipetForm):

    filename = ROOT_DIR + '/static/media/' + form.title + '.md'

    with open(filename, 'w') as fd:
        fd.write(form.content)

    return {'success': True}


@router.get('/api/snippets/')
async def get_snippet_api():

    files = [
        f
        for dirpath, dirnames, files in os.walk(ROOT_DIR + '/static/media/')
        for f in fnmatch.filter(files, '*.md')
    ]

    snippets = [
        '/snippet/{}/'.format(item.replace('.md', ''))
        for item in files
    ]

    return {'snippets': snippets}

