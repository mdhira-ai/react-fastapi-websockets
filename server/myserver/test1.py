from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

# region cors settings
# origins = [
#     "http://127.0.0.1:5173/"
#     "http://localhost:5173/",
#     "http://localhost:8080",
# ]
# endregion


# region CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# endregion


@app.get('/')
def read():
    return {
        "messages": "hello buddy"
    }





#region eventsource
# @app.get("/run")
# async def script():
#     async def generate():
#         a = 0
#         for i in range(20):
#             a = i
#             # Using Server-Sent Events format
#             yield f"data: {a}\n\n"
#             await asyncio.sleep(1)
    
#     # Configure response headers for SSE
#     headers = {
#         "Cache-Control": "no-cache",
#         "Connection": "keep-alive",
#     }
    
#     return StreamingResponse(
#         generate(), 
#         media_type="text/event-stream",
#         headers=headers
#     )
#endregion