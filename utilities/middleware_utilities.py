from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from typing import Callable
from utilities.login_utilities import verify_token

class JWTMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Middleware that handles JWT authentication.
        """
         # Debugging step: log incoming request URL and headers
        print(f"Request URL: {request.url.path}")
        print(f"Request Headers: {request.headers}")
         # Debugging step: log the Authorization header
        auth_header = request.headers.get("Authorization")
        print(f"Authorization Header: {auth_header}")
        # Define protected routes that require JWT validation
        protected_routes = ["/login/protected", "/other_protected_route"]  # Add your protected routes here
        
        # Check if the route is protected (requires JWT validation)
        if request.url.path in protected_routes:
            # Debugging step: log the Authorization header
            print(f"Authorization Header: {auth_header}")
            # Retrieve the Authorization header
            auth_header = request.headers.get("Authorization")
            
            if auth_header:
                # Check if the header follows the "Bearer <token>" format
                try:
                    scheme, token = auth_header.split()
                    if scheme.lower() != "bearer":
                        raise ValueError("Invalid auth scheme")
                except ValueError:
                    raise HTTPException(status_code=403, detail="Invalid authorization header")

                # Validate and decode the JWT token
                payload = verify_token(token)
                if payload is None:
                    raise HTTPException(status_code=403, detail="Invalid or expired token")

                # Attach user info to request state for access in endpoints
                request.state.user = payload  # Save payload info for later use
            else:
                raise HTTPException(status_code=401, detail="Authorization header missing")
        
        # Proceed with the request, whether or not JWT validation was applied
        response = await call_next(request)
        return response
