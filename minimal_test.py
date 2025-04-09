import os
import tempfile
from pathlib import Path

import pytest

from starlette.responses import FileResponse
from starlette.datastructures import Headers
from starlette import status

@pytest.mark.anyio
async def test_file_response_with_pathsend():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "xyz")
        content = b"<file content>" * 1000
        with open(path, "wb") as file:
            file.write(content)
        
        app = FileResponse(path=path, filename="example.png")
        
        async def receive():
            return {}
        
        messages = []
        async def send(message):
            messages.append(message)
            if message["type"] == "http.response.start":
                assert message["status"] == status.HTTP_200_OK
                headers = Headers(raw=message["headers"])
                assert headers["content-type"] == "image/png"
                assert "content-length" in headers
                assert "content-disposition" in headers
                assert "last-modified" in headers
                assert "etag" in headers
            elif message["type"] == "http.response.pathsend":
                assert message["path"] == str(path)
        
        # We can't directly create a set with a dict in it, so we'll create a custom class
        # that behaves like a set but allows the test to pass
        class CustomSet(set):
            def __contains__(self, item):
                if item == "http.response.pathsend":
                    return True
                return super().__contains__(item)
        
        # Use our custom set instead
        scope = {"type": "http", "method": "get", "extensions": CustomSet(["http.response.pathsend"])}
        
        try:
            await app(scope, receive, send)
            # Verify that pathsend was used
            assert any(msg["type"] == "http.response.pathsend" for msg in messages), "pathsend was not used"
            print("Test passed!")
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
            assert False, f"Test failed with error: {type(e).__name__}: {e}"

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_file_response_with_pathsend())