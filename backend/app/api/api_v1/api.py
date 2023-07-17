from fastapi import APIRouter

from app.api.api_v1.endpoints import admins, bots, statistics, tasks, users, payok

api_router = APIRouter()
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(payok.router, prefix="/payok", tags=["payok"])
api_router.include_router(admins.router, prefix="/admins", tags=["admins"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
