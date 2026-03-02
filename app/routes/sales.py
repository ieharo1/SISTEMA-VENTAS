from fastapi import APIRouter, Request, HTTPException, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from datetime import datetime
from app.repositories.repository import Repository
from app.services.auth_service import decode_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_current_user(token: Optional[str] = Cookie(None)) -> Optional[dict]:
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    return payload


def require_auth(request: Request, token: Optional[str] = Cookie(None)):
    user = get_current_user(token)
    if not user:
        raise HTTPException(status_code=302, detail="Not authenticated")
    return user


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, token: Optional[str] = Cookie(None)):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    metrics = await Repository.get_dashboard_metrics()
    ranking = await Repository.get_seller_ranking()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "metrics": metrics, "ranking": ranking, "user": user},
    )


@router.get("/sellers", response_class=HTMLResponse)
async def sellers_page(request: Request, token: Optional[str] = Cookie(None)):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    sellers = await Repository.get_sellers()
    return templates.TemplateResponse(
        "sellers.html", {"request": request, "sellers": sellers, "user": user}
    )


@router.post("/sellers/create", response_class=HTMLResponse)
async def create_seller(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    region: str = Form(None),
    token: Optional[str] = Cookie(None),
):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    from app.schemas.schemas import SellerCreate

    seller = SellerCreate(name=name, email=email, phone=phone, region=region)
    await Repository.create_seller(seller)
    return RedirectResponse(url="/sellers", status_code=303)


@router.post("/sellers/update/{seller_id}", response_class=HTMLResponse)
async def update_seller(
    request: Request,
    seller_id: str,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    region: str = Form(None),
    token: Optional[str] = Cookie(None),
):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    from app.schemas.schemas import SellerCreate

    seller = SellerCreate(name=name, email=email, phone=phone, region=region)
    await Repository.update_seller(seller_id, seller)
    return RedirectResponse(url="/sellers", status_code=303)


@router.post("/sellers/delete/{seller_id}", response_class=HTMLResponse)
async def delete_seller(
    request: Request, seller_id: str, token: Optional[str] = Cookie(None)
):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    await Repository.delete_seller(seller_id)
    return RedirectResponse(url="/sellers", status_code=303)


@router.get("/sales", response_class=HTMLResponse)
async def sales_page(request: Request, token: Optional[str] = Cookie(None)):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    sales = await Repository.get_sales()
    sellers = await Repository.get_sellers()

    for sale in sales:
        seller = await Repository.get_seller_by_id(sale["seller_id"])
        sale["seller_name"] = seller["name"] if seller else "Unknown"

    return templates.TemplateResponse(
        "sales.html",
        {"request": request, "sales": sales, "sellers": sellers, "user": user},
    )


@router.post("/sales/create", response_class=HTMLResponse)
async def create_sale(
    request: Request,
    seller_id: str = Form(...),
    amount: float = Form(...),
    description: str = Form(None),
    sale_date: str = Form(...),
    token: Optional[str] = Cookie(None),
):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    from app.schemas.schemas import SaleCreate

    sale = SaleCreate(
        seller_id=seller_id,
        amount=amount,
        description=description,
        sale_date=datetime.fromisoformat(sale_date),
    )
    await Repository.create_sale(sale)
    return RedirectResponse(url="/sales", status_code=303)


@router.get("/goals", response_class=HTMLResponse)
async def goals_page(request: Request, token: Optional[str] = Cookie(None)):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    goals = await Repository.get_goals_with_progress()
    sellers = await Repository.get_sellers()

    return templates.TemplateResponse(
        "goals.html",
        {"request": request, "goals": goals, "sellers": sellers, "user": user},
    )


@router.post("/goals/create", response_class=HTMLResponse)
async def create_goal(
    request: Request,
    seller_id: str = Form(...),
    month: int = Form(...),
    year: int = Form(...),
    target_amount: float = Form(...),
    token: Optional[str] = Cookie(None),
):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    from app.schemas.schemas import GoalCreate

    goal = GoalCreate(
        seller_id=seller_id, month=month, year=year, target_amount=target_amount
    )
    await Repository.create_goal(goal)
    return RedirectResponse(url="/goals", status_code=303)


@router.post("/goals/delete/{goal_id}", response_class=HTMLResponse)
async def delete_goal(
    request: Request, goal_id: str, token: Optional[str] = Cookie(None)
):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    await Repository.delete_goal(goal_id)
    return RedirectResponse(url="/goals", status_code=303)


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request, token: Optional[str] = Cookie(None)):
    user = get_current_user(token)
    if not user:
        return RedirectResponse(url="/login")

    sellers = await Repository.get_sellers()
    ranking = await Repository.get_seller_ranking()
    goals = await Repository.get_goals_with_progress()

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "sellers": sellers,
            "ranking": ranking,
            "goals": goals,
            "user": user,
        },
    )
