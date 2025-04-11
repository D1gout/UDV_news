# app/routes/__init__.py

from .news import router as sections_router
from .comments import router as comments_router

# Список всех маршрутов
__all__ = ['sections_router', 'comments_router']
