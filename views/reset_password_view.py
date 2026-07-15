import flet as ft
from themes.color_theme import AppTheme
from config.app_config import AppConfig
from controllers.auth_controller import AuthController

def build_reset_password_view(page: ft.Page, params: dict[str, str]) -> ft.View:
    page.title = f"Reset Password - {AppConfig.APP_NAME}"
    is_dark = page.theme_mode == ft.ThemeMode.DARK

    email_field = ft.TextField(
        label="Enter Registered Email",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=10,
        border_width=1,
        height=52,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    error_text = ft.Text(value="", color=ft.Colors.RED_400, size=13, weight=ft.FontWeight.W_500)
    success_text = ft.Text(value="", color=ft.Colors.GREEN_400, size=13, weight=ft.FontWeight.W_500)
    progress_bar = ft.ProgressBar(visible=False, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK)

    # Submit Handler
    def handle_submit(e):
        AuthController.reset_password(
            page=page,
            email=email_field.value,
            error_text=error_text,
            success_text=success_text,
            progress_bar=progress_bar
        )

    submit_button = ft.FilledButton(
        content="Send Password Reset Link",
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        ),
        width=320,
        on_click=handle_submit
    )

    theme_toggle = ft.IconButton(
        icon=ft.Icons.DARK_MODE if not is_dark else ft.Icons.LIGHT_MODE,
        on_click=lambda _: toggle_theme(page),
        icon_size=24
    )

    card_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([theme_toggle], alignment=ft.MainAxisAlignment.END),
                ft.Icon(icon=ft.Icons.LOCK_RESET_ROUNDED, size=50, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                ft.Text("Reset Password", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("Enter your email to receive a recovery link", size=12, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
                progress_bar,
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                email_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                error_text,
                success_text,
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                submit_button,
                ft.TextButton(
                    content="Back to Sign In",
                    on_click=lambda _: page.run_task(page.push_route, "/login")
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        ),
        width=360,
        padding=24,
        border_radius=16,
        bgcolor=ft.Colors.with_opacity(0.75, AppTheme.SURFACE_DARK) if is_dark else ft.Colors.with_opacity(0.85, AppTheme.SURFACE_LIGHT),
        blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
        border=ft.Border.all(1.5, "#475569" if is_dark else "#CBD5E1"),
        shadow=[
            ft.BoxShadow(
                blur_radius=30,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK) if is_dark else ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 10)
            )
        ]
    )

    return ft.View(
        route="/reset-password",
        controls=[
            ft.Container(
                content=card_container,
                alignment=ft.Alignment.CENTER,
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT,
                    colors=[
                        "#3B0029" if is_dark else "#FFF5F7",
                        "#0F172A" if is_dark else "#E2E8F0"
                    ]
                ),
                image=ft.DecorationImage(
                    src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Vavuniya_campus.jpg",
                    fit=ft.BoxFit.COVER,
                    opacity=0.25 if is_dark else 0.15
                )
            )
        ],
        padding=0
    )

def toggle_theme(page: ft.Page):
    if page.theme_mode == ft.ThemeMode.DARK:
        page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme_mode = ft.ThemeMode.DARK
    if hasattr(page, "router") and page.router:
        page.router.handle_route_change(ft.RouteChangeEvent(name="change", control=page, route=page.route))
    else:
        page.update()
