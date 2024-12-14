# app/main.py
import uvicorn
from fastapi import FastAPI
from auth import router as auth_router
from database_manager.connections.connect_to_postgres import Base, engine
from logging_service.log_config import logger
from settings.settings import settings
from sqlalchemy.schema import CreateTable
from database_manager.models.models import User

app = FastAPI()

# Include OAuth authentication route
app.include_router(auth_router)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    logger.info("Creating tables if they don't exist...")
    user_table_sql = str(CreateTable(User.__table__).compile(engine))
    logger.info(f"User table creation SQL: \n{user_table_sql}")

    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully!")

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Data Sync App. Please authenticate to proceed."}

def run_app(app_module: str, host: str, port: int, reload: bool):
    """Custom function to run FastAPI with Uvicorn."""
    uvicorn.run(app_module, host=host, port=port, reload=reload)

# Run the app with uvicorn when executing this file directly
if __name__ == "__main__":
    run_app(
        "main:app",  # This is the app module (app is the FastAPI instance)
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_RELOAD,
    )
