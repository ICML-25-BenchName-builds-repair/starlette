from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, Router
from starlette.testclient import TestClient

# Define a simple endpoint for the mounted app
def all_users_page(request):
    return PlainTextResponse("Hello, everyone!")

def user_page(request):
    username = request.path_params["username"]
    return PlainTextResponse(f"Hello, {username}!")

# Create a router with routes
users = Router(
    routes=[
        Route("/", endpoint=all_users_page),
        Route("/{username}", endpoint=user_page),
    ]
)

# Create the main app with a mounted router
app = Starlette(
    routes=[
        Mount("/users", app=users),
    ]
)

# Test the app
client = TestClient(app)

# Test the mounted routes
response = client.get("/users/")
print(f"Response status for /users/: {response.status_code}")
print(f"Response text for /users/: {response.text}")

response = client.get("/users/tomchristie")
print(f"Response status for /users/tomchristie: {response.status_code}")
print(f"Response text for /users/tomchristie: {response.text}")