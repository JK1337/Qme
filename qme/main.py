from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qme import __version__
from qme.services.cv_rewrite import rewrite_cv_for_job
from qme.services import points as points_service
from qme.settings import settings

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title=settings.app_name,
    description="Dream-job platform: learn-to-earn, AI CV alignment, styled reQme sharing.",
    version=__version__,
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse, name="home")
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request, "title": settings.app_name},
    )


@app.get("/learn", response_class=HTMLResponse)
def learn(request: Request) -> HTMLResponse:
    catalog = points_service.get_catalog()
    progress = points_service.get_progress()
    total = progress.total_points(catalog)
    return templates.TemplateResponse(
        request,
        "learn.html",
        {
            "request": request,
            "title": "Learn to earn",
            "modules": catalog,
            "progress": progress,
            "total_points": total,
        },
    )


@app.post("/learn/complete/{module_id}")
def complete_module(module_id: str) -> JSONResponse:
    progress = points_service.complete_module(module_id)
    catalog = points_service.get_catalog()
    return JSONResponse(
        {
            "completed": sorted(progress.completed_module_ids),
            "total_points": progress.total_points(catalog),
        }
    )


@app.get("/cv", response_class=HTMLResponse)
def cv_tools(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "cv.html",
        {"request": request, "title": "CV & AI"},
    )


@app.post("/api/cv/rewrite-job")
def api_cv_rewrite_job(cv_text: str = Form(...), job_description: str = Form(...)) -> JSONResponse:
    result = rewrite_cv_for_job(cv_text=cv_text, job_description=job_description)
    return JSONResponse(
        {
            "tailored_cv": result.tailored_cv,
            "notes": result.notes,
            "demo": result.demo,
        }
    )


@app.get("/reqme", response_class=HTMLResponse)
def reqme(request: Request) -> HTMLResponse:
    token = points_service.new_share_token()
    base = str(request.base_url).rstrip("/")
    share_url = f"{base}/r/{token}"
    return templates.TemplateResponse(
        request,
        "reqme.html",
        {
            "request": request,
            "title": "Your reQme",
            "share_token": token,
            "share_url": share_url,
        },
    )


@app.get("/r/{token}", response_class=HTMLResponse)
def public_reqme(request: Request, token: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "reqme_public.html",
        {"request": request, "title": "reQme", "token": token},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.env}
