import reflex as rx 
from typing import List, Optional
from .model import BlogPostModel
from sqlmodel import select

class BlogPostState(rx.State):
    posts: List['BlogPostModel'] = []
    post: Optional['BlogPostModel'] = None
    post_content:str = ""

    @rx.var(cache=True)
    def blog_post_id(self) -> Optional[int]:
        return self.router.page.params.get("blog_id") or None
    
    def load_posts(self):
        with rx.session() as session:
            result = session.exec(
                select(BlogPostModel)
            ).all()
            self.posts = result
        

    def add_post(self, form_data: dict):
        with rx.session() as session:
            post = BlogPostModel(**form_data)
            session.add(post)
            session.commit()
            session.refresh(post) # due to post.id

            # set current post
            self.post = post

    def edit_post(self, post_id: int, updated_data: dict):
        with rx.session() as session:
            post = session.exec(
                select(BlogPostModel).where(
                    BlogPostModel.id == post_id
                )
            ).one_or_none()
            if post is None:
                return
            for k, v in updated_data.items():
                setattr(post, k, v)
            session.add(post)
            session.commit()
            session.refresh(post)

            self.post = post
            self.post_content = post.content
        
    def get_post_detail(self):
        with rx.session() as session:
            if self.blog_post_id == "":
                self.post = None
            result = session.exec(
                select(BlogPostModel).where(
                    BlogPostModel.id == self.blog_post_id
                )
            ).one_or_none()

            self.post = result
            self.post_content = result.content
        

    def to_blog_post(self):
        if not self.post:
            return rx.redirect("/blog")
        return rx.redirect(f"/blog/{self.post.id}")

class BlogAddFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        self.form_data = form_data
        self.add_post(form_data)
        return self.to_blog_post()

class BlogEditFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        self.form_data = form_data
        post_id = form_data.pop('post_id')
        updated_data = {**form_data}
        self.edit_post(post_id, form_data)  
        return self.to_blog_post()      
        