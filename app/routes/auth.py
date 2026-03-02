from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from app.schemas.schemas import LoginRequest, Token, UserCreate
from app.services.auth_service import create_access_token
from app.repositories.repository import Repository
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, login_data: LoginRequest):
    user = await Repository.authenticate_user(login_data.username, login_data.password)
    if not user:
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid username or password"}
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "id": user["id"]},
        expires_delta=access_token_expires,
    )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "register": True}
    )


@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, user_data: UserCreate):
    existing_user = await Repository.get_user_by_username(user_data.username)
    if existing_user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "register": True, "error": "Username already exists"},
        )

    existing_email = await Repository.get_user_by_email(user_data.email)
    if existing_email:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "register": True, "error": "Email already exists"},
        )

    await Repository.create_user(user_data)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response
