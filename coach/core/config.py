import os
import pathlib
from functools import lru_cache

import motor.motor_asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import AsyncClient
from pymongo import MongoClient

from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent
    DB_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DB_URL')).Coach_deploy
    ADMIN_ID = os.getenv('ADMIN_ID')

    LLM = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3, use_responses_api=True)
    OPENAI_CLIENT = AsyncClient(api_key=os.getenv('OPENAI_API_KEY'))
    MONGO_CLIENT = MongoClient(os.getenv('MONGO_DB_URL'))
    VS_ID = os.getenv('VS_ID')
    TAVILY_TOOL = TavilySearchResults(tavily_api_key=os.getenv('TAVILY_API_KEY'), max_results=3)

    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    Issuer = "http://localhost:8000"
    Audience = "http://localhost:3000"


class ProductionConfig(BaseConfig):
    Issuer = ""
    Audience = ""


@lru_cache()
def get_settings() -> DevelopmentConfig | ProductionConfig:
    """Определяет активную конфигурацию по переменной окружения и кеширует результат."""
    config_cls_dict = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
    }
    config_name = os.getenv('FASTAPI_CONFIG', default='development')
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()