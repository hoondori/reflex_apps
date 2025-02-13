import reflex as rx 
from ..ui.base import base_page
from .state import BlogPostState
from .. import navigation
from ..model import BlogPostModel


def blog_post_detail_page():

    can_edit = True
    edit_link = rx.link('Edit', href=f"/blog/{BlogPostState.blog_post_id}/edit")
    edit_link_el = rx.cond(
        can_edit,
        edit_link,
        rx.fragment("")
    )
    my_child = rx.vstack(
        rx.hstack(
            rx.heading(BlogPostState.post.title, size="7"),
            edit_link_el,
        ),
        rx.cond(BlogPostState.post.userinfo, rx.text(BlogPostState.post.userinfo.email), rx.fragment("")),
        rx.text(BlogPostState.post.publish_date),
        rx.text(
            BlogPostState.post.content, 
            white_space='pre-wrap',
        ),            
        spacing="5",
        align="center",
        min_height="85vh",
    )

    return base_page(
        my_child
    )    

def blog_post_detail_link(child: rx.Component, post: BlogPostModel):
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

def blog_post_entry(blog_post: BlogPostModel) -> rx.Component:
    return rx.vstack(
        blog_post_detail_link(
            rx.vstack(
                rx.heading(blog_post.title, size="3"),
                rx.cond(blog_post.userinfo, rx.text(blog_post.userinfo.email), rx.fragment("")),
                align="center",
            ),
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
            rx.foreach(BlogPostState.posts, blog_post_entry),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )