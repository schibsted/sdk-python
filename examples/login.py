
# Flask is a dependency to run this example, but it is not a dependency for the SDK
# install Flask: pip install flask

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))


from spid.client import SPiDClient
from flask import Flask, request, session, redirect, url_for

options = {
    "client_id"             : '4e8463569caf7ca019000007',
    "client_secret"         : 'foobar',
    "client_sign_secret"    : 'foobar',
    "server"                : 'spp.dev',
    "https"                 : False,
    "redirect_uri"          : 'http://localhost:5000',
    "api_version"           : 2,
    "production"            : False
}

app = Flask(__name__)
client = SPiDClient(**options)

@app.route("/")
def index():
    code = request.args.get('code', '')
    if code:
        token = client.get_access_token(code).json()
        res = client.api("/me", params={"oauth_token": token.get('access_token', '')}).json()
        user = res.get('data', {})

        if user:
            session["token"] = token
            session["user"] = user

        return redirect(url_for("index"))

    if session.get("user", {}):
        user = session.get("user", {})
        token = session.get("token", {})

        return '''<html>
                    <head><title>SDK-Python - Login User Token Example</title></head>
                    <body>Logged in as {} with user_id {} | <a href="{}">Log out</a></body>
                </html>'''.format(user.get('displayName', ''), user.get('userId', ''), url_for("logout"))


    url = client.url_builder.get_login_url()
    return '''<html>
                <head><title>SDK-Python - Login User Token Example</title></head>
                <body><a href="{}">Log in</a></body>
            </html>'''.format(url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(client.url_builder.get_logout_url())


if __name__ == "__main__":
    app.debug = True
    app.secret_key = 'my very secret session encryption key'
    app.run()