from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Mount, Route, Router

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

# Manually test the Mount.matches method
from starlette.routing import Match

# Create a scope for /users/
scope = {
    "type": "http",
    "path": "/users/",
    "method": "GET",
}

# Get the Mount instance
mount = app.routes[0]
print(f"Mount path: {mount.path}")

# Test the matches method
match, child_scope = mount.matches(scope)
print(f"Match result: {match}")
print(f"Child scope: {child_scope}")

# Create a scope for /users/tomchristie
scope = {
    "type": "http",
    "path": "/users/tomchristie",
    "method": "GET",
}

# Test the matches method again
match, child_scope = mount.matches(scope)
print(f"Match result: {match}")
print(f"Child scope: {child_scope}")