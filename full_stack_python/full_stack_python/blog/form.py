import reflex as rx
from .state import BlogAddFormState, BlogEditFormState

def blog_post_add_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="title",                
                    placeholder="Title",
                    required=True,
                    width="100%"
                ),
                 width="100%"
            ),
            rx.text_area(
                name="content",
                placeholder="Your message",
                required=True,
                width="100%"
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=BlogAddFormState.handle_submit,
        reset_on_submit=True,
    )
         


def blog_post_edit_form() -> rx.Component:

    post = BlogEditFormState.post
    post_content = BlogEditFormState.post_content

    title = post.title

    return rx.form(
        rx.box(
            rx.input(
                type='hidden',
                name='post_id',
                value=post.id
            ),
            display="none",
        ),
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="title", 
                    default_value=title,               
                    placeholder="Title",
                    required=True,
                    width="100%"
                ),
                 width="100%"
            ),
            rx.text_area(
                name="content",
                placeholder="Your message",
                value=post_content,
                on_change=BlogEditFormState.set_post_content,
                required=True,
                width="100%"
            ),
            rx.flex(
                rx.switch(
                    default_checked=BlogEditFormState.post_publish_active,
                    on_change=BlogEditFormState.set_post_publish_active,
                    name='publish_active'
                ),
                rx.text("Publish Active"),
                spacing="2",
            ),
            rx.cond(
                BlogEditFormState.post_publish_active,
                rx.hstack(
                    rx.input(
                        type="date",
                        name="publish_date",
                        default_value=BlogEditFormState.publish_display_date,
                        width="100%",
                    ),
                    rx.input(
                        type="time",
                        name="publish_time",
                        default_value=BlogEditFormState.publish_display_time,
                        width="100%",
                    ),   
                    width="100%"                 
                ),
                rx.fragment()
            ),            
            rx.button("Submit", type="submit"),
        ),
        on_submit=BlogEditFormState.handle_submit,
        reset_on_submit=True,
    )         