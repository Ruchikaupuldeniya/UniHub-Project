import flet as ft

class AppTheme:
    # Premium Material 3 Color Palette - Vavuniya University Accents
    # Royal Blue, Teal, and Warm Amber Gold
    
    PRIMARY_LIGHT = "#670047"      # University of Vavuniya Maroon
    PRIMARY_DARK = "#FF8DA1"       # Soft Rose/Maroon for Dark Mode readability
    
    SECONDARY_LIGHT = "#FFCB00"    # University of Vavuniya Gold Accent
    SECONDARY_DARK = "#FFE082"     # Soft Gold for Dark Mode
    
    TERTIARY_LIGHT = "#0F766E"     # Teal auxiliary
    TERTIARY_DARK = "#2DD4BF"      # Light Teal
    
    BG_LIGHT = "#F8FAFC"           # Slate-50 Background
    BG_DARK = "#0F172A"            # Slate-900 Background
    
    SURFACE_LIGHT = "#FFFFFF"      # White surface
    SURFACE_DARK = "#1E293B"       # Slate-800 Surface
    
    TEXT_LIGHT = "#0F172A"         # Dark Slate
    TEXT_DARK = "#F8FAFC"          # Off White

    @classmethod
    def get_light_theme(cls) -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=cls.PRIMARY_LIGHT,
                secondary=cls.SECONDARY_LIGHT,
                tertiary=cls.TERTIARY_LIGHT,
                surface=cls.SURFACE_LIGHT,
                on_primary="#FFFFFF",
                on_secondary="#FFFFFF",
                on_surface=cls.TEXT_LIGHT,
                outline="#CBD5E1",  # Slate-300
                shadow="#000000",
                error="#EF4444"
            ),
            visual_density=ft.VisualDensity.COMFORTABLE,
            page_transitions=ft.PageTransitionsTheme(
                android=ft.PageTransitionTheme.FADE_UPWARDS,
                ios=ft.PageTransitionTheme.CUPERTINO,
                windows=ft.PageTransitionTheme.ZOOM,
                macos=ft.PageTransitionTheme.ZOOM
            )
        )

    @classmethod
    def get_dark_theme(cls) -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=cls.PRIMARY_DARK,
                secondary=cls.SECONDARY_DARK,
                tertiary=cls.TERTIARY_DARK,
                surface=cls.SURFACE_DARK,
                on_primary="#0F172A",
                on_secondary="#0F172A",
                on_surface=cls.TEXT_DARK,
                outline="#475569",  # Slate-600
                shadow="#000000",
                error="#F87171"
            ),
            visual_density=ft.VisualDensity.COMFORTABLE,
            page_transitions=ft.PageTransitionsTheme(
                android=ft.PageTransitionTheme.FADE_UPWARDS,
                ios=ft.PageTransitionTheme.CUPERTINO,
                windows=ft.PageTransitionTheme.ZOOM,
                macos=ft.PageTransitionTheme.ZOOM
            )
        )
        
    @classmethod
    def get_card_decoration(cls, is_dark: bool) -> ft.BoxDecoration:
        """
        Returns a premium Box Decoration (glassmorphism/subtle shadows) for custom cards
        """
        return ft.BoxDecoration(
            color=cls.SURFACE_DARK if is_dark else cls.SURFACE_LIGHT,
            border_radius=ft.BorderRadius.all(12),
            border=ft.Border.all(1, "#334155" if is_dark else "#E2E8F0"),
            shadows=[
                ft.BoxShadow(
                    blur_radius=10,
                    color="#000000" if is_dark else "#E2E8F0",
                    offset=ft.Offset(0, 4)
                )
            ]
        )
