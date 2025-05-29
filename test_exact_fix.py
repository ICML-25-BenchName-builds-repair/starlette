#!/usr/bin/env python3
"""
Test that exactly mimics the failing test from the issue description
"""

import os
import tempfile
import asyncio
from starlette.responses import FileResponse
from starlette import status
from starlette.datastructures import Headers
from starlette.types import Message


async def test_file_response_with_pathsend():
    """Exact copy of the test from tests/test_responses.py but with the fix applied"""
    
    # Create a temporary directory and file (mimicking tmpdir from pytest)
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "xyz")
    content = b"<file content>" * 1000
    with open(path, "wb") as file:
        file.write(content)

    try:
        app = FileResponse(path=path, filename="example.png")

        async def receive() -> Message:  # type: ignore[empty-body]
            ...  # pragma: no cover

        async def send(message: Message) -> None:
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

        # Since the TestClient doesn't support `pathsend`, we need to test this directly.
        # FIXED: Changed from {"http.response.pathsend", {}} to {"http.response.pathsend": {}}
        await app(
            {"type": "http", "method": "get", "extensions": {"http.response.pathsend": {}}},
            receive,
            send,
        )
        
        print("✓ test_file_response_with_pathsend passed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ test_file_response_with_pathsend failed: {e}")
        return False
    finally:
        # Clean up
        os.unlink(path)
        os.rmdir(tmpdir)


async def main():
    print("Testing the exact fix for the failing CI test...")
    success = await test_file_response_with_pathsend()
    
    if success:
        print("\n✓ SUCCESS: The CI test should now pass!")
    else:
        print("\n✗ FAILURE: The fix did not work")


if __name__ == "__main__":
    asyncio.run(main())