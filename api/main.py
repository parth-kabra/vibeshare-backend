from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cloudinary
from cloudinary.uploader import upload
from random import shuffle

cloudinary.config( 
  cloud_name = "", 
  api_key = "", 
  api_secret = ""
)
def uploadImage(base64_image):
    upload_result = upload(base64_image)
    return upload_result


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""
CORS(app)


db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)  # Assuming email is unique
    user = db.Column(db.String(100))
    username = db.Column(db.String(100))
    img = db.Column(db.String(1000))
    
    def __init__(self, email, user, username, img):
        self.email = email
        self.user = user
        self.username = username
        self.img = img

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    username = db.Column(db.String(100))
    created_at = db.Column(db.String(100))
    text = db.Column(db.String(300))
    img = db.Column(db.String(1000))
    pfp = db.Column(db.String(1000))

    def __init__(self, user, username, created_at, text, img, pfp):
        self.user = user
        self.username = username
        self.created_at = created_at
        self.text = text
        self.img = img
        self.pfp = pfp

    def __repr__(self):
        return f"<Post {self.id}>"

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))  # Using email as a foreign key

    def __init__(self, post_id, user_email):
        self.post_id = post_id
        self.user_email = user_email

    def __repr__(self):
        return f"<Like {self.id}>"

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('users.email'))  # Changing user_id to user_email
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    text = db.Column(db.String(150))
    created_at = db.Column(db.String(100))
    name = db.Column(db.String(100))

    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __init__(self, user_email, post_id, text, created_at, name):
        self.user_email = user_email
        self.post_id = post_id
        self.text = text
        self.created_at = created_at
        self.name = name

    def __repr__(self):
        return f"<Comment {self.id}>"

    
@app.route("/api/get-user", methods=["POST"])
def getUser():
    try:
        data = request.get_json()
        username = data.get("username")
        existing_user = User.query.filter_by(username=username).first()
        if(existing_user):
            return jsonify({"user": {
                "state": True,
                "name":existing_user.user,
                "username":existing_user.username,
                "pfp":existing_user.img
            }})
        else:
            return jsonify({"user": {
                "state": False
            }})            
    except:
        return jsonify({"user": False})

@app.route("/api/get-posts", methods=["GET"])
def getPosts():
    try:
        posts_query = Post.query.all()
        all_posts = []
        for post in posts_query:
            post_obj = {
                "name": post.user,
                "username": post.username,
                "text": post.text,
                "pfp": post.pfp,
                "img": post.img,
                "likes": get_post_likes(post.id),
                "post_id": post.id
            }
            all_posts.append(post_obj)
        return jsonify({"posts": all_posts, "status":True})
    except Exception as e:
        print(e)
        return jsonify({"status":False})



@app.route("/api/like-post", methods=["POST"])
def like_post():
    try:
        data = request.get_json()
        post_id = data.get("post_id")
        user_email = data.get("user_email")

        existing_like = Like.query.filter_by(post_id=post_id, user_email=user_email).first()
        if existing_like:
            with app.app_context():
                local_like = db.session.merge(existing_like)
                db.session.delete(local_like)
                db.session.commit()
            return jsonify({"status": False, "message": "Post like removed"})
        else:
            like = Like(post_id=post_id, user_email=user_email)
            with app.app_context():
                db.session.add(like)
                db.session.commit()
            return jsonify({"status": True, "message": "Post liked successfully"})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "message": "An error occurred while liking the post"})


def get_post_likes(post_id):
    likes_count = Like.query.filter_by(post_id=post_id).count()
    return likes_count

@app.route("/api/check-liked", methods=["POST"])
def check_liked():
    try:
        data = request.get_json()
        post_id = data.get("post_id")
        user_email = data.get("user_email")

        existing_like = Like.query.filter_by(post_id=post_id, user_email=user_email).first()
        liked = True if existing_like else False
        return jsonify({"liked":liked})
    except:
        return jsonify({"liked":False})

@app.route("/")
def index():
    return jsonify("ok")

#status of the app
@app.route("/api/home", methods=["GET"])
def home():
    try:
        return jsonify({
            "status":True
        })
    except:
        return jsonify({
            "status":False
        })        


@app.route("/api/create-post", methods=["POST"])
def CreatePost():
    try:
        data = request.get_json()
        user = data.get("user")
        username = data.get("username")
        text = data.get("text")
        img = data.get("img")
        image_data = uploadImage(img)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        img_src = image_data["secure_url"]
        pfp = data.get("pfp")

        post = Post(user=user, username=username, created_at=created_at, text=text, img=img_src, pfp=pfp)
        with app.app_context():
            db.session.add(post)
            db.session.commit()


        return jsonify({"status": True})
    except:
        return jsonify({"status": False})
    
def email_exists(email):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return True
    return False

@app.route("/api/create-user", methods=["POST"])
def CreateUser():
    try:
        data = request.get_json()
        name = data.get("name")
        username = data.get("username")
        email = data.get("email")
        pfp = data.get("pfp")
        if(not email_exists(email)):
            user = User(email, name, username, pfp)
            with app.app_context():
                db.session.add(user)
                db.session.commit()

        return jsonify({"status": True})
    except:
        return jsonify({"status": False})



@app.route("/api/create-comment", methods=["POST"])
def create_comment():
    try:
        data = request.get_json()
        text = data.get("text")
        post_id = data.get("post_id")
        email = data.get("user_email")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = data.get("name")
        new_comment = Comment(name=name,user_email=email, post_id=post_id, text=text, created_at=created_at)
        with app.app_context():
            db.session.add(new_comment)
            db.session.commit()

        return jsonify({"status":True, "message": "Comment added successfully!"})
    
    except:
        return jsonify({"status": False, "message":"Failed to add comment."})

@app.route("/api/get-comments", methods=["POST"])
def getComments():
    try:
        data = request.get_json()
        post_id = data.get("post_id")
        post = Post.query.get(post_id)
        if(not post):
            return jsonify({"status":False, "message":"Post does not exist"})
        else:
            comments = Comment.query.filter_by(post_id = post_id).all()
            all_comments = []
            for comment in comments:
                all_comments.append({
                    "name":comment.name,
                    "email": comment.user_email,
                    "text": comment.text
                })
            return jsonify({"status":True, "message":"Post comments found", "comments":all_comments})
    except:
        return jsonify({"status":False, "message":"An error occured."})


@app.route("/api/get-featured", methods=["GET"])
def getFeatured():
    try:
        users = User.query.all()
        featured = []
        for i in range(min(len(users), 4)):
            user = users[i]
            featured.append({
                "name": user.user,
                "username": user.username,
                "img":user.img
            })
        shuffle(featured)
        return jsonify({"status":True, "message":"Fetched users.", "accounts":featured})
    except:
        return jsonify({"status":False, "message":"Failed to fetch."})


@app.route("/api/get-post", methods=["POST"])
def get_post():
    if 1:
        data = request.get_json()
        post_id = data.get("post_id")
        post = Post.query.filter_by(id = post_id).first()
        res = {
            "name":post.user,
            "username":post.username,
            "pfp":post.pfp,
            "img":post.img,
            "text":post.text,
            "status":True,
            "post_id":post_id,
            "likes":get_post_likes(post_id)
        }
        return jsonify(res)

if __name__ == '__main__':
    app.run()
 