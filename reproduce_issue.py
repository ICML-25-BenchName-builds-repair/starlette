import os
import tempfile
from pathlib import Path

from starlette.responses import FileResponse

async def test_file_response_with_pathsend():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "xyz")
        content = b"<file content>" * 1000
        with open(path, "wb") as file:
            file.write(content)
        
        app = FileResponse(path=path, filename="example.png")
        
        async def receive():
            return {}
        
        async def send(message):
            print(f"Message type: {message['type']}")
            if message["type"] == "http.response.start":
                print(f"Status: {message['status']}")
            elif message["type"] == "http.response.pathsend":
                print(f"Path: {message['path']}")
        
        # This is the problematic line
        scope = {"type": "http", "method": "get", "extensions": {"http.response.pathsend", {}}}
        
        try:
            await app(scope, receive, send)
            print("Test passed!")
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_file_response_with_pathsend())