import flet as ft

def main(page: ft.Page):
    faculty_departments = {
        "Faculty of Applied Science": ["Department of Bio-Science", "Department of Physical Science"],
        "Faculty of Business Studies": ["Business Economics", "English Language Teaching"]
    }
    
    faculty_dropdown = ft.Dropdown(
        label="Faculty",
        options=[ft.dropdown.Option(fac) for fac in faculty_departments.keys()],
    )
    
    department_dropdown = ft.Dropdown(
        label="Department",
        disabled=True,
    )
    
    def handle_faculty_change(e):
        selected_faculty = faculty_dropdown.value
        department_dropdown.options.clear()
        if selected_faculty in faculty_departments:
            depts = faculty_departments[selected_faculty]
            for dept in depts:
                department_dropdown.options.append(ft.dropdown.Option(dept))
            department_dropdown.disabled = False
            department_dropdown.value = depts[0]
        else:
            department_dropdown.disabled = True
            department_dropdown.value = None
        department_dropdown.update()
        page.update()
        
    faculty_dropdown.on_change = handle_faculty_change
    page.add(faculty_dropdown, department_dropdown)

ft.app(target=main)
