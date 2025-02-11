import reflex as rx 
from ..ui.base import base_page
from . import model, state, form
from .. import navigation


def blog_post_detail_page():

    can_edit = True
    edit_link = rx.link('Edit', href=f"/blog/{state.BlogPostState.blog_post_id}/edit")
    edit_link_el = rx.cond(
        can_edit,
        edit_link,
        rx.fragment("")
    )
    my_child = rx.vstack(
        rx.hstack(
            rx.heading(state.BlogPostState.post.title, size="7"),
            edit_link_el,
        ),
        rx.text(
            state.BlogPostState.post.content, 
            white_space='pre-wrap',
        ),            
        spacing="5",
        align="center",
        min_height="85vh",
    )

    return base_page(
        my_child
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