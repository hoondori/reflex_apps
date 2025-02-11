import reflex as rx 
from typing import List, Optional
from .model import BlogPostModel
from sqlmodel import select

class BlogPostState(rx.State):
    posts: List['BlogPostModel'] = []
    post: Optional['BlogPostModel'] = None

    @rx.var(cache=True)
    def blog_post_id(self) -> Optional[int]:
        print(self.router.page.params)
        return self.router.page.params.get("blog_id") or None
    
    def load_posts(self):
        with rx.session() as session:
            result = session.exec(
                select(BlogPostModel)
            ).all()
            self.posts = result
        

    def add_post(self, form_data: dict):
        with rx.session() as session:
            print(form_data)
            post = BlogPostModel(**form_data)
            session.add(post)
            session.commit()
            session.refresh(post) # due to post.id

            # set current post
            self.post = post
        
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
        pass        

class BlogAddFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        self.form_data = form_data
        self.add_post(form_data)