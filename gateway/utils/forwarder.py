import httpx
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config import SERVICES


async def forward_request(service: str, path: str, method: str, **kwargs):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found.")

    url = f"{SERVICES[service]}{path}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, timeout=5.0, **kwargs)
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503, detail=f"{service} service is offline."
            )
