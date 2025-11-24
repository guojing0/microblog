import sqlalchemy as sa
import sqlalchemy.orm as orm

from app import create_app, db
from app.models import Post, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "orm": orm, "db": db, "User": User, "Post": Post}
