import os
from starlette.middleware.sessions import SessionMiddleware

def add_middlewares(app):
    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv("SESSION_SECRET")
    )