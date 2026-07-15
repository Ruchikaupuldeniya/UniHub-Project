import flet as ft
from config.app_config import AppConfig
from themes.color_theme import AppTheme
from routing.router import Router
from firebase.firebase_service import FirebaseService

# View Imports
from views.login_view import build_login_view
from views.error_view import build_404_view, build_403_view
from views.dashboard_view import build_student_dashboard, build_admin_dashboard
from views.register_view import build_register_view
from views.reset_password_view import build_reset_password_view

def main(page: ft.Page):
    # 1. Initialize Window & Page Properties
    page.title = AppConfig.APP_NAME
    page.theme_mode = ft.ThemeMode.LIGHT  # Default to Light Theme
    page.theme = AppTheme.get_light_theme()
    page.dark_theme = AppTheme.get_dark_theme()
    
    # Configure Desktop window sizing if running on desktop
    page.window_width = AppConfig.WINDOW_WIDTH
    page.window_height = AppConfig.WINDOW_HEIGHT
    page.window_min_width = AppConfig.WINDOW_MIN_WIDTH
    page.window_min_height = AppConfig.WINDOW_MIN_HEIGHT
    page.window_resizable = True
    page.update()

    # 2. Initialize Firebase SDK
    FirebaseService.initialize()

    # 3. Initialize & Configure Router
    router = Router(page)
    # Bind router to page so views can reference it programmatically
    page.router = router
    page.data = {"router": router}
    
    # 4. Register Routes
    # Landing path is also login path
    router.register_route("/", build_login_view)
    router.register_route("/login", build_login_view)
    router.register_route("/register", build_register_view)
    router.register_route("/reset-password", build_reset_password_view)
    router.register_route("/student/dashboard", build_student_dashboard)
    router.register_route("/admin/dashboard", build_admin_dashboard)
    router.register_route("/404", build_404_view)
    router.register_route("/403", build_403_view)

    # 5. Bind Navigation Handlers
    page.on_route_change = router.handle_route_change
    page.on_view_pop = router.handle_view_pop

    # 6. Kickstart Navigation to the Initial Route
    # Go to landing, if already logged in (checked by guards) it will route to home
    page.run_task(page.push_route, page.route if page.route and page.route != "/" else "/login")

if __name__ == "__main__":
    import sys
    view_mode = ft.AppView.WEB_BROWSER if "--web" in sys.argv else ft.AppView.FLET_APP
    port = 8550 if "--web" in sys.argv else 0
    ft.run(main, view=view_mode, port=port, assets_dir="assets")
