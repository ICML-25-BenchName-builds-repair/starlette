#!/usr/bin/env python3
"""
Verify that the fix for test_file_response_with_pathsend works correctly
"""

import os
import tempfile
import asyncio
from starlette.responses import FileResponse
from starlette import status
from starlette.datastructures import Headers
from starlette.types import Message


async def test_file_response_with_pathsend_fixed():
    """Test the fixed version of the pathsend test"""
    print("Testing the fixed pathsend test...")
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = b"<file content>" * 1000
        tmp.write(content)
        path = tmp.name
    
    try:
        app = FileResponse(path=path, filename="example.png")

        received_start = False
        received_pathsend = False

        async def receive() -> Message:  # type: ignore[empty-body]
            ...  # pragma: no cover

        async def send(message: Message) -> None:
            nonlocal received_start, received_pathsend
            
            if message["type"] == "http.response.start":
                received_start = True
                assert message["status"] == status.HTTP_200_OK
                headers = Headers(raw=message["headers"])
                assert headers["content-type"] == "image/png"
                assert "content-length" in headers
                assert "content-disposition" in headers
                assert "last-modified" in headers
                assert "etag" in headers
                print("✓ Received http.response.start message correctly")
                
            elif message["type"] == "http.response.pathsend":
                received_pathsend = True
                assert message["path"] == str(path)
                print("✓ Received http.response.pathsend message correctly")

        # This should work with the correct syntax (dictionary instead of set)
        await app(
            {"type": "http", "method": "get", "extensions": {"http.response.pathsend": {}}},
            receive,
            send,
        )
        
        # Verify both messages were received
        assert received_start, "Did not receive http.response.start message"
        assert received_pathsend, "Did not receive http.response.pathsend message"
        
        print("✓ All assertions passed - fix is working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
    finally:
        # Clean up
        os.unlink(path)


async def test_original_broken_syntax():
    """Test that the original broken syntax still fails"""
    print("\nTesting that the original broken syntax still fails...")
    
    try:
        # This should fail with TypeError: unhashable type: 'dict'
        scope = {"type": "http", "method": "get", "extensions": {"http.response.pathsend", {}}}
        print("✗ ERROR: Expected TypeError but the broken syntax didn't fail!")
        return False
        
    except TypeError as e:
        if "unhashable type: 'dict'" in str(e):
            print(f"✓ Original broken syntax correctly fails: {e}")
            return True
        else:
            print(f"✗ Got unexpected TypeError: {e}")
            return False
    except Exception as e:
        print(f"✗ Got unexpected exception: {e}")
        return False


async def main():
    print("=" * 60)
    print("VERIFYING FIX FOR test_file_response_with_pathsend")
    print("=" * 60)
    
    # Test that the original broken syntax still fails
    test1_passed = await test_original_broken_syntax()
    
    # Test that the fixed syntax works
    test2_passed = await test_file_response_with_pathsend_fixed()
    
    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("✓ ALL TESTS PASSED - Fix is working correctly!")
        print("The TypeError: unhashable type: 'dict' issue has been resolved.")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())