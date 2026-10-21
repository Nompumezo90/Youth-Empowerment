from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>SkillConnect SA</h1>
    <h2>Youth Employment & Work Readiness Platform</h2>
    <p>Application is running successfully.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)