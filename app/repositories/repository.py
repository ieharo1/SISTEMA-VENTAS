from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from app.database import get_database
from app.services.auth_service import get_password_hash, verify_password
from app.schemas.schemas import UserCreate, SellerCreate, SaleCreate, GoalCreate


def serialize_doc(doc: dict) -> dict:
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


class Repository:
    @staticmethod
    async def create_user(user: UserCreate) -> dict:
        db = get_database()
        hashed_password = get_password_hash(user.password)
        user_doc = {
            "email": user.email,
            "username": user.username,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return serialize_doc(user_doc)

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"username": username})
        return serialize_doc(user) if user else None

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"email": email})
        return serialize_doc(user) if user else None

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[dict]:
        db = get_database()
        user = await db.users.find_one({"username": username})
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return serialize_doc(user)

    @staticmethod
    async def create_seller(seller: SellerCreate) -> dict:
        db = get_database()
        seller_doc = {
            "name": seller.name,
            "email": seller.email,
            "phone": seller.phone,
            "region": seller.region,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await db.sellers.insert_one(seller_doc)
        seller_doc["_id"] = result.inserted_id
        return serialize_doc(seller_doc)

    @staticmethod
    async def get_sellers() -> List[dict]:
        db = get_database()
        sellers = await db.sellers.find().to_list(length=1000)
        return [serialize_doc(s) for s in sellers]

    @staticmethod
    async def get_seller_by_id(seller_id: str) -> Optional[dict]:
        db = get_database()
        seller = await db.sellers.find_one({"_id": ObjectId(seller_id)})
        return serialize_doc(seller) if seller else None

    @staticmethod
    async def update_seller(seller_id: str, seller: SellerCreate) -> Optional[dict]:
        db = get_database()
        result = await db.sellers.find_one_and_update(
            {"_id": ObjectId(seller_id)},
            {
                "$set": {
                    "name": seller.name,
                    "email": seller.email,
                    "phone": seller.phone,
                    "region": seller.region,
                    "updated_at": datetime.utcnow(),
                }
            },
            return_document=True,
        )
        return serialize_doc(result) if result else None

    @staticmethod
    async def delete_seller(seller_id: str) -> bool:
        db = get_database()
        result = await db.sellers.delete_one({"_id": ObjectId(seller_id)})
        return result.deleted_count > 0

    @staticmethod
    async def create_sale(sale: SaleCreate) -> dict:
        db = get_database()
        sale_doc = {
            "seller_id": sale.seller_id,
            "amount": sale.amount,
            "description": sale.description,
            "sale_date": sale.sale_date,
            "created_at": datetime.utcnow(),
        }
        result = await db.sales.insert_one(sale_doc)
        sale_doc["_id"] = result.inserted_id
        return serialize_doc(sale_doc)

    @staticmethod
    async def get_sales(seller_id: Optional[str] = None) -> List[dict]:
        db = get_database()
        query = {"seller_id": seller_id} if seller_id else {}
        sales = await db.sales.find(query).sort("sale_date", -1).to_list(length=1000)
        return [serialize_doc(s) for s in sales]

    @staticmethod
    async def get_sales_by_month(
        year: int, month: int, seller_id: Optional[str] = None
    ) -> List[dict]:
        db = get_database()
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        query = {"sale_date": {"$gte": start_date, "$lt": end_date}}
        if seller_id:
            query["seller_id"] = seller_id

        sales = await db.sales.find(query).sort("sale_date", -1).to_list(length=1000)
        return [serialize_doc(s) for s in sales]

    @staticmethod
    async def get_total_sales(seller_id: Optional[str] = None) -> float:
        db = get_database()
        query = {"seller_id": seller_id} if seller_id else {}
        pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}},
        ]
        result = await db.sales.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0.0

    @staticmethod
    async def create_goal(goal: GoalCreate) -> dict:
        db = get_database()
        existing_goal = await db.goals.find_one(
            {"seller_id": goal.seller_id, "month": goal.month, "year": goal.year}
        )
        if existing_goal:
            return None

        goal_doc = {
            "seller_id": goal.seller_id,
            "month": goal.month,
            "year": goal.year,
            "target_amount": goal.target_amount,
            "created_at": datetime.utcnow(),
        }
        result = await db.goals.insert_one(goal_doc)
        goal_doc["_id"] = result.inserted_id
        return serialize_doc(goal_doc)

    @staticmethod
    async def get_goals(seller_id: Optional[str] = None) -> List[dict]:
        db = get_database()
        query = {"seller_id": seller_id} if seller_id else {}
        goals = await db.goals.find(query).to_list(length=1000)
        return [serialize_doc(g) for g in goals]

    @staticmethod
    async def get_goal_by_id(goal_id: str) -> Optional[dict]:
        db = get_database()
        goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
        return serialize_doc(goal) if goal else None

    @staticmethod
    async def update_goal(goal_id: str, goal: GoalCreate) -> Optional[dict]:
        db = get_database()
        result = await db.goals.find_one_and_update(
            {"_id": ObjectId(goal_id)},
            {
                "$set": {
                    "seller_id": goal.seller_id,
                    "month": goal.month,
                    "year": goal.year,
                    "target_amount": goal.target_amount,
                }
            },
            return_document=True,
        )
        return serialize_doc(result) if result else None

    @staticmethod
    async def delete_goal(goal_id: str) -> bool:
        db = get_database()
        result = await db.goals.delete_one({"_id": ObjectId(goal_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_goals_with_progress() -> List[dict]:
        db = get_database()
        goals = await db.goals.find().to_list(length=1000)
        result = []
        for goal in goals:
            sales = await Repository.get_sales_by_month(
                goal["year"], goal["month"], goal["seller_id"]
            )
            achieved = sum(s["amount"] for s in sales)
            percentage = (
                (achieved / goal["target_amount"] * 100)
                if goal["target_amount"] > 0
                else 0
            )
            goal_data = serialize_doc(goal)
            goal_data["achieved_amount"] = achieved
            goal_data["percentage"] = round(percentage, 2)
            seller = await Repository.get_seller_by_id(goal["seller_id"])
            goal_data["seller_name"] = seller["name"] if seller else "Unknown"
            result.append(goal_data)
        return result

    @staticmethod
    async def get_dashboard_metrics() -> dict:
        total_sales = await Repository.get_total_sales()
        db = get_database()
        total_sellers = await db.sellers.count_documents({})
        total_goals = await db.goals.count_documents({})

        goals_with_progress = await Repository.get_goals_with_progress()
        goals_achieved = sum(1 for g in goals_with_progress if g["percentage"] >= 100)

        all_sales = await db.sales.find().to_list(length=1000)
        average_sale = total_sales / len(all_sales) if all_sales else 0.0

        pipeline = [{"$group": {"_id": "$seller_id", "total": {"$sum": "$amount"}}}]
        seller_totals = await db.sales.aggregate(pipeline).to_list(length=1000)

        top_sellers = []
        for st in sorted(seller_totals, key=lambda x: x["total"], reverse=True)[:5]:
            seller = await Repository.get_seller_by_id(st["_id"])
            if seller:
                top_sellers.append({"name": seller["name"], "total": st["total"]})

        return {
            "total_sales": total_sales,
            "total_sellers": total_sellers,
            "total_goals": total_goals,
            "goals_achieved": goals_achieved,
            "average_sale": round(average_sale, 2),
            "top_sellers": top_sellers,
        }

    @staticmethod
    async def get_seller_ranking() -> List[dict]:
        db = get_database()
        pipeline = [
            {
                "$group": {
                    "_id": "$seller_id",
                    "total": {"$sum": "$amount"},
                    "count": {"$sum": 1},
                }
            }
        ]
        seller_totals = await db.sales.aggregate(pipeline).to_list(length=1000)

        ranking = []
        for st in sorted(seller_totals, key=lambda x: x["total"], reverse=True):
            seller = await Repository.get_seller_by_id(st["_id"])
            if seller:
                ranking.append(
                    {
                        "rank": len(ranking) + 1,
                        "seller_id": st["id"],
                        "name": seller["name"],
                        "total_sales": st["total"],
                        "sale_count": st["count"],
                    }
                )
        return ranking
