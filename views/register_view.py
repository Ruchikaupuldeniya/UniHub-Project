import flet as ft
from themes.color_theme import AppTheme
from config.app_config import AppConfig
from controllers.auth_controller import AuthController

def build_register_view(page: ft.Page, params: dict[str, str]) -> ft.View:
    page.title = f"New Student Registration - {AppConfig.APP_NAME}"
    is_dark = page.theme_mode == ft.ThemeMode.DARK

    # 1. Faculty to Department Mapping
    faculty_departments = {
        "Faculty of Applied Science": [
            "Department of Bio-Science",
            "Department of Physical Science"
        ],
        "Faculty of Business Studies": [
            "Business Economics",
            "English Language Teaching",
            "Finance and Accountancy",
            "Human Resource Management",
            "Management and Entrepreneurship",
            "Marketing Management",
            "Project Management"
        ],
        "Faculty of Technological Studies": [
            "Department of ICT"
        ]
    }

    # 2. Form Input fields
    email_field = ft.TextField(
        label="University Email Address",
        hint_text="e.g. username@vau.ac.lk",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=10,
        border_width=1,
        height=52,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )
    
    password_field = ft.TextField(
        label="Password",
        prefix_icon=ft.Icons.LOCK_OUTLINED,
        password=True,
        can_reveal_password=True,
        border_radius=10,
        border_width=1,
        height=52,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    confirm_password_field = ft.TextField(
        label="Confirm Password",
        prefix_icon=ft.Icons.LOCK_RESET_ROUNDED,
        password=True,
        can_reveal_password=True,
        border_radius=10,
        border_width=1,
        height=52,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    reg_num_field = ft.TextField(
        label="Registration Number",
        hint_text="e.g. 2021/ICT/80",
        prefix_icon=ft.Icons.NUMBERS_ROUNDED,
        border_radius=10,
        border_width=1,
        height=52,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    name_field = ft.TextField(
        label="Full Name",
        hint_text="e.g. Jane Doe",
        prefix_icon=ft.Icons.PERSON_OUTLINED,
        border_radius=10,
        border_width=1,
        height=52,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    initial_faculty = "Faculty of Applied Science"
    initial_depts = faculty_departments[initial_faculty]

    faculty_dropdown = ft.Dropdown(
        label="Faculty",
        border_radius=10,
        border_width=1,
        height=52,
        value=initial_faculty,
        options=[ft.dropdown.Option(fac) for fac in faculty_departments.keys()],
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    department_dropdown = ft.Dropdown(
        label="Department",
        border_radius=10,
        border_width=1,
        height=52,
        value=initial_depts[0],
        options=[ft.dropdown.Option(dept) for dept in initial_depts],
        disabled=False,
        focused_border_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
    )

    # Dynamic loading of departments when faculty changes
    def handle_faculty_change(e):
        selected_faculty = faculty_dropdown.value
        depts = faculty_departments.get(selected_faculty, [])
        
        department_dropdown.options.clear()
        for dept in depts:
            department_dropdown.options.append(ft.dropdown.Option(dept))
            
        department_dropdown.value = depts[0] if depts else None
        department_dropdown.update()

    faculty_dropdown.on_change = handle_faculty_change

    error_text = ft.Text(value="", color=ft.Colors.RED_400, size=13, weight=ft.FontWeight.W_500)
    progress_bar = ft.ProgressBar(visible=False, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK)

    # Submit Handler
    def handle_submit(e):
        AuthController.register(
            page=page,
            email=email_field.value,
            password=password_field.value,
            confirm_password=confirm_password_field.value,
            reg_num=reg_num_field.value,
            name=name_field.value,
            faculty=faculty_dropdown.value or "",
            department=department_dropdown.value or "",
            error_text=error_text,
            progress_bar=progress_bar
        )

    submit_button = ft.FilledButton(
        content="Register",
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        ),
        width=320,
        on_click=handle_submit
    )

    # UI structure
    theme_toggle = ft.IconButton(
        icon=ft.Icons.DARK_MODE if not is_dark else ft.Icons.LIGHT_MODE,
        on_click=lambda _: toggle_theme(page),
        icon_size=24
    )

    card_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([theme_toggle], alignment=ft.MainAxisAlignment.END),
                ft.Icon(ft.Icons.HOW_TO_REG, size=50, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                ft.Text("Student Registration", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("UniHub Student Portal", size=12, italic=True, color=ft.Colors.GREY_500),
                progress_bar,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                name_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                reg_num_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                faculty_dropdown,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                department_dropdown,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                email_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                password_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                confirm_password_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                error_text,
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                submit_button,
                ft.TextButton(
                    content="Already have an account? Sign In",
                    on_click=lambda _: page.run_task(page.push_route, "/login")
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        ),
        width=400,
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

    # Scrollable column wrapper in case screen height is limited (especially on mobile)
    scroll_column = ft.Column(
        controls=[
            ft.Container(
                content=card_container,
                margin=ft.Margin.symmetric(vertical=40),
                alignment=ft.Alignment.CENTER
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )

    return ft.View(
        route="/register",
        controls=[
            ft.Container(
                content=scroll_column,
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
