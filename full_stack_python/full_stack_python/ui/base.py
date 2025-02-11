import reflex as rx

from .nav import navbar
from .dashboard import base_dashboard_page
from ..auth.state import SessionState

def base_layout_componenet(child:rx.Component, *args, **kwargs) -> rx.Component:
    return rx.fragment( # renders nada
        navbar(),
        rx.box(
            child,
            padding="1em",
            width="100%"
        ),
        rx.logo(),
        rx.color_mode.button(position="top-right"),
        padding="10em"
    )

def base_page(child:rx.Component, *args, **kwargs) -> rx.Component:
    if not isinstance(child, rx.Component):
        child = rx.heading("This is not valid child element")
     
    # show sidebar if logged-in, otherwise show navbar
    return rx.cond(
        SessionState.is_authenticated,
        base_dashboard_page(child, args, kwargs),
        base_layout_componenet(child, args, kwargs),
    )


