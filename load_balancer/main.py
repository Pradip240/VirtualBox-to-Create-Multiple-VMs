from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
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


@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"])
async def proxy(path: str, request: Request):
    for prefix, target in ROUTES.items():
        if path.startswith(prefix):
            url = f"{target}/{path}"

            headers = {
                k: v for k, v in request.headers.items()
                if k.lower() not in HOP_BY_HOP_HEADERS
            }

            client = httpx.AsyncClient(timeout=None)

            upstream = await client.stream(
                request.method,
                url,
                params=request.query_params,
                content=await request.body(),
                headers=headers,
            )

            response_headers = {
                k: v for k, v in upstream.headers.items()
                if k.lower() not in HOP_BY_HOP_HEADERS
            }

            return StreamingResponse(
                upstream.aiter_bytes(),   # <-- direct stream pipe
                status_code=upstream.status_code,
                headers=response_headers,
                media_type=upstream.headers.get("content-type"),
                background=None,  # client stays open until stream ends
            )

    return {"error": "No route matched"}