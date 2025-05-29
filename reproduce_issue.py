#!/usr/bin/env python3
"""
Script to reproduce the TypeError: unhashable type: 'dict' issue
"""

import os
import tempfile
import asyncio
from starlette.responses import FileResponse
from starlette import status
from starlette.datastructures import Headers
from starlette.types import Message


async def test_file_response_with_pathsend_broken():
    """Test that reproduces the original issue"""
    print("Testing broken version...")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = b"<file content>" * 1000
        tmp.write(content)
        path = tmp.name
    
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

        # This should fail with TypeError: unhashable type: 'dict'
        await app(
            {"type": "http", "method": "get", "extensions": {"http.response.pathsend", {}}},
            receive,
            send,
        )
        print("ERROR: Expected TypeError but test passed!")
        
    except TypeError as e:
        if "unhashable type: 'dict'" in str(e):
            print(f"✓ Successfully reproduced the issue: {e}")
        else:
            print(f"✗ Got unexpected TypeError: {e}")
    except Exception as e:
        print(f"✗ Got unexpected exception: {e}")
    finally:
        # Clean up
        os.unlink(path)


async def test_file_response_with_pathsend_fixed():
    """Test with the correct syntax"""
    print("\nTesting fixed version...")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = b"<file content>" * 1000
        tmp.write(content)
        path = tmp.name
    
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
                print("✓ pathsend message received correctly")

        # This should work with the correct syntax
        await app(
            {"type": "http", "method": "get", "extensions": {"http.response.pathsend": {}}},
            receive,
            send,
        )
        print("✓ Fixed version works correctly!")
        
    except Exception as e:
        print(f"✗ Fixed version failed: {e}")
    finally:
        # Clean up
        os.unlink(path)


async def main():
    await test_file_response_with_pathsend_broken()
    await test_file_response_with_pathsend_fixed()


if __name__ == "__main__":
    asyncio.run(main())