import reflex as rx
from rxconfig import config
from .ui.base import base_page
from . import contact, navigation, blog, pages, auth
import reflex_local_auth
from .auth.page import (
    my_login_page,
    my_register_page
)
from .auth.state import SessionState

class State(rx.State):
    """The app state."""
    label = "this is my label"
   
    def handle_title_changed(self, value):
        self.label = value


def index() -> rx.Component:
    # Welcome Page (Index)
    return base_page(
        rx.vstack(
            rx.heading(State.label, size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.input(default_value=State.label,
                on_change=State.handle_title_changed),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            text_align="center",
        ),
    )


app = rx.App()
app.add_page(index)

# auth pages
app.add_page(
    my_login_page,
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)
app.add_page(
    my_register_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)

# my page
app.add_page(pages.about_page, route=navigation.routes.ABOUT)
app.add_page(pages.protected_page, 
             route=navigation.routes.PROTECTED,
             on_load=SessionState.on_load)
app.add_page(pages.pricing_page, route=navigation.routes.PRICING)
app.add_page(contact.contact_page, route=navigation.routes.CONTACT_US)
app.add_page(contact.contact_entry_list_page, route=navigation.routes.CONTACT_ENTRIES, 
             on_load=contact.ContactState.list_entries)
app.add_page(blog.blog_post_list_page, 
             route=navigation.routes.BLOG,
             on_load=blog.BlogPostState.load_posts)
app.add_page(blog.blog_post_add_page, 
             route=navigation.routes.BLOG_ADD)
app.add_page(blog.blog_post_detail_page, 
             route="/blog/[blog_id]",
             on_load=blog.BlogPostState.get_post_detail)
app.add_page(blog.blog_post_edit_page, 
             route="/blog/[blog_id]/edit",
             on_load=blog.BlogPostState.get_post_detail)