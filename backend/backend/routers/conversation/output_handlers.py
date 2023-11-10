import asyncio
import io
import logging
import os
from typing import Union

import aiofiles
from fastapi import (APIRouter, FastAPI, Query, Request, WebSocket,
                     WebSocketDisconnect)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.conf import (get_jinja_templates_path, get_root_package_path,
                          initialise_app)


async def generate_response(user_id: str, enable_audio_output: bool) -> bytes:
    """
    Generates a response based on the user interaction.
    """
    pass
