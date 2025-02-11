import reflex as rx

from .sidebar import sidebar

def base_dashboard_page(child:rx.Component, *args, **kwargs) -> rx.Component:
    if not isinstance(child, rx.Component):
        child = rx.heading("This is not valid child element")      
    else:
        return rx.container(
            rx.hstack(
                sidebar(),
                rx.box(
                    child,
                    rx.logo(),
                    padding="1em",
                    width="100%",
                )
            ),     
            rx.color_mode.button(position="top-right"),
        )

