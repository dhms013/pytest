from flask import Flask
# Import all four method-specific blueprints
from routes.post_users import post_bp
from routes.get_users import get_bp
from routes.put_users import put_bp
from routes.delete_users import delete_bp

app = Flask(__name__)

# Register each blueprint with the main app
app.register_blueprint(post_bp)
app.register_blueprint(get_bp)
app.register_blueprint(put_bp)
app.register_blueprint(delete_bp)

if __name__ == '__main__':
    # Flask defaults to 127.0.0.1:5000. 
    # If you see 3000, you explicitly set it like this:
    app.run(debug=True, host='127.0.0.1', port=3000)