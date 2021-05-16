"""fake data helper."""
import time

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
