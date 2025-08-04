from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Store your actual IBM API key in Replit's Secrets or use os.environ.get
IBM_API_KEY = os.environ.get("IBM_API_KEY")  # make sure to set this in Replit secrets
GRANITE_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-07-01"

# Updated course dataset
courses = [
    {"course_name": "Artificial Intelligence & Machine Learning", "domain": "Artificial Intelligence & Machine Learning", "level": "Beginner", "link": "#"},
    {"course_name": "Data Science & Big Data Analytics", "domain": "Data Science & Big Data Analytics", "level": "Beginner", "link": "#"},
    {"course_name": "Cybersecurity & Ethical Hacking", "domain": "Cybersecurity", "level": "Beginner", "link": "#"},
    {"course_name": "Cloud Computing & DevOps", "domain": "Cloud Computing", "level": "Intermediate", "link": "#"},
    {"course_name": "Full-Stack Web Development", "domain": "Web Development", "level": "Intermediate", "link": "#"},
    {"course_name": "UI/UX Design", "domain": "UI/UX Design", "level": "All", "link": "#"},
    {"course_name": "Product Management", "domain": "Product Management", "level": "All", "link": "#"},
    {"course_name": "Blockchain & Web3 Development", "domain": "Blockchain", "level": "Intermediate", "link": "#"},
    {"course_name": "Quantum Computing", "domain": "Quantum Computing", "level": "Advanced", "link": "#"},
    {"course_name": "Internet of Things (IoT) & Edge Computing", "domain": "IoT", "level": "Intermediate", "link": "#"},
    {"course_name": "Digital Marketing with AI Tools", "domain": "Digital Marketing", "level": "Intermediate", "link": "#"},
    {"course_name": "Software Testing & Automation", "domain": "Software Testing", "level": "Intermediate", "link": "#"},
    {"course_name": "Mobile App Development (Android/iOS)", "domain": "Mobile Development", "level": "Intermediate", "link": "#"},
    {"course_name": "AR/VR Development", "domain": "AR/VR", "level": "Advanced", "link": "#"},
    {"course_name": "Game Development", "domain": "Game Development", "level": "Intermediate", "link": "#"},
    {"course_name": "Data Engineering", "domain": "Data Engineering", "level": "Intermediate", "link": "#"},
    {"course_name": "DevOps & Agile Methodologies", "domain": "DevOps", "level": "Advanced", "link": "#"},
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    interest = request.form.get("interest", "").strip()
    level = request.form.get("level", "").strip()

    if not interest or not level:
        return jsonify({"error": "Please select both interest and skill level"}), 400

    # Check if we have courses in our dataset
    filtered_courses = [
        c for c in courses 
        if c["domain"].lower() == interest.lower() and 
        (c["level"].lower() == level.lower() or c["level"].lower() == "all")
    ]

    # Generate learning roadmap based on interest and level
    roadmap = generate_roadmap(interest, level)

    return jsonify({
        "message": f"Learning Path for {interest} at {level} Level:",
        "courses": filtered_courses,
        "roadmap": roadmap
    })

def generate_roadmap(interest, level):
    roadmaps = {
        "Artificial Intelligence & Machine Learning": {
            "Beginner": [
                "🧠 Step 1: Understand AI fundamentals.",
                "📊 Step 2: Learn basic machine learning algorithms.",
                "📈 Step 3: Get hands-on with data analysis using Python."
            ],
            "Intermediate": [
                "📚 Step 1: Study advanced ML algorithms.",
                "🔍 Step 2: Explore deep learning concepts.",
                "⚙️ Step 3: Work on real-world ML projects."
            ],
            "Advanced": [
                "🧠 Step 1: Research cutting-edge ML techniques.",
                "🔍 Step 2: Participate in ML competitions.",
                "🌐 Step 3: Contribute to open-source AI projects."
            ],
        },
        # Add similar entries for the other courses (follow the format above)
    }

    return roadmaps.get(interest, {}).get(level, [
        "🔍 Research fundamentals in your chosen field",
        "📊 Practice hands-on projects", 
        "📝 Build a portfolio",
        "🌐 Network with professionals",
        "📅 Stay updated with industry trends"
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)