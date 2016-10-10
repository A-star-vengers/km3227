from app import db
from models import BlogPost

# Create the database and the db tables
db.create_all()

# insert
db.session.add(BlogPost("Good", "Im good."))
db.session.add(BlogPost("Well", "Im well."))

# commit the changes
db.session.commit()
