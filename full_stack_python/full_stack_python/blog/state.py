from typing import List, Optional
import reflex as rx 
from sqlmodel import select
from datetime import datetime
import sqlalchemy
from ..model import BlogPostModel, UserInfo
from ..auth.state import SessionState

class BlogPostState(SessionState):
    posts: List['BlogPostModel'] = []
    post: Optional['BlogPostModel'] = None
    post_content:str = ""
    post_publish_active: bool = False

    @rx.var(cache=True)
    def blog_post_id(self) -> Optional[int]:
        return self.router.page.params.get("blog_id") or None
    
    def load_posts(self):
        # load user's post only
        with rx.session() as session:
            # BlogPostModel.join(Userinfo)
            result = session.exec(
                select(BlogPostModel)
                .options(sqlalchemy.orm.joinedload(BlogPostModel.userinfo))
                .where(BlogPostModel.userinfo_id == self.my_userinfo_id)
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
        # if not logged, then nullify all
        if self.my_userinfo_id is None:
            self.post = None
            self.post_content = ""
            self.post_publish_active = False
        
        # 자기가 작성한 것
        lookups = (
            (BlogPostModel.userinfo_id == self.my_userinfo_id) &
            (BlogPostModel.id == self.blog_post_id)
        )
        with rx.session() as session:
            if self.blog_post_id == "":
                self.post = None
                return 
            
            # BlogPost.join(UserInfo).join(User)
            sql_statement = select(BlogPostModel).options(
                sqlalchemy.orm.joinedload(BlogPostModel.userinfo).joinedload(UserInfo.user)
            ).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            self.post = result 
            if result is None: # post 가 None이면 content도 None
                self.post_content = ""
                return 
            self.post_content = result.content
            self.post_publish_active = result.publish_active

    def to_blog_post(self):
        if not self.post:
            return rx.redirect("/blog")
        return rx.redirect(f"/blog/{self.post.id}")

class BlogAddFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        data = form_data.copy()
        # add userinfo if loggined
        if self.my_userinfo_id is not None:
            data['userinfo_id'] = self.my_userinfo_id
        self.form_data = data
        self.add_post(data)
        return self.to_blog_post()

class BlogEditFormState(BlogPostState):
    form_data: dict = {}

    @rx.var(cache=True)
    def publish_display_date(self) -> str:
        if not self.post:
            return datetime.now().strftime("%Y-%m-%d")
        if not self.post.publish_date:
            return datetime.now().strftime("%Y-%m-%d")
        return self.post.publish_date.strftime("%Y-%m-%d")

    @rx.var(cache=True)
    def publish_display_time(self) -> str:        
        if not self.post:
            return datetime.now().strftime("%H:%M:%S")    
        if not self.post.publish_date:
            return datetime.now().strftime("%H:%M:%S")    
        return self.post.publish_date.strftime("%H:%M:%S")    

    def handle_submit(self, form_data):
        self.form_data = form_data
        post_id = form_data.pop('post_id')
        
        publish_active = False
        if 'publish_active' in form_data:
            publish_active = form_data.pop('publish_active') == 'on'

        publish_date = None
        if 'publish_date' in form_data:
            publish_date = form_data.pop('publish_date')

        publish_time = None
        if 'publish_time' in form_data:
            publish_time = form_data.pop('publish_time')

        publish_input_string = f"{publish_date} {publish_time}"
        try:
            final_publish_date = datetime.strptime(
                publish_input_string, '%Y-%m-%d %H:%M:%S'
            )
        except:
            final_publish_date = None

        updated_data = {**form_data}
        updated_data['publish_active'] = publish_active
        updated_data['publish_date'] = final_publish_date
        print(post_id, updated_data)
        self.edit_post(post_id, updated_data)  
        return self.to_blog_post()      
        