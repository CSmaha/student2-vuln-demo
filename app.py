from flask import Flask, request, make_response, render_template_string, redirect, url_for

app = Flask(__name__)

USERS = {
    "student": "123456"
}

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Training Shop</title>
</head>
<body>
    <h1>Training Shop</h1>
    <p>Welcome to the demo application.</p>
    <ul>
        <li><a href="/search?q=test">Search</a></li>
        <li><a href="/login?username=student&password=123456">Quick Login Demo</a></li>
        <li><a href="/profile">Profile</a></li>
    </ul>
</body>
</html>
"""

@app.route("/")
def home():
    response = make_response(HOME_PAGE)
    response.set_cookie("session_id", "demo-session-value")
    return response

@app.route("/search")
def search():
    query = request.args.get("q", "")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search</title>
    </head>
    <body>
        <h2>Search Results</h2>
        <p>You searched for: {query}</p>
        <a href="/">Back</a>
    </body>
    </html>
    """
    return html

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    if USERS.get(username) == password:
        response = make_response(redirect(url_for("profile")))
        response.set_cookie("auth", username)
        return response

    return """
    <!DOCTYPE html>
    <html>
    <head><title>Login Failed</title></head>
    <body>
        <h3>Invalid credentials</h3>
        <a href="/">Back</a>
    </body>
    </html>
    """, 401

@app.route("/profile")
def profile():
    user = request.cookies.get("auth", "guest")
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Profile</title>
    </head>
    <body>
        <h2>User Profile</h2>
        <p>Welcome {{ user }}</p>
        <p>Email: student@example.com</p>
        <p>Role: user</p>
        <a href="/">Home</a>
    </body>
    </html>
    """, user=user)

@app.route("/debug")
def debug():
    return {
        "environment": "training",
        "version": "1.0.0",
        "feature_flag": True
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
