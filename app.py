import os
from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from models import db, User
from flask_cors import CORS
from cache import cache
from dotenv import load_dotenv

login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    CORS(app,supports_credentials=os.getenv("supports_credentials"), origins=[os.getenv("origins")])
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE")
    app.config["CACHE_REDIS_HOST"] = os.getenv("CACHE_REDIS_HOST")
    app.config["CACHE_REDIS_PORT"] = os.getenv("CACHE_REDIS_PORT")
    app.config["CACHE_DEFAULT_TIMEOUT"] = os.getenv("CACHE_DEFAULT_TIMEOUT")

    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({
            "success": False,
            "message": "Authentication required."
        }), 401

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None
        
    from blueprints.auth import auth_bp
    from blueprints.admin import admin_bp
    from blueprints.staff import staff_bp
    from blueprints.user import user_bp

    app.register_blueprint(auth_bp, url_prefix = "/auth")
    app.register_blueprint(admin_bp, url_prefix = "/admin")
    app.register_blueprint(staff_bp, url_prefix = "/staff")
    app.register_blueprint(user_bp, url_prefix = "/user")

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role="admin").first()
        if not admin:
            admin = User(
                name = "Admin",
                email = "soumyastudy710@gmail.com",
                phone = "1234567890",
                role = "admin"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print(">> Default Admin Created: soumyastudy710@gmail.com / admin123")
        else:
            print(">> Admin already existed")
    

    @app.route("/")
    def home():
        return render_template("index.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
