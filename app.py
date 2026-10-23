from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("skillconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        skills = request.form["skills"]

        conn = sqlite3.connect("skillconnect.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO registrations
        (fullname, email, phone, skills)
        VALUES (?, ?, ?, ?)
        """, (fullname, email, phone, skills))

        conn.commit()
        conn.close()

        return f"""
        <h1>Registration Successful</h1>

        <p><b>Full Name:</b> {fullname}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Skills:</b> {skills}</p>

        <br>

        <a href="/candidates">View All Candidates</a>

        <br><br>

        <a href="/">Return Home</a>
        """

    return """
    <html>
    <head>
        <title>SkillConnect SA</title>
    </head>

    <body style="font-family: Arial; margin:40px;">

        <h1>SkillConnect SA</h1>

        <h2>Youth Employment & Work Readiness Platform</h2>

        <p>
        SkillConnect SA helps young people build professional profiles,
        improve work readiness and connect with employment opportunities.
        </p>

        <hr>

        <p>
        <a href="/career-guidance">Career Guidance</a> |
        <a href="/interview-tips">Interview Tips</a> |
        <a href="/opportunities">Opportunities</a> |
        <a href="/candidates">Registered Candidates</a>
        </p>

        <hr>

        <h3>Candidate Registration</h3>

        <form method="POST">

            <label>Full Name</label><br>
            <input type="text" name="fullname" required><br><br>

            <label>Email Address</label><br>
            <input type="email" name="email" required><br><br>

            <label>Phone Number</label><br>
            <input type="text" name="phone" required><br><br>

            <label>Skills</label><br>
            <textarea name="skills" rows="5" cols="40"></textarea><br><br>

            <button type="submit">
                Submit Application
            </button>

        </form>

    </body>
    </html>
    """


@app.route("/candidates")
def candidates():

    conn = sqlite3.connect("skillconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT fullname, email, phone, skills
    FROM registrations
    """)

    records = cursor.fetchall()
    conn.close()

    html = """
    <h1>Registered Candidates</h1>
    <hr>
    """

    if len(records) == 0:
        html += "<p>No candidates registered yet.</p>"

    for candidate in records:
        html += f"""
        <p><b>Name:</b> {candidate[0]}</p>
        <p><b>Email:</b> {candidate[1]}</p>
        <p><b>Phone:</b> {candidate[2]}</p>
        <p><b>Skills:</b> {candidate[3]}</p>
        <hr>
        """

    html += '<br><a href="/">Back to Home</a>'

    return html


@app.route("/career-guidance")
def career_guidance():
    return """
    <h1>Career Guidance</h1>

    <ul>
        <li>Create a professional CV.</li>
        <li>Build communication skills.</li>
        <li>Develop workplace readiness.</li>
        <li>Prepare for your first job.</li>
    </ul>

    <a href="/">Back to Home</a>
    """


@app.route("/interview-tips")
def interview_tips():
    return """
    <h1>Interview Preparation</h1>

    <ul>
        <li>Research the company.</li>
        <li>Dress professionally.</li>
        <li>Practice common interview questions.</li>
        <li>Arrive on time.</li>
        <li>Be confident and honest.</li>
    </ul>

    <a href="/">Back to Home</a>
    """


@app.route("/opportunities")
def opportunities():
    return """
    <h1>Available Opportunities</h1>

    <h3>Software Development Internship</h3>
    <p>Johannesburg</p>

    <h3>IT Support Learnership</h3>
    <p>Gauteng</p>

    <h3>Graduate Programme</h3>
    <p>Remote</p>

    <br>

    <a href="/">Back to Home</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
    