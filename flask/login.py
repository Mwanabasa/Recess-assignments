from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = "replace-with-a-strong-secret"

# Demo credentials for assignment purposes.
DEMO_USER = {"email": "hanes@gmail.com", "password": "12345"}


@app.route("/")
def home():
	return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form.get("email", "").strip().lower()
		password = request.form.get("password", "")

		if email == DEMO_USER["email"] and password == DEMO_USER["password"]:
			flash("Login successful.", "success")
			return redirect(url_for("dashboard"))

		flash("Invalid email or password.", "danger")

	return render_template("login.html")


@app.route("/dashboard")
def dashboard():
	return "<h2>Welcome to the dashboard.</h2><p><a href='/login'>Back to login</a></p>"


@app.route("/register")
def register():
	return "<h2>Register page placeholder.</h2><p>Create your register page here.</p>"


if __name__ == "__main__":
	app.run(debug=True)
