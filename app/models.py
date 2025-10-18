from datetime import UTC, datetime
from hashlib import md5

import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), index=True, unique=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: orm.Mapped[str | None] = orm.mapped_column(sa.String(256))

    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates='author')

    about_me: orm.Mapped[str | None] = orm.mapped_column(sa.String(140))
    last_seen: orm.Mapped[datetime | None] = orm.mapped_column(
        default=lambda: datetime.now(UTC)
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

class Post(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    body: orm.Mapped[str] = orm.mapped_column(sa.String(140))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(index=True, default=lambda: datetime.now(UTC))
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('user.id'), index=True)

    author: orm.Mapped['User'] = orm.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body}>'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
