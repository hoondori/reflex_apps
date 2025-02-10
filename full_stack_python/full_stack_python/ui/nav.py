import reflex as rx


def navbar_link(text:str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )

def navbar_logo() -> rx.Component:
    return rx.hstack(
        rx.image(src="/logo.jpg", width="2.25em", height="auto", border_radius="25%"),
        rx.heading("Reflex", size="7", weight="bold"),
        align_items="center"
    )

def navbar_menu() -> rx.Component:
    return rx.hstack(
        navbar_link("Home", "/#"),
        navbar_link("About", "/#"),
        navbar_link("Pricing", "/#"),
        navbar_link("Contact", "/#"),
        spacing="5",
    )
def navbar_auth() -> rx.Component:
    return rx.hstack(
        rx.button("Sign Up", size="3", variant="outline"),
        rx.button("Log In", size="3"),
        spacing="4",
        justify="end"
    )

def navbar_buttons() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                navbar_logo(),
                navbar_menu(),
                navbar_auth(),
                justify="between",
                align_items="center"
            )
        ),
        rx.mobile_and_tablet(
            # TODO
        ),
        bg=rx.Color("accent", 3),
        padding="1em",
        width="100%"
    )