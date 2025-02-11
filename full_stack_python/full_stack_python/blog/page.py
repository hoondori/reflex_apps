import reflex as rx 
from ..ui.base import base_page
from . import model, state, form
from .. import navigation


def blog_post_detail_page():
    return base_page(
        rx.vstack(
            rx.heading(state.BlogPostState.post.title, size="7"),
            rx.text(state.BlogPostState.post.content),            
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )    

def blog_post_detail_link(child: rx.Component, post: model.BlogPostModel):
    """ generate link with post id """

    if post is None:
        return rx.fragment(child)
    post_id = post.id
    if post_id is None:
        return rx.fragment(child)
    url_root_path = navigation.routes.BLOG
    post_detail_url = f"{url_root_path}/{post_id}"
    return rx.link(
        child,
        href=post_detail_url
    )

def blog_post_entry(blog_post: model.BlogPostModel) -> rx.Component:
    return rx.vstack(
        blog_post_detail_link(
            rx.heading(blog_post.title, size="3"),
            blog_post
        ),
        padding="1em",
    )

def blog_post_list_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Blog Posts", size="7"),
            rx.link(
                rx.button("New Post"),
                href=navigation.routes.BLOG_ADD,
            ),
            rx.foreach(state.BlogPostState.posts, blog_post_entry),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )

def blog_post_add_page() -> rx.Component:
    my_form = form.blog_post_add_form()
    my_child =  rx.vstack(
        rx.heading("New Blog Post", size="9"),
        rx.desktop_only(
            rx.box(my_form, width="50vw")),
        rx.tablet_only(
            rx.box(my_form, width="80vw")),
        rx.mobile_only(
            rx.box(my_form, width="95vw")),
        spacing="5",
        justify="center",
        align="center",
        min_height="95vh",
    )

    return base_page(
        my_child,
    )