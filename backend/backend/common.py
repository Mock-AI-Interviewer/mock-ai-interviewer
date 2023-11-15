from fastapi.templating import Jinja2Templates

from backend.conf import get_jinja_templates_path

def get_jinja_templates(template_name: str, data: dict):
    if "request" not in data:
        raise ValueError(
            "The data dictionary must contain a 'request' key with fastapi.Request object"
        )

    templates = Jinja2Templates(directory=get_jinja_templates_path())
    return templates.TemplateResponse(
        template_name,
        data,
    )
