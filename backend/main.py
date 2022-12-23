import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from fastapi.security import HTTPBearer

import os

from settings import origins

from controllers import ad_controller
from controllers import account_controller

load_dotenv()

token_auth_scheme = HTTPBearer()

app = FastAPI( 
  # openapi_url='/docs',
  title='Jewerly Auction Site', 
  version='0.5.2'
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(ad_controller.ad_router)
app.include_router(account_controller.account_router)

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.get("/", tags=['Root'])
async def root(
    token: str = Depends(token_auth_scheme)
) -> dict:
  """Test Endpoint"""
  return { "message": "Jewerly Auction Site" }

if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=os.environ.get('DOMAIN'),
    port=int(os.environ.get('PORT')),
    log_level="info",
    reload=True
  )