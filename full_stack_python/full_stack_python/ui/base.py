import reflex as rx

from .nav import navbar_buttons

def base_page(child:rx.Component, hide_navbar=False, *args, **kwargs) -> rx.Component:
    if not isinstance(child, rx.Component):
        child = rx.heading("This is not valid child element")
    if hide_navbar:
        return rx.container(
            child,
            rx.logo(),
            rx.color_mode.button(position="bottom-left"),
        )        
    else:
        return rx.container(
            navbar_buttons(),
            child,
            rx.logo(),
            rx.color_mode.button(position="bottom-left"),
        )

