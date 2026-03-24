from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from qme import __version__
from qme.services import accounts
from qme.services import credits as credits_service
from qme.services import jobs as jobs_service
from qme.services import resume_file_import as resume_import
from qme.services.cv_rewrite import rewrite_cv_for_job
from qme.settings import settings

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _safe_redirect_path(path: str, default: str = "/account") -> str:
    return path if path.startswith("/") and not path.startswith("//") else default

app = FastAPI(
    title=settings.app_name,
    description="Find your dream job — play-to-learn credits, AI CV alignment, reQme sharing.",
    version=__version__,
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="lax",
    https_only=False,
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def tpl(request: Request, template_name: str, **context: Any) -> HTMLResponse:
    ctx = dict(context)
    ctx["request"] = request
    u = accounts.user_from_request(request)
    ctx["current_user"] = u
    uid = u.id if u else None
    ctx["credit_balance"] = credits_service.balance_for_session(request.session, uid)
    ctx["rewrite_cost"] = credits_service.REWRITE_COST
    ctx["job_shortlist"] = list(request.session.get("job_shortlist", []))
    return templates.TemplateResponse(request, template_name, ctx)


@app.get("/", response_class=HTMLResponse, name="home")
def home(request: Request) -> HTMLResponse:
    return tpl(request, "index.html", title=settings.app_name)


@app.get("/dream-job", response_class=HTMLResponse)
def dream_job(request: Request) -> HTMLResponse:
    return tpl(request, "dream_job.html", title="Find your dream job")


@app.get("/jobs", response_class=HTMLResponse)
def jobs_list(
    request: Request,
    q: str = "",
    location: str = "",
    work_type: str = "",
) -> HTMLResponse:
    rows = jobs_service.list_jobs(q=q, location=location, work_type=work_type)
    return tpl(
        request,
        "jobs.html",
        title="Browse roles",
        jobs=rows,
        q=q,
        location=location,
        work_type=work_type,
    )


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, job_id: str) -> HTMLResponse:
    job = jobs_service.get_job(job_id)
    if not job:
        return tpl(request, "job_not_found.html", title="Role not found")
    return tpl(request, "job_detail.html", title=job.title, job=job)


@app.post("/jobs/shortlist/toggle/{job_id}", response_model=None)
def shortlist_toggle(request: Request, job_id: str) -> RedirectResponse:
    if jobs_service.get_job(job_id) is None:
        return RedirectResponse(url="/jobs", status_code=303)
    sl = list(request.session.get("job_shortlist", []))
    if job_id in sl:
        sl.remove(job_id)
    else:
        sl.append(job_id)
    request.session["job_shortlist"] = sl
    ref = request.headers.get("referer") or "/jobs"
    return RedirectResponse(url=ref, status_code=303)


@app.get("/learn", response_class=HTMLResponse)
def learn(request: Request) -> HTMLResponse:
    catalog = credits_service.get_catalog()
    uid = accounts.session_user_id(request)
    progress = credits_service.get_progress(request.session, uid)
    earned = progress.total_credits(catalog)
    available = credits_service.balance_for_session(request.session, uid)
    return tpl(
        request,
        "learn.html",
        title="Play to learn",
        modules=catalog,
        progress=progress,
        credits_earned=earned,
        credits_available=available,
    )


@app.post("/learn/complete/{module_id}")
def complete_module(request: Request, module_id: str) -> JSONResponse:
    uid = accounts.session_user_id(request)
    progress = credits_service.complete_module(request.session, uid, module_id)
    catalog = credits_service.get_catalog()
    return JSONResponse(
        {
            "completed": sorted(progress.completed_module_ids),
            "credits_earned": progress.total_credits(catalog),
            "credits_available": credits_service.balance_for_session(request.session, uid),
        }
    )


@app.get("/cv", response_class=HTMLResponse)
def cv_tools(request: Request, job: str | None = None) -> HTMLResponse:
    user = accounts.user_from_request(request)
    job_obj = jobs_service.get_job(job) if job else None
    jd_prefill = ""
    if job_obj:
        jd_prefill = f"{job_obj.title} — {job_obj.company} ({job_obj.location})\n\n{job_obj.description}"
    base = str(request.base_url).rstrip("/")
    share_url = f"{base}/r/{user.reqme_token}" if user else None
    register_href = f"/account/register?{urlencode({'next': '/cv'})}"
    return tpl(
        request,
        "cv.html",
        title="My Resume",
        profile_user=user,
        job_pick=job_obj,
        job_description_prefill=jd_prefill,
        share_url=share_url,
        register_href=register_href,
    )


@app.post("/api/cv/rewrite-job")
def api_cv_rewrite_job(
    request: Request,
    job_description: str = Form(...),
    cv_override: str = Form(""),
) -> JSONResponse:
    user = accounts.user_from_request(request)
    override = cv_override.strip()
    document = override if override else (user.main_cv if user else "")
    life_story = user.life_story if user else ""

    if not document:
        return JSONResponse(
            {
                "error": "Add a main CV in your account or paste a CV for this role.",
                "tailored_cv": "",
                "notes": "",
                "demo": True,
            },
            status_code=400,
        )

    uid = user.id if user else None
    if user and not credits_service.try_spend(request.session, uid, credits_service.REWRITE_COST):
        return JSONResponse(
            {
                "error": (
                    f"Not enough credits (need {credits_service.REWRITE_COST}). "
                    "Complete modules under Play to learn to earn more."
                ),
                "tailored_cv": "",
                "notes": "",
                "demo": True,
            },
            status_code=402,
        )

    result = rewrite_cv_for_job(
        job_description=job_description,
        document_cv=document,
        life_story=life_story,
    )
    remaining = credits_service.balance_for_session(request.session, uid)
    return JSONResponse(
        {
            "tailored_cv": result.tailored_cv,
            "notes": result.notes,
            "demo": result.demo,
            "credits_remaining": remaining,
            "credits_charged": credits_service.REWRITE_COST if user else 0,
        }
    )


@app.post("/api/cv/import-resume-file")
async def api_cv_import_resume_file(file: UploadFile = File(...)) -> JSONResponse:
    """Accept PDF/DOCX from LinkedIn (e.g. Save to PDF) and return plain text for the resume editor."""
    raw = await file.read(resume_import.MAX_RESUME_FILE_BYTES + 1)
    if len(raw) > resume_import.MAX_RESUME_FILE_BYTES:
        return JSONResponse(
            {
                "error": f"File too large (max {resume_import.MAX_RESUME_FILE_BYTES // (1024 * 1024)} MB).",
                "text": "",
            },
            status_code=413,
        )
    try:
        text = resume_import.extract_resume_text(data=raw, filename=file.filename)
    except ValueError as exc:
        return JSONResponse({"error": str(exc), "text": ""}, status_code=400)
    if not text.strip():
        return JSONResponse(
            {
                "error": "No text could be extracted. Scanned/image-only PDFs are not supported.",
                "text": "",
            },
            status_code=422,
        )
    return JSONResponse({"text": text, "error": ""})


@app.get("/account/register", response_class=HTMLResponse)
def register_form(request: Request, error: str | None = None, next: str | None = None) -> HTMLResponse:
    next_path = next or "/account"
    login_href = f"/account/login?{urlencode({'next': next_path})}"
    return tpl(
        request,
        "register.html",
        title="Create account",
        error=error,
        next_path=next_path,
        login_href=login_href,
    )


@app.post("/account/register", response_model=None)
def register_submit(
    request: Request,
    email: str = Form(...),
    display_name: str = Form(""),
    password: str = Form(...),
    main_cv: str = Form(""),
    life_story: str = Form(""),
    next: str = Form("/account"),
) -> RedirectResponse | HTMLResponse:
    err, user = accounts.register_user(
        email=email,
        display_name=display_name,
        password=password,
        main_cv=main_cv,
        life_story=life_story,
    )
    if err:
        next_path = _safe_redirect_path(next)
        login_href = f"/account/login?{urlencode({'next': next_path})}"
        return tpl(
            request,
            "register.html",
            title="Create account",
            error=err,
            next_path=next_path,
            login_href=login_href,
        )
    assert user is not None
    credits_service.migrate_guest_to_user(request.session, user.id)
    accounts.set_session_user(request, user.id)
    return RedirectResponse(url=_safe_redirect_path(next), status_code=303)


@app.get("/account/login", response_class=HTMLResponse)
def login_form(request: Request, error: str | None = None, next: str | None = None) -> HTMLResponse:
    next_path = next or "/account"
    register_href = f"/account/register?{urlencode({'next': next_path})}"
    return tpl(
        request,
        "login.html",
        title="Sign in",
        error=error,
        next_path=next_path,
        register_href=register_href,
    )


@app.post("/account/login", response_model=None)
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    next: str = Form("/account"),
) -> RedirectResponse | HTMLResponse:
    user = accounts.verify_login(email, password)
    if not user:
        next_path = _safe_redirect_path(next)
        register_href = f"/account/register?{urlencode({'next': next_path})}"
        return tpl(
            request,
            "login.html",
            title="Sign in",
            error="Email or password is incorrect.",
            next_path=next_path,
            register_href=register_href,
        )
    accounts.set_session_user(request, user.id)
    return RedirectResponse(url=_safe_redirect_path(next), status_code=303)


@app.post("/account/logout", response_model=None)
def logout(request: Request) -> RedirectResponse:
    accounts.clear_session_user(request)
    return RedirectResponse(url="/", status_code=303)


@app.get("/account", response_class=HTMLResponse, response_model=None)
def account_page(request: Request) -> RedirectResponse | HTMLResponse:
    user = accounts.user_from_request(request)
    if not user:
        return RedirectResponse(url="/account/login?next=/account", status_code=303)
    catalog = credits_service.get_catalog()
    prog = credits_service.progress_for_logged_user_id(user.id)
    certs = credits_service.certificates_for_progress(prog, catalog)
    return tpl(
        request,
        "account.html",
        title="Your account",
        user=user,
        certificates=certs,
        credits_earned=prog.total_credits(catalog),
        credits_available=credits_service.balance_for_key(f"u:{user.id}", catalog),
    )


@app.post("/account", response_model=None)
def account_update(
    request: Request,
    display_name: str = Form(...),
    main_cv: str = Form(""),
    life_story: str = Form(""),
) -> RedirectResponse | HTMLResponse:
    uid = accounts.session_user_id(request)
    if not uid:
        return RedirectResponse(url="/account/login?next=/account", status_code=303)
    accounts.update_profile(uid, display_name=display_name, main_cv=main_cv, life_story=life_story)
    user = accounts.get_user(uid)
    assert user is not None
    catalog = credits_service.get_catalog()
    prog = credits_service.progress_for_logged_user_id(user.id)
    certs = credits_service.certificates_for_progress(prog, catalog)
    return tpl(
        request,
        "account.html",
        title="Your account",
        user=user,
        saved=True,
        certificates=certs,
        credits_earned=prog.total_credits(catalog),
        credits_available=credits_service.balance_for_key(f"u:{user.id}", catalog),
    )


@app.get("/reqme", response_class=HTMLResponse, response_model=None)
def reqme(request: Request) -> RedirectResponse | HTMLResponse:
    user = accounts.user_from_request(request)
    if not user:
        return RedirectResponse(url="/account/login?next=/reqme", status_code=303)
    base = str(request.base_url).rstrip("/")
    share_url = f"{base}/r/{user.reqme_token}"
    catalog = credits_service.get_catalog()
    prog = credits_service.progress_for_logged_user_id(user.id)
    certs = credits_service.certificates_for_progress(prog, catalog)
    excerpt = (user.main_cv.strip()[:400] + "…") if len(user.main_cv.strip()) > 400 else user.main_cv.strip()
    return tpl(
        request,
        "reqme.html",
        title="My Resume · reQme",
        share_url=share_url,
        certificates=certs,
        cv_excerpt=excerpt,
    )


@app.post("/reqme/rotate-token", response_model=None)
def reqme_rotate(request: Request) -> RedirectResponse:
    user = accounts.user_from_request(request)
    if not user:
        return RedirectResponse(url="/account/login?next=/reqme", status_code=303)
    accounts.rotate_reqme_token(user.id)
    return RedirectResponse(url="/reqme", status_code=303)


@app.get("/r/{token}", response_class=HTMLResponse)
def public_reqme(request: Request, token: str) -> HTMLResponse:
    user = accounts.get_user_by_reqme_token(token)
    if not user:
        return tpl(request, "reqme_public.html", title="reQme", not_found=True)
    catalog = credits_service.get_catalog()
    prog = credits_service.progress_for_logged_user_id(user.id)
    certs = credits_service.certificates_for_progress(prog, catalog)
    excerpt = (user.main_cv.strip()[:500] + "…") if len(user.main_cv.strip()) > 500 else user.main_cv.strip()
    story_excerpt = (
        (user.life_story.strip()[:320] + "…") if len(user.life_story.strip()) > 320 else user.life_story.strip()
    )
    return tpl(
        request,
        "reqme_public.html",
        title=f"{user.display_name} — reQme",
        public_user=user,
        certificates=certs,
        cv_excerpt=excerpt,
        story_excerpt=story_excerpt,
        not_found=False,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.env}
