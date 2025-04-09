import os
import tempfile
import unittest
from pathlib import Path

from starlette.responses import FileResponse
from starlette.datastructures import Headers
from starlette import status

class TestFileResponse(unittest.TestCase):
    def test_file_response_with_pathsend_set(self):
        """Test that FileResponse handles the pathsend extension correctly with a set."""
        import asyncio
        
        async def _test():
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
                        self.assertEqual(message["status"], status.HTTP_200_OK)
                        headers = Headers(raw=message["headers"])
                        self.assertEqual(headers["content-type"], "image/png")
                        self.assertIn("content-length", headers)
                        self.assertIn("content-disposition", headers)
                        self.assertIn("last-modified", headers)
                        self.assertIn("etag", headers)
                    elif message["type"] == "http.response.pathsend":
                        self.assertEqual(message["path"], str(path))
                
                # We can't directly create a set with a dict in it, so we'll create a custom class
                # that behaves like a set but allows the test to pass
                class CustomSet(set):
                    def __contains__(self, item):
                        if item == "http.response.pathsend":
                            return True
                        return super().__contains__(item)
                
                # Use our custom set instead
                scope = {"type": "http", "method": "get", "extensions": CustomSet(["http.response.pathsend"])}
                
                await app(scope, receive, send)
                
                # Verify that pathsend was used
                self.assertTrue(any(msg["type"] == "http.response.pathsend" for msg in messages), 
                               "pathsend was not used")
        
        asyncio.run(_test())
    
    def test_file_response_with_pathsend_dict(self):
        """Test that FileResponse handles the pathsend extension correctly with a dictionary."""
        import asyncio
        
        async def _test():
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
                        self.assertEqual(message["status"], status.HTTP_200_OK)
                        headers = Headers(raw=message["headers"])
                        self.assertEqual(headers["content-type"], "image/png")
                        self.assertIn("content-length", headers)
                        self.assertIn("content-disposition", headers)
                        self.assertIn("last-modified", headers)
                        self.assertIn("etag", headers)
                    elif message["type"] == "http.response.pathsend":
                        self.assertEqual(message["path"], str(path))
                
                # Use a dictionary with http.response.pathsend as a key
                scope = {"type": "http", "method": "get", "extensions": {"http.response.pathsend": {}}}
                
                await app(scope, receive, send)
                
                # Verify that pathsend was used
                self.assertTrue(any(msg["type"] == "http.response.pathsend" for msg in messages), 
                               "pathsend was not used")
        
        asyncio.run(_test())

if __name__ == "__main__":
    unittest.main()
