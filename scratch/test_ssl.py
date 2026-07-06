import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

url1 = "postgresql+asyncpg://user:pass@host:5432/db?ssl=disable"
url2 = "postgresql+asyncpg://user:pass@host:5432/db"

engine1 = create_async_engine(url1)
engine2 = create_async_engine(url2)

print("URL1 connect_args:", engine1.url.query)
print("URL2 connect_args:", engine2.url.query)
