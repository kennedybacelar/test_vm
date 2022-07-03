from fastapi import FastAPI
from api.routers import users, products, vendor_machine

app = FastAPI()
app.include_router(users.router)
app.include_router(products.router)
app.include_router(vendor_machine.router)
