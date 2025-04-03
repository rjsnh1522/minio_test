import os
from datetime import timedelta
from uuid import uuid4

from dotenv import load_dotenv
from starlette.responses import JSONResponse
from urllib3 import ProxyManager

load_dotenv('.env')
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio, S3Error
from urllib.parse import urlparse, urlunparse

MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', False)
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', False)
MINIO_SERVER = os.getenv('MINIO_SERVER', False)


assert MINIO_ACCESS_KEY, 'Missing MINIO_ACCESS_KEY'
assert MINIO_SECRET_KEY, 'Missing MINIO_SECRET_KEY'
assert MINIO_SERVER, 'Missing MINIO_SERVER'

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


minio_client = Minio(
            f"minio:9000",
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,

        )

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/signed-url")
async def get_signed_url():
    try:
        print(f"server name --> {os.getenv('MINIO_SERVER')}:{os.getenv('MINIO_PORT')}")
        print(f"mino: {os.getenv('MINIO_ENDPOINT')}")
        print(f" MINIO_ACCESS_KEY -- > {MINIO_ACCESS_KEY}")
        print(f" MINIO_SECRET_KEY -- > {MINIO_SECRET_KEY}")

        # Override the endpoint for signed URLs

        object_name = str(uuid4())
        signed_url = minio_client.get_presigned_url(
            "PUT",
            "bucket",
            object_name,
            expires=timedelta(days=1),
            response_headers={
                "Content-Type": "application/octet-stream"
            }
        )

        # 👇 Replace just the netloc (host:port) — not the signature

        parsed = urlparse(signed_url)
        public_url = urlunparse(parsed._replace(netloc="localhost:9000"))
        print(f"public url {public_url}")
        return JSONResponse(status_code=200,
                            content={'signed_url': public_url, 'file_id': object_name}
                            )
    except Exception as e:
        print(f"Error {e}")


@app.post("/upload_status")
async def file_upload_status(request: Request):
    data = await request.json()
    object_id = data.get("object_id")

    if not object_id:
        return {"error": "Missing object_id"}

    try:
        stat = minio_client.stat_object("bucket", object_id)
        data = {
            "file_name": stat.object_name,
            "size": stat.size,
            "content_type": stat.content_type
        }
        return JSONResponse(status_code=200, content={'data': data})
    except S3Error as e:
        return JSONResponse(status_code=500, content={'error': "something went wrong"})




