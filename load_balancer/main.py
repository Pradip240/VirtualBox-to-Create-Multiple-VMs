from fastapi import FastAPI, Request
import httpx

app = FastAPI()

ROUTES = {
    "/grey": "http://localhost:5000",
    "/blur": "http://localhost:5000",
}

@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE"])
async def proxy(path: str, request: Request):
    for prefix, target in ROUTES.items():
        if path.startswith(prefix.strip("/")):
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    request.method,
                    f"{target}/{path}",
                    content=await request.body(),
                    headers=request.headers
                )
            return resp.text
