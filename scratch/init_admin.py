import httpx
import asyncio

async def main():
    url = "http://127.0.0.1:8000/api/v1/admin/auth/setup"
    payload = {"email": "admin@admin.com", "password": "password123"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print("Status:", response.status_code)
        print("Response:", response.json())

if __name__ == "__main__":
    asyncio.run(main())
