import flet as ft
from services.auth_service import AuthService
from utils.validators import Validators

class AuthController:
    @classmethod
    def login(cls, page: ft.Page, email: str, password: str, error_text: ft.Text, progress_bar: ft.ProgressBar):
        """
        Coordinates user sign in, error display, and redirection.
        """
        # Validate inputs
        if not Validators.is_non_empty(email) or not Validators.is_non_empty(password):
            error_text.value = "Please enter both email and password."
            page.update()
            return
            
        if not Validators.is_valid_email(email):
            error_text.value = "Invalid email format."
            page.update()
            return
            
        # Start Progress UI
        progress_bar.visible = True
        error_text.value = ""
        page.update()
        
        try:
            # Perform Authentication
            session = AuthService.sign_in(email, password)
            
            # Setup session in router
            if hasattr(page, 'router') and page.router:
                page.router.set_user_session(session)
                
                # Navigate depending on role
                role = session.get("role", "student").lower()
                if role == "administrator":
                    page.run_task(page.push_route, "/admin/dashboard")
                else:
                    page.run_task(page.push_route, "/student/dashboard")
            else:
                error_text.value = "Router is not initialized correctly."
                
        except Exception as ex:
            error_text.value = str(ex)
        finally:
            # End Progress UI
            progress_bar.visible = False
            page.update()

    @classmethod
    def register(cls, page: ft.Page, email: str, password: str, confirm_password: str, reg_num: str, 
                 name: str, faculty: str, department: str, error_text: ft.Text, progress_bar: ft.ProgressBar):
        """
        Coordinates student registration, form validation, and database entry.
        """
        # Validate empty fields (department is optional if faculty is set)
        required = [email, password, confirm_password, reg_num, name, faculty]
        if not all(Validators.is_non_empty(f) for f in required):
            error_text.value = "All fields are required. Please fill in all entries."
            page.update()
            return
            
        # Validate Email format (allow any valid email)
        if not Validators.is_valid_email(email):
            error_text.value = "Please enter a valid email address."
            page.update()
            return
            
        # Validate Reg Number format
        if not Validators.is_valid_registration_number(reg_num):
            error_text.value = "Invalid Registration Number format. Use YYYY/FAC/ID (e.g. 2021/ICT/80)."
            page.update()
            return
            
        # Validate password strength
        is_strong, pwd_msg = Validators.is_valid_password(password)
        if not is_strong:
            error_text.value = pwd_msg
            page.update()
            return
            
        # Validate password match
        if password != confirm_password:
            error_text.value = "Passwords do not match."
            page.update()
            return
            
        # Start Progress UI
        progress_bar.visible = True
        error_text.value = ""
        page.update()
        
        try:
            # Execute sign up
            session = AuthService.sign_up(
                email=email,
                password=password,
                reg_num=reg_num,
                name=name,
                faculty=faculty,
                department=department
            )
            
            # Setup session in router
            if hasattr(page, 'router') and page.router:
                page.router.set_user_session(session)
                
                # Navigate to student dashboard
                page.run_task(page.push_route, "/student/dashboard")
                
                # Show success notification
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Account created successfully! Welcome to UniHub."),
                    bgcolor=ft.Colors.GREEN_600
                )
                page.snack_bar.open = True
            else:
                error_text.value = "Router is not initialized correctly."
                
        except Exception as ex:
            error_text.value = str(ex)
        finally:
            progress_bar.visible = False
            page.update()

    @classmethod
    def reset_password(cls, page: ft.Page, email: str, error_text: ft.Text, success_text: ft.Text, progress_bar: ft.ProgressBar):
        """
        Coordinates password recovery.
        """
        if not Validators.is_non_empty(email):
            error_text.value = "Please enter your email address."
            success_text.value = ""
            page.update()
            return
            
        if not Validators.is_valid_email(email):
            error_text.value = "Invalid email format."
            success_text.value = ""
            page.update()
            return
            
        # Start progress
        progress_bar.visible = True
        error_text.value = ""
        success_text.value = ""
        page.update()
        
        try:
            AuthService.reset_password(email)
            success_text.value = "A password reset email has been sent! Check your inbox."
        except Exception as ex:
            error_text.value = str(ex)
        finally:
            progress_bar.visible = False
            page.update()
