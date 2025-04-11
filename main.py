import os
import importlib

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(root_path='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routes_dir = 'app/routes'
for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'app.routes.{filename[:-3]}'
        module = importlib.import_module(module_name)

        if hasattr(module, 'router'):
            app.include_router(module.router)
