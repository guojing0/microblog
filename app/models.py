from datetime import UTC, datetime
from hashlib import md5
from time import time

import jwt
import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
)


class User(UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), index=True, unique=True
    )
    email: orm.Mapped[str] = orm.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))

    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates='author')

    about_me: orm.Mapped[str | None] = orm.mapped_column(sa.String(140))
    last_seen: orm.Mapped[datetime | None] = orm.mapped_column(
        default=lambda: datetime.now(UTC)
    )

    following: orm.WriteOnlyMapped['User'] = orm.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers',
    )
    followers: orm.WriteOnlyMapped['User'] = orm.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following',
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        return db.session.scalar(
            sa.select(sa.func.count())
            .select_from(followers)
            .where(followers.c.followed_id == self.id)
        )

    def following_count(self):
        return db.session.scalar(
            sa.select(sa.func.count())
            .select_from(followers)
            .where(followers.c.follower_id == self.id)
        )

    def following_posts(self):
        Author = orm.aliased(User)
        Follower = orm.aliased(User)

        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(
                sa.or_(
                    Author.id == self.id,  # author's own posts
                    Follower.id == self.id,  # posts from followed users
                )
            )
            .group_by(Post)  # to avoid duplicate posts
            .order_by(Post.timestamp.desc())
        )

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256',
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256']
            )['reset_password']
        except Exception:
            return None
        return db.session.get(User, id)


class Post(db.Model):
    __searchable__ = ['body']
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    body: orm.Mapped[str] = orm.mapped_column(sa.String(140))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(
        index=True, default=lambda: datetime.now(UTC)
    )
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('user.id'), index=True)

    author: orm.Mapped['User'] = orm.relationship(back_populates='posts')

    language: orm.Mapped[str | None] = orm.mapped_column(sa.String(5))

    def __repr__(self):
        return f'<Post {self.body}>'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
