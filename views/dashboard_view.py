import flet as ft
import time
from themes.color_theme import AppTheme
from services.auth_service import AuthService
from services.bot_service import BotService
from services.attendance_service import AttendanceService
from services.admin_service import AdminService
from services.club_service import ClubService

def build_student_dashboard(page: ft.Page, params: dict[str, str]) -> ft.View:
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    current_uid = ""
    current_email = ""
    
    if hasattr(page, 'router') and page.router and page.router.current_user:
        current_uid = page.router.current_user.get("uid", "")
        current_email = page.router.current_user.get("email", "")

    # Retrieve student profile from database, use mock defaults if not found
    student_profile = AuthService.get_student_profile(current_uid)
    if not student_profile:
        # Create a mock default student profile
        student_profile = {
            "uid": current_uid or "mock_student_uid",
            "reg_num": "2021/ICT/80",
            "name": "Jane Doe",
            "faculty": "Faculty of Applied Science",
            "department": "Department of Physical Science",
            "is_active": True,
            "profile_pic": ""
        }
        
    # Standard GPA mock data
    gpa_history = {
        "Semester 1": 3.40,
        "Semester 2": 3.65,
        "Semester 3": 3.50,
        "Semester 4": 3.75,
        "Semester 5": 3.80,
    }

    # Tab State - persistent via page.data
    if not isinstance(page.data, dict):
        page.data = {}
    active_tab = page.data.get("active_tab") or "overview"
    
    content_area = ft.Container(
        expand=True,
        padding=24,
        gradient=ft.LinearGradient(
            colors=["#0A0915", "#161233", "#0A0915"] if is_dark else ["#F8FAFC", "#EEF2F6"],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT
        )
    )

    # 1. Left Sidebar Navigation
    logo_row = ft.Row(
        [
            ft.Image(src="/app_logo.jpg", width=32, height=32, fit="contain"),
            ft.Text("UniHub", size=22, weight=ft.FontWeight.BOLD)
        ],
        spacing=10
    )

    sidebar_buttons = {}

    def switch_tab(tab_name):
        nonlocal active_tab
        active_tab = tab_name
        if isinstance(page.data, dict):
            page.data["active_tab"] = tab_name
        
        # Highlight active tab button
        for btn_name, btn in sidebar_buttons.items():
            is_active = (btn_name == tab_name)
            btn.bgcolor = (
                ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_LIGHT) if is_active and not is_dark 
                else (ft.Colors.with_opacity(0.2, AppTheme.PRIMARY_DARK) if is_active and is_dark else None)
            )
            # Update colors of children
            text_color = AppTheme.PRIMARY_LIGHT if is_active and not is_dark else (AppTheme.PRIMARY_DARK if is_active and is_dark else (ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700))
            btn.content.controls[0].color = text_color
            btn.content.controls[1].color = text_color
            
        content_area.content = build_tab_content(tab_name)
        page.update()

    # 2. Header Bar Theme Toggle Function
    def toggle_dashboard_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        
        if hasattr(page, "router") and page.router:
            page.router.handle_route_change(ft.RouteChangeEvent(name="change", control=page, route=page.route))
        else:
            page.update()

    theme_toggle_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE if not is_dark else ft.Icons.LIGHT_MODE,
        icon_size=20,
        icon_color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700,
        tooltip="Toggle Dark/Light Mode",
        on_click=toggle_dashboard_theme
    )

    header_bar = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Student Portal", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_100 if is_dark else ft.Colors.GREY_900),
                        ft.Text("Academic Year 2026/2027 • Active", size=11, color=ft.Colors.GREY_500 if is_dark else ft.Colors.GREY_600)
                    ],
                    spacing=2
                ),
                ft.Row(
                    [
                        theme_toggle_btn,
                        ft.VerticalDivider(width=1, color="#334155" if is_dark else "#E2E8F0"),
                        ft.Row(
                            [
                                ft.CircleAvatar(
                                    content=ft.Icon(ft.Icons.PERSON, size=18, color=ft.Colors.WHITE),
                                    radius=14,
                                    bgcolor=AppTheme.PRIMARY_LIGHT
                                ),
                                ft.Column(
                                    [
                                        ft.Text(student_profile.get("name", "Student"), size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_200 if is_dark else ft.Colors.GREY_800),
                                        ft.Text(student_profile.get("reg_num", "N/A"), size=10, color=ft.Colors.GREY_500)
                                    ],
                                    spacing=0
                                )
                            ],
                            spacing=8
                        )
                    ],
                    spacing=16
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=12),
        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
        border=ft.Border(bottom=ft.BorderSide(1, "#334155" if is_dark else "#E2E8F0")),
        height=64
    )

    def make_sidebar_btn(icon, text, tab_name):
        btn = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700),
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700)
                ],
                spacing=10
            ),
            padding=ft.Padding.symmetric(vertical=12, horizontal=16),
            border_radius=10,
            on_click=lambda e: switch_tab(tab_name),

        )
        sidebar_buttons[tab_name] = btn
        return btn

    # Populate sidebar options
    overview_btn = make_sidebar_btn(ft.Icons.DASHBOARD_ROUNDED, "Overview", "overview")
    profile_btn = make_sidebar_btn(ft.Icons.PERSON_ROUNDED, "Academic Profile", "profile")
    gpa_btn = make_sidebar_btn(ft.Icons.BAR_CHART_ROUNDED, "GPA Tracker", "gpa")
    attendance_btn = make_sidebar_btn(ft.Icons.CALENDAR_MONTH_ROUNDED, "Attendance", "attendance")
    clubs_btn = make_sidebar_btn(ft.Icons.GROUPS_ROUNDED, "Club Events", "clubs")
    cafeteria_btn = make_sidebar_btn(ft.Icons.RESTAURANT_ROUNDED, "Cafeteria", "cafeteria")
    assistant_btn = make_sidebar_btn(ft.Icons.SMART_TOY_ROUNDED, "AI Companion", "assistant")

    def handle_logout(e):
        if hasattr(page, 'router') and page.router:
            page.router.clear_user_session()
            page.run_task(page.push_route, "/login")

    logout_btn = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color=ft.Colors.RED_400),
                ft.Text("Sign Out", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.RED_400)
            ],
            spacing=10
        ),
        padding=ft.Padding.symmetric(vertical=12, horizontal=16),
        border_radius=10,
        on_click=handle_logout,

    )

    sidebar = ft.Container(
        content=ft.Column(
            [
                logo_row,
                ft.Divider(height=20, color=ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_300),
                overview_btn,
                profile_btn,
                gpa_btn,
                attendance_btn,
                clubs_btn,
                cafeteria_btn,
                assistant_btn,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                logout_btn
            ],
            spacing=8
        ),
        width=240,
        padding=16,
        bgcolor=AppTheme.SURFACE_DARK if is_dark else "#F1F5F9",
        border=ft.Border(right=ft.BorderSide(1, "#334155" if is_dark else "#E2E8F0"))
    )

    # 2. Build Tab Content Dynamically
    def build_tab_content(tab_name) -> ft.Control:
        nonlocal student_profile
        
        # Sync profile data from auth service
        refreshed = AuthService.get_student_profile(current_uid)
        if refreshed:
            student_profile = refreshed
            
        if tab_name == "overview":
            # Welcome banner
            welcome_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Welcome back, {student_profile.get('name', 'Student')}! 👋", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Campus Companion helps you manage your academics and query smart insights about your curriculum.", size=14, color=ft.Colors.WHITE70),
                    ],
                    spacing=5
                ),
                padding=24,
                border_radius=16,
                gradient=ft.LinearGradient(
                    colors=[AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK, "#8A2387"],
                    begin=ft.Alignment.TOP_LEFT,
                    end=ft.Alignment.BOTTOM_RIGHT
                ),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK), offset=ft.Offset(0, 4))
            )
            
            # Quick Stats Row
            avg_gpa = sum(gpa_history.values()) / len(gpa_history)
            
            stat_gpa = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cumulative GPA", size=12, color=ft.Colors.GREY_500),
                        ft.Text(f"{avg_gpa:.2f}", size=28, weight=ft.FontWeight.BOLD, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                    ],
                    spacing=2
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                expand=True
            )

            stat_dept = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Department", size=12, color=ft.Colors.GREY_500),
                        ft.Text(student_profile.get("department", "ICT").replace("Department of ", ""), size=14, weight=ft.FontWeight.BOLD, overflow=ft.TextOverflow.ELLIPSIS),
                    ],
                    spacing=5
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                expand=True
            )

            stat_status = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Portal Status", size=12, color=ft.Colors.GREY_500),
                        ft.Row(
                            [
                                ft.Container(width=10, height=10, bgcolor=ft.Colors.GREEN_400, border_radius=5),
                                ft.Text("Active Student", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400 if is_dark else ft.Colors.GREEN_700)
                            ],
                            spacing=5
                        )
                    ],
                    spacing=5
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                expand=True
            )

            stats_row = ft.Row([stat_gpa, stat_dept, stat_status], spacing=16)

            # Quick Link Info
            info_card = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.LIGHTBULB_CIRCLE_ROUNDED, color=ft.Colors.AMBER_400, size=32),
                        ft.Column(
                            [
                                ft.Text("Need help with University guidelines?", size=14, weight=ft.FontWeight.BOLD),
                                ft.Text("Head over to the AI Companion tab to query schedules, syllabus contents, and guidelines.", size=12, color=ft.Colors.GREY_500)
                            ],
                            spacing=2,
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                            on_click=lambda e: switch_tab("assistant")
                        )
                    ]
                ),
                padding=16,
                border_radius=12,
                bgcolor=ft.Colors.with_opacity(0.05, AppTheme.PRIMARY_LIGHT)
            )
            return ft.Column([welcome_card, ft.Divider(height=10, color=ft.Colors.TRANSPARENT), stats_row, ft.Divider(height=10, color=ft.Colors.TRANSPARENT), info_card], spacing=16)

        elif tab_name == "profile":
            name_input = ft.TextField(label="Full Name", value=student_profile.get("name", ""), border_radius=8)
            
            # Faculty & Dept selectors
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

            faculty_dropdown = ft.Dropdown(
                label="Faculty",
                border_radius=8,
                options=[ft.dropdown.Option(fac) for fac in faculty_departments.keys()],
                value=student_profile.get("faculty", "")
            )

            current_dept = student_profile.get("department", "")
            dept_list = faculty_departments.get(student_profile.get("faculty", ""), [])
            dept_options = [ft.dropdown.Option(dept) for dept in dept_list]
            if current_dept and current_dept not in dept_list:
                dept_options.append(ft.dropdown.Option(current_dept))

            dept_dropdown = ft.Dropdown(
                label="Department",
                border_radius=8,
                options=dept_options,
                value=current_dept
            )

            def handle_fac_change(e):
                new_depts = faculty_departments.get(faculty_dropdown.value, [])
                
                dept_dropdown.options.clear()
                for d in new_depts:
                    dept_dropdown.options.append(ft.dropdown.Option(d))
                    
                dept_dropdown.value = new_depts[0] if new_depts else None
                dept_dropdown.update()

            faculty_dropdown.on_change = handle_fac_change

            def save_profile(e):
                if not faculty_dropdown.value or not dept_dropdown.value:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please select both Faculty and Department."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                updates = {
                    "name": name_input.value,
                    "faculty": faculty_dropdown.value,
                    "department": dept_dropdown.value
                }
                if AuthService.update_student_profile(current_uid, updates):
                    page.snack_bar = ft.SnackBar(content=ft.Text("Profile updated successfully!"), bgcolor=ft.Colors.GREEN_600)
                    page.snack_bar.open = True
                    # Refresh local page layout
                    switch_tab("profile")
                else:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Failed to update profile."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True

            save_btn = ft.FilledButton(
                content=ft.Text("Save Changes", color=ft.Colors.WHITE),
                style=ft.ButtonStyle(
                    bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                on_click=save_profile
            )

            profile_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.CircleAvatar(
                                    content=ft.Icon(ft.Icons.PERSON, size=40, color=ft.Colors.WHITE),
                                    radius=40,
                                    bgcolor=AppTheme.PRIMARY_LIGHT
                                ),
                                ft.Column(
                                    [
                                        ft.Text(student_profile.get("name", "Student"), size=20, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Reg No: {student_profile.get('reg_num', 'N/A')}", size=14, color=ft.Colors.GREY_500),
                                        ft.Text(f"Official Email: {current_email}", size=14, color=ft.Colors.GREY_500),
                                    ],
                                    spacing=2
                                )
                            ],
                            spacing=20
                        ),
                        ft.Divider(height=20),
                        ft.Text("Edit Academic Information", size=16, weight=ft.FontWeight.BOLD),
                        name_input,
                        faculty_dropdown,
                        dept_dropdown,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        save_btn
                    ],
                    spacing=12
                ),
                padding=24,
                border_radius=16,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )

            # Change Password section
            new_pwd_input = ft.TextField(
                label="New Password",
                password=True,
                can_reveal_password=True,
                border_radius=8,
                prefix_icon=ft.Icons.LOCK_OUTLINED,
                height=52
            )
            confirm_pwd_input = ft.TextField(
                label="Confirm New Password",
                password=True,
                can_reveal_password=True,
                border_radius=8,
                prefix_icon=ft.Icons.LOCK_OUTLINED,
                height=52
            )
            pwd_error_text = ft.Text(value="", color=ft.Colors.RED_400, size=12)
            
            def handle_change_password(e):
                new_pwd = new_pwd_input.value
                confirm_pwd = confirm_pwd_input.value
                
                if not new_pwd or not confirm_pwd:
                    pwd_error_text.value = "Please enter and confirm your new password."
                    pwd_error_text.color = ft.Colors.RED_400
                    page.update()
                    return
                
                if new_pwd != confirm_pwd:
                    pwd_error_text.value = "Passwords do not match."
                    pwd_error_text.color = ft.Colors.RED_400
                    page.update()
                    return
                
                from utils.validators import Validators
                is_strong, pwd_msg = Validators.is_valid_password(new_pwd)
                if not is_strong:
                    pwd_error_text.value = pwd_msg
                    pwd_error_text.color = ft.Colors.RED_400
                    page.update()
                    return
                
                try:
                    current_token = ""
                    if hasattr(page, 'router') and page.router and page.router.current_user:
                        current_token = page.router.current_user.get("token", "")
                    
                    if AuthService.change_password(current_uid, current_token, new_pwd):
                        pwd_error_text.value = "Password updated successfully!"
                        pwd_error_text.color = ft.Colors.GREEN_400
                        new_pwd_input.value = ""
                        confirm_pwd_input.value = ""
                        page.update()
                    else:
                        pwd_error_text.value = "Failed to update password."
                        pwd_error_text.color = ft.Colors.RED_400
                        page.update()
                except Exception as ex:
                    pwd_error_text.value = str(ex)
                    pwd_error_text.color = ft.Colors.RED_400
                    page.update()

            change_pwd_btn = ft.FilledButton(
                content=ft.Text("Update Password", color=ft.Colors.WHITE),
                style=ft.ButtonStyle(
                    bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                on_click=handle_change_password
            )

            change_password_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Security & Password", size=16, weight=ft.FontWeight.BOLD),
                        new_pwd_input,
                        confirm_pwd_input,
                        pwd_error_text,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        change_pwd_btn
                    ],
                    spacing=12
                ),
                padding=24,
                border_radius=16,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )
            
            return ft.Column([profile_card, change_password_card], spacing=16, scroll=ft.ScrollMode.AUTO)

        elif tab_name == "gpa":
            # Interactive custom bar chart using Container boxes
            chart_bars = []
            max_gpa = 4.0
            
            for semester, val in gpa_history.items():
                gpa_val = float(val)
                bar_height = (gpa_val / max_gpa) * 180
                
                bar = ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(f"{gpa_val:.2f}", size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                            width=50,
                            height=bar_height,
                            border_radius=ft.BorderRadius.only(top_left=6, top_right=6),
                            gradient=ft.LinearGradient(
                                colors=[AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK, "#EC4899"],
                                begin=ft.Alignment.BOTTOM_CENTER,
                                end=ft.Alignment.TOP_CENTER
                            ),
                            alignment=ft.Alignment.TOP_CENTER,
                            padding=ft.Padding.only(top=5)
                        ),
                        ft.Text(semester.replace("Semester ", "Sem "), size=11, color=ft.Colors.GREY_500)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
                chart_bars.append(bar)

            chart_row = ft.Container(
                content=ft.Row(
                    chart_bars,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.END
                ),
                padding=ft.Padding.all(20),
                height=250,
                border=ft.Border(bottom=ft.BorderSide(2, "#334155" if is_dark else "#CBD5E1")),
                margin=ft.Margin.only(bottom=10)
            )

            # GPA Inputs for edits
            inputs_column = ft.Column(spacing=10)
            
            def handle_gpa_change(sem_key, input_field):
                val_str = input_field.value
                try:
                    val = float(val_str)
                    if 0.0 <= val <= 4.0:
                        gpa_history[sem_key] = val
                        switch_tab("gpa") # Refresh layout
                    else:
                        page.snack_bar = ft.SnackBar(content=ft.Text("GPA must be between 0.0 and 4.0"))
                        page.snack_bar.open = True
                except ValueError:
                    pass

            for semester, val in gpa_history.items():
                input_field = ft.TextField(
                    label=semester,
                    value=str(val),
                    width=120,
                    border_radius=8,
                    height=45,
                    text_size=13
                )
                input_field.on_change = lambda e, s=semester, f=input_field: handle_gpa_change(s, f)
                inputs_column.controls.append(input_field)

            avg_gpa = sum(gpa_history.values()) / len(gpa_history)
            
            # 3D illustration and gauge card
            illustration_card = ft.Container(
                content=ft.Image(
                    src="/gpa_3d.png",
                    width=200,
                    height=200,
                    fit="contain"
                ),
                alignment=ft.Alignment.CENTER
            )

            gauge_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cumulative GPA Status", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_400),
                        ft.Stack(
                            [
                                ft.ProgressRing(value=avg_gpa / 4.0, stroke_width=8, width=120, height=120, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                ft.Container(
                                    content=ft.Text(f"{avg_gpa:.2f}", size=24, weight=ft.FontWeight.BOLD),
                                    alignment=ft.Alignment.CENTER,
                                    width=120,
                                    height=120
                                )
                            ],
                            alignment=ft.Alignment.CENTER
                        ),
                        ft.Text("Scale: 0.00 - 4.00 Max", size=11, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=20,
                border_radius=16,
                border=ft.Border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE) if is_dark else ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE) if is_dark else ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                width=240,
                alignment=ft.Alignment.CENTER
            )

            gpa_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.BAR_CHART_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK, size=28),
                                ft.Text("GPA Performance Console", size=18, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            [
                                gauge_card,
                                illustration_card,
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text("Edit Semester GPAs (Updates Chart Live):", size=13, weight=ft.FontWeight.BOLD),
                                            ft.Row(inputs_column.controls, wrap=True, spacing=10)
                                        ],
                                        spacing=8
                                    ),
                                    expand=True,
                                    padding=10
                                )
                            ],
                            spacing=20,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Text("GPA Trend Analysis Diagram", size=14, weight=ft.FontWeight.BOLD),
                        chart_row
                    ],
                    spacing=12,
                    scroll=ft.ScrollMode.ADAPTIVE
                ),
                expand=True
            )
            return gpa_card

        elif tab_name == "attendance":
            from services.attendance_service import AttendanceService
            attendance_data = AttendanceService.get_attendance(current_uid)
            overall_percent = AttendanceService.calculate_percentage(attendance_data)
            at_risk = AttendanceService.subjects_at_risk(attendance_data)
            
            status_text = "Good Standing" if overall_percent >= 75.0 else "At Risk"
            status_color = ft.Colors.GREEN_600 if overall_percent >= 75.0 else ft.Colors.RED_600
            
            overall_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Overall Attendance Percentage", size=12, color=ft.Colors.GREY_500),
                        ft.Row(
                            [
                                ft.Text(f"{overall_percent:.1f}%", size=28, weight=ft.FontWeight.BOLD, color=status_color),
                                ft.Container(
                                    content=ft.Text(status_text, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    bgcolor=status_color,
                                    padding=ft.Padding.symmetric(vertical=4, horizontal=10),
                                    border_radius=15
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.ProgressBar(value=overall_percent / 100, color=status_color, bgcolor=ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_200)
                    ],
                    spacing=10
                ),
                padding=20,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )
            
            module_rows = []
            for subject, (attended, total) in attendance_data.items():
                percent = (attended / total) * 100 if total > 0 else 0.0
                subject_at_risk = percent < 75.0
                subject_status_color = ft.Colors.GREEN_500 if not subject_at_risk else ft.Colors.RED_500
                
                module_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(subject, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(f"{attended} / {total}")),
                            ft.DataCell(ft.Text(f"{percent:.1f}%", color=subject_status_color, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.CHECK_CIRCLE_ROUNDED if not subject_at_risk else ft.Icons.WARNING_ROUNDED,
                                            color=subject_status_color,
                                            size=18
                                        ),
                                        ft.Text(
                                            "On Track" if not subject_at_risk else "Low Attendance",
                                            color=subject_status_color,
                                            size=13
                                        )
                                    ],
                                    spacing=5
                                )
                            )
                        ]
                    )
                )
                
            attendance_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Lecture Module")),
                    ft.DataColumn(ft.Text("Attended Sessions")),
                    ft.DataColumn(ft.Text("Percentage")),
                    ft.DataColumn(ft.Text("Status")),
                ],
                rows=module_rows,
                column_spacing=24
            )
            
            table_container = ft.Container(
                content=ft.Column([attendance_table], scroll=ft.ScrollMode.ADAPTIVE),
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                border_radius=12,
                padding=16,
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                expand=True
            )
            
            warning_box = ft.Container()
            if at_risk:
                at_risk_names = ", ".join([item["subject"] for item in at_risk])
                warning_box = ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.WARNING_ROUNDED, color=ft.Colors.AMBER_400, size=24),
                            ft.Text(f"Warning: Low attendance (<75%) detected in: {at_risk_names}. Ensure to attend upcoming sessions to meet exam eligibility criteria.", size=13, weight=ft.FontWeight.W_500, expand=True)
                        ]
                    ),
                    padding=16,
                    border_radius=12,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_400)
                )
                
            attendance_layout = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Attendance Status Panel", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    overall_card,
                    warning_box,
                    ft.Text("Course Attendance Breakdown", size=15, weight=ft.FontWeight.BOLD),
                    table_container
                ],
                spacing=16,
                expand=True
            )
            return attendance_layout

        elif tab_name == "assistant":
            chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
            
            chat_list.controls.append(
                ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=16, color=ft.Colors.WHITE),
                            radius=16,
                            bgcolor=ft.Colors.BLUE_GREY_600 if is_dark else ft.Colors.BLUE_GREY_400
                        ),
                        ft.Container(
                            content=ft.Markdown(BotService._get_mock_reply("hello", is_admin=False), selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                            bgcolor=ft.Colors.GREY_200 if not is_dark else "#1E293B",
                            padding=12,
                            border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_right=12),
                            width=500
                        )
                    ],
                    spacing=10
                )
            )
            
            chat_input = ft.TextField(
                hint_text="Ask me about modules, GPA calculations, or campus locations...",
                expand=True,
                border_radius=10,
                height=50,
                on_submit=lambda e: send_message(e)
            )
            
            def send_message(e):
                user_msg = chat_input.value.strip()
                if not user_msg:
                    return
                    
                chat_list.controls.append(
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(user_msg, size=13, color=ft.Colors.WHITE),
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                padding=12,
                                border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_left=12),
                                width=400
                            ),
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.WHITE),
                                radius=16,
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10
                    )
                )
                
                chat_input.value = ""
                page.update()
                
                typing_indicator = ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=16, color=ft.Colors.WHITE),
                            radius=16,
                            bgcolor=ft.Colors.BLUE_GREY_600 if is_dark else ft.Colors.BLUE_GREY_400
                        ),
                        ft.Container(
                            content=ft.Text("UniHub Companion is typing...", size=13, italic=True, color=ft.Colors.GREY_500),
                            bgcolor=ft.Colors.GREY_200 if not is_dark else "#1E293B",
                            padding=12,
                            border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_right=12)
                        )
                    ],
                    spacing=10
                )
                chat_list.controls.append(typing_indicator)
                page.update()
                
                time.sleep(0.5)
                
                bot_reply = BotService.get_reply(user_msg, is_admin=False)
                
                chat_list.controls.remove(typing_indicator)
                
                chat_list.controls.append(
                    ft.Row(
                        [
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=16, color=ft.Colors.WHITE),
                                radius=16,
                                bgcolor=ft.Colors.BLUE_GREY_600 if is_dark else ft.Colors.BLUE_GREY_400
                            ),
                            ft.Container(
                                content=ft.Markdown(bot_reply, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                                bgcolor=ft.Colors.GREY_200 if not is_dark else "#1E293B",
                                padding=12,
                                border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_right=12),
                                width=500
                            )
                        ],
                        spacing=10
                    )
                )
                page.update()
                
            send_btn = ft.IconButton(
                icon=ft.Icons.SEND_ROUNDED,
                icon_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                on_click=send_message
            )
            
            def on_chip_click(text):
                chat_input.value = text
                send_message(None)
                
            suggestion_chips = ft.Row(
                [
                    ft.Container(
                        content=ft.Text(label, size=12, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                        bgcolor=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_LIGHT) if not is_dark else ft.Colors.with_opacity(0.15, AppTheme.PRIMARY_DARK),
                        padding=ft.Padding.symmetric(vertical=6, horizontal=12),
                        border_radius=15,
                        on_click=lambda e, val=label: on_chip_click(val)
                    )
                    for label in ["GPA calculations", "Faculty of Applied Science", "Campus location"]
                ],
                spacing=10,
                wrap=True
            )
            
            assistant_layout = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SMART_TOY_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("UniHub Student Companion", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Text("Your smart academic companion powered by Gemini.", size=12, color=ft.Colors.GREY_500),
                    ft.Divider(height=10),
                    ft.Container(
                        content=chat_list,
                        expand=True,
                        padding=12,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        border_radius=12,
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else "#F8FAFC"
                    ),
                    suggestion_chips,
                    ft.Row([chat_input, send_btn], spacing=10)
                ],
                expand=True
            )
            return assistant_layout

        elif tab_name == "clubs":
            from services.club_service import ClubService
            clubs = ClubService.get_clubs()
            events = ClubService.get_events()

            club_cards = []
            for club in clubs:
                is_member = current_uid in club["members"]
                
                def toggle_join(e, cid=club["id"]):
                    ClubService.toggle_club_membership(current_uid, cid)
                    switch_tab("clubs")

                club_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(club["name"], size=14, weight=ft.FontWeight.BOLD),
                                ft.Text(club["description"], size=12, color=ft.Colors.GREY_500, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Row(
                                    [
                                        ft.Text(f"👥 {len(club['members'])} Members", size=11, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                        ft.TextButton(
                                            content=ft.Text("Joined" if is_member else "Join", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600 if is_member else AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                            on_click=toggle_join
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=8
                        ),
                        padding=12,
                        width=250,
                        border_radius=8,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
                    )
                )

            clubs_row = ft.Row(club_cards, scroll=ft.ScrollMode.ADAPTIVE, spacing=12)

            event_cards = []
            for event in events:
                is_reg = current_uid in event["registered_users"]
                is_rem = current_uid in event["reminders_enabled"]

                def toggle_reg(e, eid=event["id"]):
                    ClubService.toggle_event_registration(current_uid, eid)
                    switch_tab("clubs")

                def toggle_rem(e, eid=event["id"]):
                    ClubService.toggle_event_reminder(current_uid, eid)
                    switch_tab("clubs")

                event_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Image(
                                        src=event["image"],
                                        fit="cover",
                                        border_radius=8,
                                        width=300,
                                        height=150
                                    ),
                                    bgcolor=ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_200,
                                    border_radius=8
                                ),
                                ft.Text(event["title"], size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"📅 {event['date']} at {event['time']}", size=12, color=ft.Colors.GREY_500),
                                ft.Text(f"📍 {event['location']}", size=12, color=ft.Colors.GREY_500),
                                ft.Text(f"📣 Host: {event['club']}", size=12, weight=ft.FontWeight.W_500, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                ft.Text(event["description"], size=12, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Row(
                                    [
                                        ft.FilledButton(
                                            content=ft.Text("Registered" if is_reg else "Register", color=ft.Colors.WHITE),
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.GREEN_600 if is_reg else AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                                shape=ft.RoundedRectangleBorder(radius=6)
                                            ),
                                            on_click=toggle_reg
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.NOTIFICATION_ADD_ROUNDED if not is_rem else ft.Icons.NOTIFICATIONS_ACTIVE_ROUNDED,
                                            icon_color=ft.Colors.AMBER_500 if is_rem else ft.Colors.GREY_500,
                                            on_click=toggle_rem
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=8
                        ),
                        padding=16,
                        width=320,
                        border_radius=12,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
                    )
                )

            events_row = ft.Row(event_cards, scroll=ft.ScrollMode.ADAPTIVE, spacing=16)

            gallery_images = []
            for event in events:
                gallery_images.append(
                    ft.Container(
                        content=ft.Image(
                            src=event["image"],
                            fit="cover",
                            border_radius=10,
                            width=120,
                            height=120,
                            tooltip=event["title"]
                        ),
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0")
                    )
                )
            gallery_row = ft.Row(gallery_images, spacing=10, scroll=ft.ScrollMode.ADAPTIVE)

            # Build chronological timeline diagram
            timeline_items = []
            sorted_events = sorted(events, key=lambda x: x["date"])
            for idx, ev in enumerate(sorted_events):
                timeline_items.append(
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Text(str(idx + 1), weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                width=28,
                                height=28,
                                border_radius=14,
                                alignment=ft.Alignment.CENTER
                            ),
                            ft.Text(ev["date"], size=10, weight=ft.FontWeight.BOLD),
                            ft.Text(ev["title"], size=11, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=110, text_align=ft.TextAlign.CENTER)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4
                    )
                )
                if idx < len(sorted_events) - 1:
                    timeline_items.append(
                        ft.Container(
                            width=60,
                            height=2,
                            bgcolor="#334155" if is_dark else "#CBD5E1",
                            margin=ft.Margin.only(top=14)
                        )
                    )
            
            timeline_container = ft.Container(
                content=ft.Row(timeline_items, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START, scroll=ft.ScrollMode.ADAPTIVE),
                padding=20,
                border_radius=16,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=ft.Colors.with_opacity(0.02, AppTheme.PRIMARY_LIGHT),
                margin=ft.Margin.symmetric(vertical=10)
            )

            clubs_layout = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.GROUPS_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK, size=28),
                                            ft.Text("Campus Clubs & Events", size=18, weight=ft.FontWeight.BOLD),
                                        ],
                                        spacing=10
                                    ),
                                    ft.Text("Explore active student associations & societies:", size=13, color=ft.Colors.GREY_500),
                                ],
                                expand=True
                            ),
                            ft.Image(
                                src="/clubs_3d.png",
                                width=120,
                                height=100,
                                fit="contain"
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    clubs_row,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text("Chronological Event Roadmap", size=15, weight=ft.FontWeight.BOLD),
                    timeline_container,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text("Upcoming Event Registrations:", size=15, weight=ft.FontWeight.BOLD),
                    events_row,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text("Event Photo Gallery:", size=15, weight=ft.FontWeight.BOLD),
                    gallery_row
                ],
                spacing=12,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
            return clubs_layout

        elif tab_name == "cafeteria":
            from services.cafeteria_service import CafeteriaService
            menu_items = CafeteriaService.get_menu()
            student_orders = CafeteriaService.get_student_orders(current_uid)
            all_feedback = CafeteriaService.get_all_feedback()

            if "cafeteria_cart" not in page.data:
                page.data["cafeteria_cart"] = {}
            cart = page.data["cafeteria_cart"]

            def add_to_cart(item_id):
                cart[item_id] = cart.get(item_id, 0) + 1
                switch_tab("cafeteria")

            def remove_from_cart(item_id):
                if item_id in cart:
                    cart[item_id] -= 1
                    if cart[item_id] <= 0:
                        del cart[item_id]
                switch_tab("cafeteria")

            categories = ["Breakfast", "Lunch", "Snacks", "Beverages"]
            category_tabs = []
            
            # Map category to icon
            cat_icons = {
                "Breakfast": ft.Icons.FREE_BREAKFAST_ROUNDED,
                "Lunch": ft.Icons.LUNCH_DINING_ROUNDED,
                "Snacks": ft.Icons.COOKIE_ROUNDED,
                "Beverages": ft.Icons.LOCAL_DRINK_ROUNDED
            }
            
            for cat in categories:
                items_in_cat = [i for i in menu_items if i["category"] == cat and i["available"]]
                cat_controls = []
                for item in items_in_cat:
                    qty = cart.get(item["id"], 0)
                    cat_controls.append(
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(cat_icons.get(cat, ft.Icons.FASTFOOD_ROUNDED), size=24, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                    ft.Column(
                                        [
                                            ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD),
                                            ft.Text(f"Rs. {item['price']:.2f}", size=13, color=ft.Colors.GREY_500)
                                        ],
                                        spacing=2,
                                        expand=True
                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINED, on_click=lambda e, iid=item["id"]: remove_from_cart(iid), icon_size=20),
                                            ft.Text(str(qty), size=14, weight=ft.FontWeight.BOLD),
                                            ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINED, on_click=lambda e, iid=item["id"]: add_to_cart(iid), icon_size=20)
                                        ],
                                        spacing=2
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=12,
                            border_radius=10,
                            border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                            bgcolor=ft.Colors.with_opacity(0.01, AppTheme.PRIMARY_LIGHT)
                        )
                    )
                category_tabs.append(ft.Column(cat_controls, spacing=8))

            menu_column = ft.Column(
                [
                    ft.Text("Today's Food Menu", size=16, weight=ft.FontWeight.BOLD),
                    ft.Tabs(
                        length=4,
                        selected_index=0,
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.TabBar(
                                    tabs=[
                                        ft.Tab(label="Breakfast"),
                                        ft.Tab(label="Lunch"),
                                        ft.Tab(label="Snacks"),
                                        ft.Tab(label="Beverages"),
                                    ]
                                ),
                                ft.TabBarView(
                                    expand=True,
                                    controls=category_tabs
                                )
                            ]
                        )
                    )
                ],
                expand=True
            )

            cart_rows = []
            subtotal = 0.0
            pre_order_items = []
            
            for item_id, qty in list(cart.items()):
                item = next((i for i in menu_items if i["id"] == item_id), None)
                if item:
                    item_total = item["price"] * qty
                    subtotal += item_total
                    pre_order_items.append({"name": item["name"], "quantity": qty, "price": item["price"]})
                    cart_rows.append(
                        ft.Row(
                            [
                                ft.Text(f"{item['name']} x{qty}", size=12, expand=True),
                                ft.Text(f"Rs. {item_total:.2f}", size=12, weight=ft.FontWeight.BOLD)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )

            pickup_time_dropdown = ft.Dropdown(
                label="Select Pickup Time",
                options=[
                    ft.dropdown.Option("08:00 AM"), ft.dropdown.Option("08:30 AM"),
                    ft.dropdown.Option("12:00 PM"), ft.dropdown.Option("12:30 PM"),
                    ft.dropdown.Option("01:00 PM"), ft.dropdown.Option("03:30 PM"),
                    ft.dropdown.Option("04:00 PM")
                ],
                value="12:30 PM",
                height=45,
                border_radius=8
            )

            def submit_order(e):
                if not pre_order_items:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Cart is empty!"))
                    page.snack_bar.open = True
                    page.update()
                    return
                CafeteriaService.place_pre_order(current_uid, pre_order_items, subtotal, pickup_time_dropdown.value)
                cart.clear()
                page.snack_bar = ft.SnackBar(content=ft.Text("Pre-order placed successfully! Check active orders."), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("cafeteria")

            checkout_btn = ft.FilledButton(
                content=ft.Text("Place Pre-order", color=ft.Colors.WHITE),
                style=ft.ButtonStyle(
                    bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                disabled=len(cart) == 0,
                on_click=submit_order
            )

            cart_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Order Cart", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Column(cart_rows if cart_rows else [ft.Text("Cart is empty", color=ft.Colors.GREY_500, italic=True)], spacing=6),
                        ft.Divider(height=10),
                        ft.Row(
                            [
                                ft.Text("Subtotal", size=13),
                                ft.Text(f"Rs. {subtotal:.2f}", size=14, weight=ft.FontWeight.BOLD)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        pickup_time_dropdown,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        checkout_btn
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=280
            )

            # Build graphical status tracking cards for pre-orders instead of simple table
            order_cards = []
            for ord in student_orders:
                items_str = ", ".join([f"{i['name']} (x{i['quantity']})" for i in ord["items"]])
                
                # Dynamic status timeline colors/icons
                is_pending = ord["status"] == "Pending"
                is_ready = ord["status"] == "Ready"
                is_delivered = ord["status"] == "Delivered"

                step1_color = ft.Colors.GREEN_600
                step2_color = ft.Colors.GREEN_600 if (is_ready or is_delivered) else ft.Colors.AMBER_600 if is_pending else ft.Colors.GREY_600
                step3_color = ft.Colors.GREEN_600 if is_delivered else ft.Colors.GREY_600

                stepper_row = ft.Row(
                    [
                        ft.Column([ft.Container(width=16, height=16, bgcolor=step1_color, border_radius=8), ft.Text("Placed", size=9, weight=ft.FontWeight.BOLD)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(width=40, height=2, bgcolor=step2_color, margin=ft.Margin.only(bottom=12)),
                        ft.Column([ft.Container(width=16, height=16, bgcolor=step2_color, border_radius=8), ft.Text("Preparing", size=9, weight=ft.FontWeight.BOLD)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Container(width=40, height=2, bgcolor=step3_color, margin=ft.Margin.only(bottom=12)),
                        ft.Column([ft.Container(width=16, height=16, bgcolor=step3_color, border_radius=8), ft.Text("Ready", size=9, weight=ft.FontWeight.BOLD)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )

                order_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(f"Order #{ord['id']}", size=13, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Rs. {ord['total_price']:.2f}", size=13, weight=ft.FontWeight.BOLD, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Text(items_str, size=12, color=ft.Colors.GREY_500, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"🕒 Pickup Scheduled: {ord['pickup_time']}", size=11, color=ft.Colors.GREY_500),
                                ft.Divider(height=10),
                                stepper_row
                            ],
                            spacing=6
                        ),
                        padding=12,
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=ft.Colors.with_opacity(0.01, AppTheme.PRIMARY_LIGHT),
                        width=280
                    )
                )

            orders_layout_control = ft.Row(
                order_cards if order_cards else [ft.Text("No active pre-orders found.", italic=True, color=ft.Colors.GREY_500)],
                wrap=True,
                spacing=10
            )

            orders_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Active Pre-orders Tracker", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        orders_layout_control
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                expand=True
            )

            rating_dropdown = ft.Dropdown(
                label="Rating",
                options=[ft.dropdown.Option(str(i)) for i in range(5, 0, -1)],
                value="5",
                width=100,
                height=45,
                border_radius=8
            )
            comment_input = ft.TextField(
                hint_text="Write a review about today's food...",
                expand=True,
                height=45,
                border_radius=8
            )

            def submit_feedback(e):
                com = comment_input.value.strip()
                if not com:
                    return
                CafeteriaService.submit_feedback(student_profile.get("name", "Student"), int(rating_dropdown.value), com)
                comment_input.value = ""
                page.snack_bar = ft.SnackBar(content=ft.Text("Feedback submitted! Thank you."), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("cafeteria")

            feedback_btn = ft.FilledButton(
                content=ft.Text("Submit Review", color=ft.Colors.WHITE),
                style=ft.ButtonStyle(
                    bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                    shape=ft.RoundedRectangleBorder(radius=8)
                ),
                on_click=submit_feedback
            )

            feedback_cards = []
            for fb in all_feedback[-3:]:
                stars = "★" * fb["rating"] + "☆" * (5 - fb["rating"])
                feedback_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(fb["student_name"], size=12, weight=ft.FontWeight.BOLD),
                                        ft.Text(stars, size=12, color=ft.Colors.AMBER_400)
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Text(fb["comment"], size=12, italic=True)
                            ],
                            spacing=4
                        ),
                        padding=10,
                        border_radius=8,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=ft.Colors.with_opacity(0.02, AppTheme.PRIMARY_LIGHT)
                    )
                )

            feedback_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cafeteria Reviews & Feedback", size=15, weight=ft.FontWeight.BOLD),
                        ft.Row([rating_dropdown, comment_input, feedback_btn], spacing=10),
                        ft.Divider(height=10),
                        ft.Column(feedback_cards, spacing=8)
                    ],
                    spacing=10
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )

            cafeteria_layout = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.RESTAURANT_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK, size=28),
                                            ft.Text("Campus Cafeteria & Pre-order System", size=18, weight=ft.FontWeight.BOLD),
                                        ],
                                        spacing=10
                                    ),
                                    ft.Text("Order fresh meals ahead and skip the cafeteria queue:", size=13, color=ft.Colors.GREY_500),
                                ],
                                expand=True
                            ),
                            ft.Image(
                                src="/cafeteria_3d.png",
                                width=120,
                                height=100,
                                fit="contain"
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Row([menu_column, cart_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True),
                    ft.Row([orders_container, feedback_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START)
                ],
                spacing=16,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
            return cafeteria_layout

            return assistant_layout
    # Trigger active class highlights
    switch_tab(active_tab)

    return ft.View(
        route="/student/dashboard",
        controls=[
            ft.Row(
                [
                    sidebar,
                    ft.Column(
                        [
                            header_bar,
                            content_area
                        ],
                        expand=True,
                        spacing=0
                    )
                ],
                expand=True,
                spacing=0
            )
        ],
        padding=0
    )


def build_admin_dashboard(page: ft.Page, params: dict[str, str]) -> ft.View:
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    current_email = ""
    if hasattr(page, 'router') and page.router and page.router.current_user:
        current_email = page.router.current_user.get("email", "")

    # Retrieve all student entries
    students_list = AuthService.get_all_students()

    # Tab State - persistent via page.data
    if not isinstance(page.data, dict):
        page.data = {}
    active_tab = page.data.get("active_tab_admin") or "directory"
    
    content_area = ft.Container(
        expand=True,
        padding=24,
        gradient=ft.LinearGradient(
            colors=["#0A0915", "#161233", "#0A0915"] if is_dark else ["#F8FAFC", "#EEF2F6"],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT
        )
    )

    # Left Sidebar Navigation
    logo_row = ft.Row(
        [
            ft.Image(src="/app_logo.jpg", width=32, height=32, fit="contain"),
            ft.Text("UniHub Admin", size=20, weight=ft.FontWeight.BOLD)
        ],
        spacing=10
    )

    sidebar_buttons = {}

    def switch_tab(tab_name):
        nonlocal active_tab
        active_tab = tab_name
        if isinstance(page.data, dict):
            page.data["active_tab_admin"] = tab_name
        
        for btn_name, btn in sidebar_buttons.items():
            is_active = (btn_name == tab_name)
            btn.bgcolor = (
                ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_LIGHT) if is_active and not is_dark 
                else (ft.Colors.with_opacity(0.2, AppTheme.PRIMARY_DARK) if is_active and is_dark else None)
            )
            text_color = AppTheme.PRIMARY_LIGHT if is_active and not is_dark else (AppTheme.PRIMARY_DARK if is_active and is_dark else (ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700))
            btn.content.controls[0].color = text_color
            btn.content.controls[1].color = text_color
            
        content_area.content = build_tab_content(tab_name)
        page.update()

    # Admin Header Bar Theme Toggle Function
    def toggle_dashboard_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        
        if hasattr(page, "router") and page.router:
            page.router.handle_route_change(ft.RouteChangeEvent(name="change", control=page, route=page.route))
        else:
            page.update()

    theme_toggle_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE if not is_dark else ft.Icons.LIGHT_MODE,
        icon_size=20,
        icon_color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700,
        tooltip="Toggle Dark/Light Mode",
        on_click=toggle_dashboard_theme
    )

    header_bar = ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Administration Portal", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_100 if is_dark else ft.Colors.GREY_900),
                        ft.Text("System Administration • UniHub", size=11, color=ft.Colors.GREY_500 if is_dark else ft.Colors.GREY_600)
                    ],
                    spacing=2
                ),
                ft.Row(
                    [
                        theme_toggle_btn,
                        ft.VerticalDivider(width=1, color="#334155" if is_dark else "#E2E8F0"),
                        ft.Row(
                            [
                                ft.CircleAvatar(
                                    content=ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=18, color=ft.Colors.WHITE),
                                    radius=14,
                                    bgcolor=AppTheme.PRIMARY_LIGHT
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Admin Console", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_200 if is_dark else ft.Colors.GREY_800),
                                        ft.Text(current_email, size=10, color=ft.Colors.GREY_500)
                                    ],
                                    spacing=0
                                )
                            ],
                            spacing=8
                        )
                    ],
                    spacing=16
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=12),
        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
        border=ft.Border(bottom=ft.BorderSide(1, "#334155" if is_dark else "#E2E8F0")),
        height=64
    )

    def make_sidebar_btn(icon, text, tab_name):
        btn = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700),
                    ft.Text(text, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700)
                ],
                spacing=10
            ),
            padding=ft.Padding.symmetric(vertical=12, horizontal=16),
            border_radius=10,
            on_click=lambda e: switch_tab(tab_name),

        )
        sidebar_buttons[tab_name] = btn
        return btn

    students_btn = make_sidebar_btn(ft.Icons.PEOPLE_ROUNDED, "Manage Students", "directory")
    lecturers_btn = make_sidebar_btn(ft.Icons.SUPERVISED_USER_CIRCLE_ROUNDED, "Manage Lecturers", "lecturers")
    courses_btn = make_sidebar_btn(ft.Icons.BOOK_ROUNDED, "Manage Courses", "courses")
    buses_btn = make_sidebar_btn(ft.Icons.DIRECTIONS_BUS_ROUNDED, "Manage Buses", "buses")
    attendance_btn = make_sidebar_btn(ft.Icons.CO_PRESENT_ROUNDED, "Manage Attendance", "attendance")
    notices_btn = make_sidebar_btn(ft.Icons.CAMPAIGN_ROUNDED, "Manage Notices", "notices")
    clubs_btn = make_sidebar_btn(ft.Icons.GROUPS_ROUNDED, "Manage Clubs", "clubs")
    notes_btn = make_sidebar_btn(ft.Icons.DESCRIPTION_ROUNDED, "Manage Notes", "notes")
    events_btn = make_sidebar_btn(ft.Icons.EVENT_ROUNDED, "Manage Events", "events")
    stats_btn = make_sidebar_btn(ft.Icons.ANALYTICS_ROUNDED, "Analytics Dashboard", "stats")
    assistant_btn = make_sidebar_btn(ft.Icons.SMART_TOY_ROUNDED, "AI Assistant", "assistant")

    def handle_logout(e):
        if hasattr(page, 'router') and page.router:
            page.router.clear_user_session()
            page.run_task(page.push_route, "/login")

    logout_btn = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color=ft.Colors.RED_400),
                ft.Text("Sign Out", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.RED_400)
            ],
            spacing=10
        ),
        padding=ft.Padding.symmetric(vertical=12, horizontal=16),
        border_radius=10,
        on_click=handle_logout,

    )

    sidebar = ft.Container(
        content=ft.Column(
            [
                logo_row,
                ft.Divider(height=20, color=ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_300),
                ft.Column(
                    [
                        students_btn,
                        lecturers_btn,
                        courses_btn,
                        buses_btn,
                        attendance_btn,
                        notices_btn,
                        clubs_btn,
                        notes_btn,
                        events_btn,
                        stats_btn,
                        assistant_btn,
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                    spacing=5
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                logout_btn
            ],
            spacing=8
        ),
        width=240,
        padding=16,
        bgcolor=AppTheme.SURFACE_DARK if is_dark else "#F1F5F9",
        border=ft.Border(right=ft.BorderSide(1, "#334155" if is_dark else "#E2E8F0"))
    )

    def build_tab_content(tab_name) -> ft.Control:
        nonlocal students_list
        
        # Refresh student list
        students_list = AuthService.get_all_students()

        if tab_name == "directory":
            # Search Bar
            search_input = ft.TextField(
                hint_text="Search students by name or registration number...",
                prefix_icon=ft.Icons.SEARCH_ROUNDED,
                expand=True,
                border_radius=10,
                height=45
            )

            # Build Data Rows
            data_rows = []
            
            def make_toggle_handler(student_uid):
                return lambda e: handle_toggle_status(student_uid)

            def handle_toggle_status(student_uid):
                if AuthService.toggle_student_status(student_uid):
                    page.snack_bar = ft.SnackBar(content=ft.Text("Student status updated!"), bgcolor=ft.Colors.GREEN_600)
                    page.snack_bar.open = True
                    switch_tab("directory")
                else:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Error updating status."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True

            for s in students_list:
                is_active = s.get("is_active", True)
                
                status_switch = ft.Switch(
                    value=is_active,
                    active_color=ft.Colors.GREEN_600,
                    on_change=make_toggle_handler(s.get("uid"))
                )

                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(s.get("name", "Student"))),
                        ft.DataCell(ft.Text(s.get("reg_num", "N/A"))),
                        ft.DataCell(ft.Text(s.get("faculty", "N/A").replace("Faculty of ", ""))),
                        ft.DataCell(ft.Text(s.get("department", "N/A").replace("Department of ", ""))),
                        ft.DataCell(
                            ft.Text(
                                "Active" if is_active else "Deactivated",
                                color=ft.Colors.GREEN_400 if is_active else ft.Colors.RED_400,
                                weight=ft.FontWeight.BOLD
                            )
                        ),
                        ft.DataCell(status_switch)
                    ]
                )
                data_rows.append(row)

            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Name")),
                    ft.DataColumn(ft.Text("Reg Number")),
                    ft.DataColumn(ft.Text("Faculty")),
                    ft.DataColumn(ft.Text("Department")),
                    ft.DataColumn(ft.Text("Status")),
                    ft.DataColumn(ft.Text("Deactivate Toggle")),
                ],
                rows=data_rows,
                column_spacing=24
            )

            table_container = ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.ADAPTIVE),
                expand=True,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                border_radius=12,
                padding=16,
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )

            def trigger_search(e):
                query = search_input.value.lower().strip()
                filtered_rows = []
                for s in students_list:
                    if query in s.get("name", "").lower() or query in s.get("reg_num", "").lower():
                        is_active = s.get("is_active", True)
                        row = ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(s.get("name", "Student"))),
                                ft.DataCell(ft.Text(s.get("reg_num", "N/A"))),
                                ft.DataCell(ft.Text(s.get("faculty", "N/A").replace("Faculty of ", ""))),
                                ft.DataCell(ft.Text(s.get("department", "N/A").replace("Department of ", ""))),
                                ft.DataCell(
                                    ft.Text(
                                        "Active" if is_active else "Deactivated",
                                        color=ft.Colors.GREEN_400 if is_active else ft.Colors.RED_400,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ),
                                ft.DataCell(ft.Switch(value=is_active, on_change=make_toggle_handler(s.get("uid"))))
                            ]
                        )
                        filtered_rows.append(row)
                table.rows = filtered_rows
                page.update()

            search_input.on_change = trigger_search

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PEOPLE_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Student Directory Console", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([search_input], spacing=10),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    table_container
                ],
                expand=True
            )

        elif tab_name == "lecturers":
            lecturers_list = AdminService.get_lecturers()
            name_field = ft.TextField(label="Lecturer Name", hint_text="e.g. Dr. John Smith", border_radius=8, height=45, text_size=13)
            dept_field = ft.Dropdown(
                label="Department",
                border_radius=8,
                height=45,
                options=[
                    ft.dropdown.Option("Department of Bio-Science"),
                    ft.dropdown.Option("Department of Physical Science"),
                    ft.dropdown.Option("Business Economics"),
                    ft.dropdown.Option("English Language Teaching"),
                    ft.dropdown.Option("Finance and Accountancy"),
                    ft.dropdown.Option("Human Resource Management"),
                    ft.dropdown.Option("Management and Entrepreneurship"),
                    ft.dropdown.Option("Marketing Management"),
                    ft.dropdown.Option("Project Management"),
                    ft.dropdown.Option("Department of ICT")
                ],
                value="Department of ICT"
            )
            email_field = ft.TextField(label="Email Address", hint_text="e.g. smith@vau.ac.lk", border_radius=8, height=45, text_size=13)
            desig_field = ft.TextField(label="Designation", hint_text="e.g. Senior Lecturer", border_radius=8, height=45, text_size=13)

            def add_lec(e):
                name = name_field.value.strip()
                dept = dept_field.value
                email = email_field.value.strip()
                desig = desig_field.value.strip()
                if not name or not email or not desig:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all fields."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                AdminService.add_lecturer(name, dept, email, desig)
                page.snack_bar = ft.SnackBar(content=ft.Text("Lecturer added successfully!"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("lecturers")

            def delete_lec(lid):
                AdminService.delete_lecturer(lid)
                page.snack_bar = ft.SnackBar(content=ft.Text("Lecturer removed."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("lecturers")

            lec_cards = []
            for lec in lecturers_list:
                lec_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.PERSON_PIN_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                                ft.Text(lec["name"], size=14, weight=ft.FontWeight.BOLD),
                                            ],
                                            spacing=8
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Remove Lecturer",
                                            on_click=lambda e, lid=lec["id"]: delete_lec(lid)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500)),
                                ft.Row([ft.Icon(ft.Icons.WORK_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(lec["designation"], size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.BUSINESS_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(lec["department"], size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.EMAIL_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(lec["email"], size=12)], spacing=6),
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                        width=280
                    )
                )

            cards_container = ft.Container(
                content=ft.Row(lec_cards if lec_cards else [ft.Text("No lecturers registered.", italic=True)], wrap=True, spacing=12, scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Add New Lecturer", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        name_field,
                        dept_field,
                        email_field,
                        desig_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Add Lecturer", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_lec,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SUPERVISED_USER_CIRCLE_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage University Lecturers", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([cards_container, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "courses":
            courses_list = AdminService.get_courses()
            lecturers = AdminService.get_lecturers()
            
            code_field = ft.TextField(label="Course Code", hint_text="e.g. ICT 2113", border_radius=8, height=45, text_size=13)
            name_field = ft.TextField(label="Course Name", hint_text="e.g. Object Oriented Programming", border_radius=8, height=45, text_size=13)
            dept_field = ft.Dropdown(
                label="Department",
                border_radius=8,
                height=45,
                options=[
                    ft.dropdown.Option("Department of Bio-Science"),
                    ft.dropdown.Option("Department of Physical Science"),
                    ft.dropdown.Option("Business Economics"),
                    ft.dropdown.Option("English Language Teaching"),
                    ft.dropdown.Option("Finance and Accountancy"),
                    ft.dropdown.Option("Human Resource Management"),
                    ft.dropdown.Option("Management and Entrepreneurship"),
                    ft.dropdown.Option("Marketing Management"),
                    ft.dropdown.Option("Project Management"),
                    ft.dropdown.Option("Department of ICT")
                ],
                value="Department of ICT"
            )
            credits_field = ft.Dropdown(
                label="Credits",
                border_radius=8,
                height=45,
                options=[ft.dropdown.Option("1"), ft.dropdown.Option("2"), ft.dropdown.Option("3"), ft.dropdown.Option("4")],
                value="3"
            )
            lec_options = [ft.dropdown.Option(l["name"]) for l in lecturers]
            lec_field = ft.Dropdown(
                label="Lecturer",
                border_radius=8,
                height=45,
                options=lec_options,
                value=lecturers[0]["name"] if lecturers else None
            )

            def add_course(e):
                code = code_field.value.strip().upper()
                name = name_field.value.strip()
                dept = dept_field.value
                credits = int(credits_field.value)
                lec_name = lec_field.value
                
                if not code or not name or not lec_name:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all fields."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                    
                if AdminService.add_course(code, name, dept, credits, lec_name):
                    page.snack_bar = ft.SnackBar(content=ft.Text("Course registered successfully!"), bgcolor=ft.Colors.GREEN_600)
                    page.snack_bar.open = True
                    switch_tab("courses")
                else:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Course code already exists!"), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()

            def delete_course(code):
                AdminService.delete_course(code)
                page.snack_bar = ft.SnackBar(content=ft.Text("Course deleted."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("courses")

            course_cards = []
            for c in courses_list:
                course_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text(c["code"], size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                            bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                            padding=ft.Padding.symmetric(vertical=2, horizontal=8),
                                            border_radius=8
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Remove Course",
                                            on_click=lambda e, code=c["code"]: delete_course(code)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Text(c["name"], size=13, weight=ft.FontWeight.BOLD),
                                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500)),
                                ft.Row([ft.Icon(ft.Icons.BUSINESS_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(c["department"], size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.STAR_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"{c['credits']} Credits", size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.PERSON_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(c["lecturer"], size=12)], spacing=6),
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                        width=280
                    )
                )

            cards_container = ft.Container(
                content=ft.Row(course_cards if course_cards else [ft.Text("No courses registered.", italic=True)], wrap=True, spacing=12, scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Create New Course", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        code_field,
                        name_field,
                        dept_field,
                        credits_field,
                        lec_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Create Course", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_course,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.BOOK_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage Academic Courses", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([cards_container, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "buses":
            buses_list = AdminService.get_buses()
            bus_no_field = ft.TextField(label="Bus Number", hint_text="e.g. PB-2918", border_radius=8, height=45, text_size=13)
            driver_field = ft.TextField(label="Driver Name", hint_text="e.g. S. Ramanathan", border_radius=8, height=45, text_size=13)
            route_field = ft.TextField(label="Route", hint_text="e.g. Vavuniya <-> Pampaimadu", border_radius=8, height=45, text_size=13)
            dep_field = ft.TextField(label="Departure Time", hint_text="e.g. 07:30 AM", border_radius=8, height=45, text_size=13)

            def add_bus(e):
                bno = bus_no_field.value.strip().upper()
                drv = driver_field.value.strip()
                rt = route_field.value.strip()
                dep = dep_field.value.strip()
                if not bno or not drv or not rt or not dep:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all fields."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                AdminService.add_bus(bno, drv, rt, dep)
                page.snack_bar = ft.SnackBar(content=ft.Text("Bus registered successfully!"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("buses")

            def delete_bus(bid):
                AdminService.delete_bus(bid)
                page.snack_bar = ft.SnackBar(content=ft.Text("Bus removed."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("buses")

            def change_status(bid, status):
                AdminService.update_bus_status(bid, status)
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Bus status updated to {status}"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("buses")

            bus_cards = []
            for b in buses_list:
                status_dropdown = ft.Dropdown(
                    options=[
                        ft.dropdown.Option("On Time"),
                        ft.dropdown.Option("Delayed"),
                        ft.dropdown.Option("Cancelled")
                    ],
                    value=b["status"],
                    width=120,
                    height=35,
                    text_size=11,
                    content_padding=5,
                    border_radius=6
                )
                status_dropdown.on_change = lambda e, bid=b["id"]: change_status(bid, e.control.value)

                bus_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.DIRECTIONS_BUS_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                                ft.Text(b["bus_no"], size=14, weight=ft.FontWeight.BOLD),
                                            ],
                                            spacing=8
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Remove Bus",
                                            on_click=lambda e, bid=b["id"]: delete_bus(bid)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500)),
                                ft.Row([ft.Icon(ft.Icons.ROUTE_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(b["route"], size=12, weight=ft.FontWeight.W_500)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.PERSON_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"Driver: {b['driver']}", size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"Departs: {b['departure']}", size=12)], spacing=6),
                                ft.Row(
                                    [
                                        ft.Text("Status:", size=12, weight=ft.FontWeight.BOLD),
                                        status_dropdown
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                        width=280
                    )
                )

            cards_container = ft.Container(
                content=ft.Row(bus_cards if bus_cards else [ft.Text("No buses registered.", italic=True)], wrap=True, spacing=12, scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Register New Bus", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        bus_no_field,
                        driver_field,
                        route_field,
                        dep_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Add Bus", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_bus,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DIRECTIONS_BUS_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage University Transport", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([cards_container, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "attendance":
            students = AuthService.get_all_students()
            student_options = []
            for s in students:
                student_options.append(ft.dropdown.Option(key=s["uid"], text=f"{s['name']} ({s['reg_num']})"))
                
            selected_student_uid = page.data.get("attendance_edit_student_uid", None)
            
            if not selected_student_uid and students:
                selected_student_uid = students[0]["uid"]
                page.data["attendance_edit_student_uid"] = selected_student_uid
                
            student_dropdown = ft.Dropdown(
                label="Select Student to Edit",
                options=student_options,
                value=selected_student_uid,
                width=350,
                border_radius=8,
                height=48
            )
            student_dropdown.on_change = lambda e: (page.data.update({"attendance_edit_student_uid": e.control.value}), switch_tab("attendance"))
            
            attendance_detail = ft.Column(spacing=12, expand=True)
            
            if selected_student_uid:
                student_attendance = AttendanceService.get_attendance(selected_student_uid)
                overall_percent = AttendanceService.calculate_percentage(student_attendance)
                
                status_text = "Good Standing" if overall_percent >= 75.0 else "At Risk"
                status_color = ft.Colors.GREEN_600 if overall_percent >= 75.0 else ft.Colors.RED_600
                
                overall_banner = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Overall Attendance Percentage:", size=13),
                            ft.Text(f"{overall_percent:.1f}%", size=20, weight=ft.FontWeight.BOLD, color=status_color),
                            ft.Container(
                                content=ft.Text(status_text, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=status_color,
                                padding=ft.Padding.symmetric(vertical=4, horizontal=10),
                                border_radius=15
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=16,
                    border_radius=10,
                    border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                    bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
                )
                attendance_detail.controls.append(overall_banner)
                
                rows = []
                
                def save_subj_attendance(subject, att_field, tot_field):
                    try:
                        att = int(att_field.value)
                        tot = int(tot_field.value)
                        if att < 0 or tot < 0 or att > tot:
                            page.snack_bar = ft.SnackBar(content=ft.Text("Attended sessions cannot exceed total sessions or be negative!"), bgcolor=ft.Colors.RED_600)
                            page.snack_bar.open = True
                            page.update()
                            return
                        AttendanceService.update_attendance(selected_student_uid, subject, att, tot)
                        page.snack_bar = ft.SnackBar(content=ft.Text(f"Updated {subject} attendance successfully!"), bgcolor=ft.Colors.GREEN_600)
                        page.snack_bar.open = True
                        switch_tab("attendance")
                    except ValueError:
                        page.snack_bar = ft.SnackBar(content=ft.Text("Please enter valid integers."), bgcolor=ft.Colors.RED_600)
                        page.snack_bar.open = True
                        page.update()

                for subject, (attended, total) in student_attendance.items():
                    att_input = ft.TextField(value=str(attended), width=60, height=35, text_size=12, text_align=ft.TextAlign.CENTER, border_radius=6, content_padding=5)
                    tot_input = ft.TextField(value=str(total), width=60, height=35, text_size=12, text_align=ft.TextAlign.CENTER, border_radius=6, content_padding=5)
                    
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(subject, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(att_input),
                            ft.DataCell(tot_input),
                            ft.DataCell(ft.Text(f"{(attended/total*100):.1f}%" if total > 0 else "0.0%")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.SAVE_ROUNDED,
                                    icon_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                    on_click=lambda e, s=subject, a=att_input, t=tot_input: save_subj_attendance(s, a, t)
                                )
                            )
                        ]
                    )
                    rows.append(row)
                    
                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Subject/Module")),
                        ft.DataColumn(ft.Text("Attended")),
                        ft.DataColumn(ft.Text("Total")),
                        ft.DataColumn(ft.Text("Percentage")),
                        ft.DataColumn(ft.Text("Action"))
                    ],
                    rows=rows,
                    column_spacing=16
                )
                
                table_container = ft.Container(
                    content=ft.Column([table], scroll=ft.ScrollMode.ADAPTIVE),
                    border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                    border_radius=12,
                    padding=16,
                    bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                    expand=True
                )
                attendance_detail.controls.append(table_container)
            else:
                attendance_detail.controls.append(ft.Text("No students found in registry.", italic=True, color=ft.Colors.GREY_500))

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CO_PRESENT_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage Student Attendance", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    student_dropdown,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    attendance_detail
                ],
                expand=True
            )

        elif tab_name == "notices":
            notices_list = AdminService.get_notices()
            title_field = ft.TextField(label="Notice Title", hint_text="e.g. Exam Schedule", border_radius=8, height=45, text_size=13)
            cat_field = ft.Dropdown(
                label="Category",
                border_radius=8,
                height=45,
                options=[
                    ft.dropdown.Option("Academic"),
                    ft.dropdown.Option("Exams"),
                    ft.dropdown.Option("Sports"),
                    ft.dropdown.Option("General")
                ],
                value="Academic"
            )
            content_field = ft.TextField(label="Notice Content", hint_text="Write announcement body here...", multiline=True, min_lines=3, max_lines=5, border_radius=8, text_size=13)

            def add_notice(e):
                title = title_field.value.strip()
                cat = cat_field.value
                content = content_field.value.strip()
                
                if not title or not content:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in notice title and content."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                AdminService.add_notice(title, content, cat)
                page.snack_bar = ft.SnackBar(content=ft.Text("Notice published successfully!"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("notices")

            def delete_notice(nid):
                AdminService.delete_notice(nid)
                page.snack_bar = ft.SnackBar(content=ft.Text("Notice removed."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("notices")

            notice_cards = []
            for n in notices_list:
                notice_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text(n["category"], size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                            bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                            padding=ft.Padding.symmetric(vertical=2, horizontal=8),
                                            border_radius=10
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            icon_color=ft.Colors.RED_400,
                                            icon_size=18,
                                            on_click=lambda e, nid=n["id"]: delete_notice(nid)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Text(n["title"], size=14, weight=ft.FontWeight.BOLD),
                                ft.Text(n["content"], size=12, color=ft.Colors.GREY_300 if is_dark else ft.Colors.GREY_700),
                                ft.Text(f"Published on: {n['date']}", size=10, italic=True, color=ft.Colors.GREY_500)
                            ],
                            spacing=6
                        ),
                        padding=12,
                        border_radius=8,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                        width=280
                    )
                )

            cards_row = ft.Row(notice_cards, wrap=True, spacing=16, scroll=ft.ScrollMode.ADAPTIVE, expand=True)

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Publish New Announcement", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        title_field,
                        cat_field,
                        content_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Publish Notice", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_notice,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CAMPAIGN_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage Notice Board", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([cards_row, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "clubs":
            clubs_list = ClubService.get_clubs()
            name_field = ft.TextField(label="Club Name", hint_text="e.g. IEEE Student Branch", border_radius=8, height=45, text_size=13)
            desc_field = ft.TextField(label="Description", hint_text="e.g. Advancing technology...", multiline=True, min_lines=2, max_lines=4, border_radius=8, text_size=13)

            def add_club(e):
                name = name_field.value.strip()
                desc = desc_field.value.strip()
                if not name or not desc:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in club name and description."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                ClubService.add_club(name, desc)
                page.snack_bar = ft.SnackBar(content=ft.Text("Club registered successfully!"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("clubs")

            def delete_club(cid):
                ClubService.delete_club(cid)
                page.snack_bar = ft.SnackBar(content=ft.Text("Club removed."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("clubs")

            club_rows = []
            for club in clubs_list:
                club_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(club["name"], weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(club["description"], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)),
                            ft.DataCell(ft.Text(f"{len(club['members'])} Members")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_color=ft.Colors.RED_400,
                                    on_click=lambda e, cid=club["id"]: delete_club(cid)
                                )
                            )
                        ]
                    )
                )

            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Club Name")),
                    ft.DataColumn(ft.Text("Description")),
                    ft.DataColumn(ft.Text("Members")),
                    ft.DataColumn(ft.Text("Actions"))
                ],
                rows=club_rows,
                column_spacing=16
            )

            table_container = ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.ADAPTIVE),
                expand=True,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                border_radius=12,
                padding=16,
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Register New Club", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        name_field,
                        desc_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Register Club", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_club,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.GROUPS_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage Campus Clubs", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([table_container, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "notes":
            notes_list = AdminService.get_notes()
            courses = AdminService.get_courses()
            lecturers = AdminService.get_lecturers()
            
            title_field = ft.TextField(label="Note Title", hint_text="e.g. OOP Lecture 1", border_radius=8, height=45, text_size=13)
            
            course_options = [ft.dropdown.Option(c["name"]) for c in courses]
            subject_field = ft.Dropdown(
                label="Subject/Course",
                border_radius=8,
                height=45,
                options=course_options,
                value=courses[0]["name"] if courses else None
            )
            
            link_field = ft.TextField(label="File Link (URL)", hint_text="e.g. https://vau.ac.lk/notes/oop.pdf", border_radius=8, height=45, text_size=13)
            
            lec_options = [ft.dropdown.Option(l["name"]) for l in lecturers]
            uploader_field = ft.Dropdown(
                label="Uploaded By",
                border_radius=8,
                height=45,
                options=lec_options,
                value=lecturers[0]["name"] if lecturers else None
            )

            def add_note(e):
                title = title_field.value.strip()
                subject = subject_field.value
                link = link_field.value.strip()
                uploader = uploader_field.value
                
                if not title or not subject or not link or not uploader:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all fields."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                AdminService.add_note(title, subject, link, uploader)
                page.snack_bar = ft.SnackBar(content=ft.Text("Note uploaded successfully!"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("notes")

            def delete_note(nid):
                AdminService.delete_note(nid)
                page.snack_bar = ft.SnackBar(content=ft.Text("Note removed."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("notes")

            note_cards = []
            for n in notes_list:
                note_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.NOTE_ALT_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                                ft.Text(n["title"], size=14, weight=ft.FontWeight.BOLD, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=160),
                                            ],
                                            spacing=8
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Remove Note",
                                            on_click=lambda e, nid=n["id"]: delete_note(nid)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500)),
                                ft.Row([ft.Icon(ft.Icons.BOOK_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(n["subject"], size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.PERSON_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"Uploaded: {n['uploaded_by']}", size=12)], spacing=6),
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Icon(ft.Icons.LINK_ROUNDED, size=14, color=ft.Colors.BLUE_400 if is_dark else ft.Colors.BLUE_800),
                                            ft.Text("Open Note File", size=12, color=ft.Colors.BLUE_400 if is_dark else ft.Colors.BLUE_800, weight=ft.FontWeight.BOLD),
                                        ],
                                        spacing=6,
                                    ),
                                    on_click=lambda e, url=n["file_link"]: page.launch_url(url)
                                )
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                        width=280
                    )
                )

            cards_container = ft.Container(
                content=ft.Row(note_cards if note_cards else [ft.Text("No lecture notes uploaded.", italic=True)], wrap=True, spacing=12, scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Upload Course Note", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        title_field,
                        subject_field,
                        link_field,
                        uploader_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Upload Note", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_note,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Manage Lecture Notes", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([cards_container, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "events":
            events_list = ClubService.get_events()
            clubs = ClubService.get_clubs()
            
            title_field = ft.TextField(label="Event Title", hint_text="e.g. ACM Music Night", border_radius=8, height=45, text_size=13)
            desc_field = ft.TextField(label="Description", hint_text="e.g. Acoustic session...", multiline=True, min_lines=2, max_lines=4, border_radius=8, text_size=13)
            date_field = ft.TextField(label="Date (YYYY-MM-DD)", hint_text="e.g. 2026-07-25", border_radius=8, height=45, text_size=13)
            time_field = ft.TextField(label="Time", hint_text="e.g. 06:00 PM", border_radius=8, height=45, text_size=13)
            loc_field = ft.TextField(label="Location", hint_text="e.g. Main Auditorium", border_radius=8, height=45, text_size=13)
            
            club_options = [ft.dropdown.Option(c["name"]) for c in clubs]
            club_field = ft.Dropdown(
                label="Host Club",
                border_radius=8,
                height=45,
                options=club_options,
                value=clubs[0]["name"] if clubs else None
            )

            def add_event(e):
                title = title_field.value.strip()
                desc = desc_field.value.strip()
                edate = date_field.value.strip()
                etime = time_field.value.strip()
                eloc = loc_field.value.strip()
                eclub = club_field.value
                
                if not title or not desc or not edate or not etime or not eloc or not eclub:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all fields."), bgcolor=ft.Colors.RED_600)
                    page.snack_bar.open = True
                    page.update()
                    return
                ClubService.add_event(title, desc, edate, etime, eloc, eclub)
                page.snack_bar = ft.SnackBar(content=ft.Text("Event scheduled successfully!"), bgcolor=ft.Colors.GREEN_600)
                page.snack_bar.open = True
                switch_tab("events")

            def delete_event(eid):
                ClubService.delete_event(eid)
                page.snack_bar = ft.SnackBar(content=ft.Text("Event cancelled/deleted."), bgcolor=ft.Colors.GREY_700)
                page.snack_bar.open = True
                switch_tab("events")

            event_cards = []
            for ev in events_list:
                event_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.EVENT_AVAILABLE_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                                                ft.Text(ev["title"], size=14, weight=ft.FontWeight.BOLD, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=160),
                                            ],
                                            spacing=8
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Remove Event",
                                            on_click=lambda e, eid=ev["id"]: delete_event(eid)
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=1, color=ft.Colors.with_opacity(0.1, ft.Colors.GREY_500)),
                                ft.Row([ft.Icon(ft.Icons.GROUPS_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"Host: {ev['club']}", size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"{ev['date']} @ {ev['time']}", size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.LOCATION_ON_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(ev["location"], size=12)], spacing=6),
                                ft.Row([ft.Icon(ft.Icons.PEOPLE_ROUNDED, size=14, color=ft.Colors.GREY_500), ft.Text(f"{len(ev['registered_users'])} Registered Users", size=12, weight=ft.FontWeight.BOLD)], spacing=6),
                            ],
                            spacing=8
                        ),
                        padding=12,
                        border_radius=10,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                        width=280
                    )
                )

            cards_container = ft.Container(
                content=ft.Row(event_cards if event_cards else [ft.Text("No events scheduled.", italic=True)], wrap=True, spacing=12, scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )

            form_container = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Schedule Club Event", size=15, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        title_field,
                        club_field,
                        desc_field,
                        date_field,
                        time_field,
                        loc_field,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.FilledButton(
                            content=ft.Text("Create Event", color=ft.Colors.WHITE),
                            style=ft.ButtonStyle(
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=add_event,
                            width=220
                        )
                    ],
                    spacing=8
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE,
                width=260
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.EVENT_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("Schedule Club Events", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Row([cards_container, form_container], spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
                ],
                expand=True
            )

        elif tab_name == "stats":
            total_students = len(students_list)
            active_count = sum(1 for s in students_list if s.get("is_active", True))
            deactive_count = total_students - active_count
            
            # Faculty counts
            fac_counts = {}
            for s in students_list:
                fac = s.get("faculty", "Other").replace("Faculty of ", "")
                fac_counts[fac] = fac_counts.get(fac, 0) + 1

            stat_total = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Total Registered", size=12, color=ft.Colors.GREY_500),
                        ft.Text(str(total_students), size=28, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=2
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                expand=True
            )

            stat_active = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Active Portals", size=12, color=ft.Colors.GREY_500),
                        ft.Text(str(active_count), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400 if is_dark else ft.Colors.GREEN_700),
                    ],
                    spacing=2
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                expand=True
            )

            stat_deactive = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Deactivated Portals", size=12, color=ft.Colors.GREY_500),
                        ft.Text(str(deactive_count), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400 if is_dark else ft.Colors.RED_700),
                    ],
                    spacing=2
                ),
                padding=16,
                border_radius=12,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                expand=True
            )

            stats_row = ft.Row([stat_total, stat_active, stat_deactive], spacing=16)

            # Draw simple bar chart for Faculty Distribution
            chart_bars = []
            max_val = max(fac_counts.values()) if fac_counts else 1
            
            for fac, count in fac_counts.items():
                height_val = (count / max_val) * 150
                bar = ft.Column(
                    [
                        ft.Container(
                            content=ft.Text(str(count), size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            width=60,
                            height=height_val,
                            border_radius=6,
                            gradient=ft.LinearGradient(
                                colors=[AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK, "#0F766E"],
                                begin=ft.Alignment.BOTTOM_CENTER,
                                end=ft.Alignment.TOP_CENTER
                            ),
                            alignment=ft.Alignment.TOP_CENTER,
                            padding=ft.Padding.only(top=5)
                        ),
                        ft.Text(fac.replace("Studies", "Stud.").replace("Science", "Sci."), size=10, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER, width=80)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
                chart_bars.append(bar)

            chart_row = ft.Container(
                content=ft.Row(
                    chart_bars,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.END
                ),
                padding=20,
                height=220,
                border=ft.Border(bottom=ft.BorderSide(2, "#334155" if is_dark else "#CBD5E1")),
                margin=ft.Margin.only(bottom=10)
            )

            chart_card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Faculty Distribution Overview", size=16, weight=ft.FontWeight.BOLD),
                        chart_row
                    ],
                    spacing=12
                ),
                padding=24,
                border_radius=16,
                border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                bgcolor=AppTheme.SURFACE_DARK if is_dark else ft.Colors.WHITE
            )

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.BAR_CHART_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("System Metrics Panel", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    stats_row,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    chart_card
                ],
                spacing=16
            )

        elif tab_name == "assistant":
            # Conversation Box
            chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
            
            # Initial bot greeting
            chat_list.controls.append(
                ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=16, color=ft.Colors.WHITE),
                            radius=16,
                            bgcolor=ft.Colors.BLUE_GREY_600 if is_dark else ft.Colors.BLUE_GREY_400
                        ),
                        ft.Container(
                            content=ft.Markdown(BotService._get_mock_reply("hello", is_admin=True), selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                            bgcolor=ft.Colors.GREY_200 if not is_dark else "#1E293B",
                            padding=12,
                            border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_right=12),
                            width=500
                        )
                    ],
                    spacing=10
                )
            )

            chat_input = ft.TextField(
                hint_text="Ask me about administration portal controls...",
                expand=True,
                border_radius=10,
                height=50,
                on_submit=lambda e: send_message(e)
            )

            def send_message(e):
                user_msg = chat_input.value.strip()
                if not user_msg:
                    return
                    
                # 1. Append user bubble
                chat_list.controls.append(
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(user_msg, size=13, color=ft.Colors.WHITE),
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                                padding=12,
                                border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_left=12),
                                width=400
                            ),
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.WHITE),
                                radius=16,
                                bgcolor=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=10
                    )
                )
                
                chat_input.value = ""
                page.update()
                
                # Show typing indicator
                typing_indicator = ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=16, color=ft.Colors.WHITE),
                            radius=16,
                            bgcolor=ft.Colors.BLUE_GREY_600 if is_dark else ft.Colors.BLUE_GREY_400
                        ),
                        ft.Container(
                            content=ft.Text("UniHub Assistant is typing...", size=13, italic=True, color=ft.Colors.GREY_500),
                            bgcolor=ft.Colors.GREY_200 if not is_dark else "#1E293B",
                            padding=12,
                            border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_right=12)
                        )
                    ],
                    spacing=10
                )
                chat_list.controls.append(typing_indicator)
                page.update()
                
                time.sleep(0.5)
                
                # 2. Query bot response
                bot_reply = BotService.get_reply(user_msg, is_admin=True)
                
                # Remove typing indicator
                chat_list.controls.remove(typing_indicator)
                
                # 3. Append bot bubble
                chat_list.controls.append(
                    ft.Row(
                        [
                            ft.CircleAvatar(
                                content=ft.Icon(ft.Icons.SMART_TOY_ROUNDED, size=16, color=ft.Colors.WHITE),
                                radius=16,
                                bgcolor=ft.Colors.BLUE_GREY_600 if is_dark else ft.Colors.BLUE_GREY_400
                            ),
                            ft.Container(
                                content=ft.Markdown(bot_reply, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                                bgcolor=ft.Colors.GREY_200 if not is_dark else "#1E293B",
                                padding=12,
                                border_radius=ft.BorderRadius.only(top_left=12, top_right=12, bottom_right=12),
                                width=500
                            )
                        ],
                        spacing=10
                    )
                )
                page.update()

            send_btn = ft.IconButton(
                icon=ft.Icons.SEND_ROUNDED,
                icon_color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK,
                on_click=send_message
            )

            def on_chip_click(text):
                chat_input.value = text
                send_message(None)

            suggestion_chips = ft.Row(
                [
                    ft.Container(
                        content=ft.Text(label, size=12, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                        bgcolor=ft.Colors.with_opacity(0.1, AppTheme.PRIMARY_LIGHT) if not is_dark else ft.Colors.with_opacity(0.15, AppTheme.PRIMARY_DARK),
                        padding=ft.Padding.symmetric(vertical=6, horizontal=12),
                        border_radius=15,
                        on_click=lambda e, val=label: on_chip_click(val)
                    )
                    for label in ["Deactivate portal", "System statistics", "Faculties info"]
                ],
                spacing=10,
                wrap=True
            )

            assistant_layout = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SMART_TOY_ROUNDED, color=AppTheme.PRIMARY_LIGHT if not is_dark else AppTheme.PRIMARY_DARK),
                            ft.Text("UniHub Admin Assistant", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=10
                    ),
                    ft.Text("Your smart administrative companion powered by Gemini.", size=12, color=ft.Colors.GREY_500),
                    ft.Divider(height=10),
                    ft.Container(
                        content=chat_list,
                        expand=True,
                        padding=12,
                        border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
                        border_radius=12,
                        bgcolor=AppTheme.SURFACE_DARK if is_dark else "#F8FAFC"
                    ),
                    suggestion_chips,
                    ft.Row([chat_input, send_btn], spacing=10)
                ],
                expand=True
            )
            return assistant_layout

        return ft.Text("Tab not found.")

    content_area.content = build_tab_content(active_tab)
    switch_tab(active_tab)

    return ft.View(
        route="/admin/dashboard",
        controls=[
            ft.Row(
                [
                    sidebar,
                    ft.Column(
                        [
                            header_bar,
                            content_area
                        ],
                        expand=True,
                        spacing=0
                    )
                ],
                expand=True,
                spacing=0
            )
        ],
        padding=0
    )
