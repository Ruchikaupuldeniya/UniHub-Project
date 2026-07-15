import re
import flet as ft
from typing import Callable, Dict, Any, Optional

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes: Dict[str, Callable[[ft.Page, Dict[str, str]], ft.View]] = {}
        self.route_patterns: list[tuple[re.Pattern, str, Callable[[ft.Page, Dict[str, str]], ft.View]]] = []
        
        # User session parameters for route protection
        self.current_user: Optional[Dict[str, Any]] = None  # Holds user dict: {"uid": ..., "role": "student"|"admin"}
        
        # Guard definitions: path prefix -> required role
        self.guards = {
            "/admin": "administrator",
            "/student": "student"
        }
        
        # Default route configuration
        self.login_route = "/login"
        self.error_route = "/404"
        self.access_denied_route = "/403"

    def register_route(self, route_path: str, view_builder: Callable[[ft.Page, Dict[str, str]], ft.View]):
        """
        Registers a route. Supports path parameters using syntax like '/course/:id'.
        """
        self.routes[route_path] = view_builder
        
        # Convert path parameters (e.g. :id) to regex group captures
        regex_path = re.sub(r':([a-zA-Z0-9_]+)', r'(?P<\1>[^/]+)', route_path)
        # Match from start to end of route path
        pattern = re.compile(f"^{regex_path}$")
        self.route_patterns.append((pattern, route_path, view_builder))

    def navigate_to(self, route: str):
        """
        Programmatically navigates the app to a new route.
        """
        self.page.run_task(self.page.push_route, route)

    def handle_route_change(self, e: ft.RouteChangeEvent):
        """
        Handles the event when the route changes. Validates guards and appends the view to page.views.
        """
        route = e.route
        self.page.views.clear()
        
        # 1. Evaluate guards (Route protection)
        allowed, redirect_to = self._check_guards(route)
        if not allowed:
            self.page.run_task(self.page.push_route, redirect_to)
            return

        # 2. Resolve matching route pattern and compile view
        view = self._resolve_route(route)
        if view:
            self.page.views.append(view)
        else:
            # Route not found - fallback to 404
            error_view = self._resolve_route(self.error_route)
            if error_view:
                self.page.views.append(error_view)
            else:
                # Basic inline fallback 404 if no 404 view is registered
                self.page.views.append(
                    ft.View(
                        route="/404",
                        controls=[
                            ft.AppBar(title=ft.Text("404 Not Found")),
                            ft.Container(
                                content=ft.Text("The requested page was not found.", size=20),
                                alignment=ft.Alignment.CENTER,
                                expand=True
                            )
                        ]
                    )
                )
        self.page.update()

    def handle_view_pop(self, e: ft.ViewPopEvent):
        """
        Handles the browser/device back button.
        """
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.run_task(self.page.push_route, top_view.route)

    def set_user_session(self, user_data: Optional[Dict[str, Any]]):
        """
        Sets the user session information (e.g. {"uid": "abc", "role": "student"})
        """
        self.current_user = user_data

    def clear_user_session(self):
        """
        Logs out / clears current user session.
        """
        self.current_user = None

    def _check_guards(self, route: str) -> tuple[bool, str]:
        """
        Verifies if current user meets requirements for the given route path.
        Returns (is_allowed, redirect_path)
        """
        # If user is not authenticated and is trying to access a guarded path, redirect to login
        is_guarded = any(route.startswith(prefix) for prefix in self.guards.keys())
        
        if is_guarded and not self.current_user:
            return False, self.login_route
            
        if self.current_user:
            user_role = self.current_user.get("role", "student").lower()
            
            # Admins have access to everything
            if user_role == "administrator":
                return True, ""
                
            # If student attempts to access admin space, redirect to access denied / student dashboard
            if route.startswith("/admin") and user_role != "administrator":
                return False, self.access_denied_route
                
            # If user is logged in, restrict landing/login access, redirect to their home
            if route in ["/", "/login", "/register"]:
                if user_role == "administrator":
                    return False, "/admin/dashboard"
                else:
                    return False, "/student/dashboard"

        return True, ""

    def _resolve_route(self, route: str) -> Optional[ft.View]:
        """
        Matches a route string against registered routes/patterns, extracts parameters, and builds the view.
        """
        # Strip query params for pattern matching but pass them inside params
        path_part = route.split("?")[0]
        query_params = {}
        
        if "?" in route:
            query_part = route.split("?")[1]
            for kv in query_part.split("&"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    query_params[k] = v

        for pattern, route_template, view_builder in self.route_patterns:
            match = pattern.match(path_part)
            if match:
                # Merge query parameters and path parameters
                params = {**query_params, **match.groupdict()}
                return view_builder(self.page, params)
                
        return None
