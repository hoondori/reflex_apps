import reflex as rx

from ..navigation import routes


def navbar_link(text:str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )

def navbar_desktop_logo() -> rx.Component:
    return rx.hstack(
        rx.link(rx.image(src="/logo.jpg", width="2.25em", height="auto", border_radius="25%"),href=routes.HOME),
        rx.link(rx.heading("Reflex", size="7", weight="bold"), href=routes.HOME),
        align_items="center"
    )

def navbar_mobile_logo() -> rx.Component:
    return rx.hstack(
        rx.image(src="/logo.jpg", width="2em", height="auto", border_radius="25%"),
        rx.heading("Reflex", size="6", weight="bold"),
        align_items="center"
    )

def navbar_desktop_menu() -> rx.Component:
    return rx.hstack(
        navbar_link("Home", routes.HOME),
        navbar_link("About", routes.ABOUT),
        navbar_link("Blog", routes.BLOG),        
        navbar_link("Pricing", routes.PRICING),
        navbar_link("Contact", routes.CONTACT_US),
        spacing="5",
    )

def navbar_mobile_menu() -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.icon("menu", size=30)
        ),
        rx.menu.content(
            rx.menu.item("Home", on_click=rx.redirect(routes.HOME)),
            rx.menu.item("About", on_click=rx.redirect(routes.ABOUT)),
            rx.menu.item("Blog", on_click=rx.redirect(routes.BLOG)),
            rx.menu.item("Pricing", on_click=rx.redirect(routes.PRICING)),
            rx.menu.item("Contact", on_click=rx.redirect(routes.CONTACT_US)),
            rx.menu.separator(),
            rx.menu.item("Log in"),
            rx.menu.item("Sign up"),
        ),
        justify="end",
    )

def navbar_auth() -> rx.Component:
    return rx.hstack(
        rx.button("Sign Up", size="3", variant="outline"),
        rx.button("Log In", size="3"),
        spacing="4",
        justify="end"
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                navbar_desktop_logo(),
                navbar_desktop_menu(),
                navbar_auth(),
                justify="between",
                align_items="center"
            )
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                navbar_mobile_logo(),
                navbar_mobile_menu(),
                justify="between",
                align_items="center"
            ),
        ),
        bg=rx.Color("accent", 3),
        padding="1em",
        width="100%"
    )