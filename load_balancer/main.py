from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
import httpx

app = FastAPI()

ROUTES = {
    "/grey": "http://192.168.1.9:5000",
    "/blur": "http://192.168.1.8:5000",
}

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}

client = httpx.AsyncClient(timeout=None)


@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"])
async def proxy(path: str, request: Request):
    full_path = request.url.path 
    for prefix, target in ROUTES.items():
        if full_path.startswith(prefix):
            url = f"{target}{full_path}"

            headers = {
                k: v for k, v in request.headers.items()
                if k.lower() not in HOP_BY_HOP_HEADERS
            }

            # Stream request body instead of buffering it all
            body = request.stream()

            upstream = await client.stream(
                request.method,
                url,
                params=request.query_params,
                content=body,
                headers=headers,
            )

            response_headers = {
                k: v for k, v in upstream.headers.items()
                if k.lower() not in HOP_BY_HOP_HEADERS
            }

            return StreamingResponse(
                upstream.aiter_bytes(),
                status_code=upstream.status_code,
                headers=response_headers,
                media_type=upstream.headers.get("content-type"),
                background=BackgroundTask(upstream.aclose),
            )

    return {"error": "No route matched"}
