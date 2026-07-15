import flet as ft
from themes.color_theme import AppTheme

def build_404_view(page: ft.Page, params: dict[str, str]) -> ft.View:
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    return ft.View(
        route="/404",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            icon=ft.Icons.WRONG_LOCATION_ROUNDED,
                            color=ft.Colors.RED_400,
                            size=80
                        ),
                        ft.Text("404", size=60, weight=ft.FontWeight.BOLD),
                        ft.Text("Page Not Found", size=20, weight=ft.FontWeight.W_500),
                        ft.Text(
                            "The route you are looking for does not exist or has been moved.",
                            size=14,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content="Go Back Home",
                            on_click=lambda _: page.run_task(page.push_route, "/"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        ]
    )

def build_403_view(page: ft.Page, params: dict[str, str]) -> ft.View:
    return ft.View(
        route="/403",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            icon=ft.Icons.GPP_BAD_ROUNDED,
                            color=ft.Colors.ORANGE_500,
                            size=80
                        ),
                        ft.Text("403", size=60, weight=ft.FontWeight.BOLD),
                        ft.Text("Access Denied", size=20, weight=ft.FontWeight.W_500),
                        ft.Text(
                            "You do not have permission to access this page.",
                            size=14,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content="Go Back Home",
                            on_click=lambda _: page.run_task(page.push_route, "/"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        ]
    )
