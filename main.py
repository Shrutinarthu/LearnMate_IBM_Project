
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, template_folder='Templates')

# Store your actual IBM API key in Replit's Secrets or use os.environ.get
IBM_API_KEY = os.environ.get("IBM_API_KEY")  # make sure to set this in Replit secrets
GRANITE_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-07-01"

# Load course dataset
try:
    with open("dataset.json") as f:
        courses = json.load(f)
except Exception as e:
    courses = []
    print("Failed to load dataset.json:", e)

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
        "message": f"Perfect! Here's your personalized learning path for {interest} at {level} level",
        "courses": filtered_courses,
        "roadmap": roadmap
    })

def generate_roadmap(interest, level):
    roadmaps = {
        "Artificial Intelligence & Machine Learning": {
            "Beginner": [
                "🧠 Start with Python programming fundamentals and basic mathematics (linear algebra, statistics)",
                "📊 Learn data manipulation with pandas and NumPy libraries",
                "🤖 Understand machine learning concepts and algorithms (supervised vs unsupervised learning)",
                "📈 Practice with simple projects like linear regression and classification problems",
                "📊 Explore data visualization using matplotlib and seaborn",
                "💼 Build your first end-to-end ML project and create a portfolio"
            ],
            "Intermediate": [
                "🧠 Deepen your understanding of advanced ML algorithms and ensemble methods",
                "🔥 Learn neural networks and deep learning frameworks (TensorFlow/PyTorch)",
                "👁️ Specialize in areas like computer vision or natural language processing",
                "⚙️ Practice feature engineering and model optimization techniques",
                "🏆 Work on real-world projects and participate in Kaggle competitions",
                "🚀 Start learning about MLOps and model deployment"
            ],
            "Advanced": [
                "📚 Research cutting-edge AI techniques and read academic papers",
                "🏗️ Implement advanced architectures like transformers and GANs",
                "🌟 Contribute to open-source AI projects and libraries",
                "🏭 Build production-ready AI systems with proper monitoring and scaling",
                "🔬 Explore specialized areas like reinforcement learning or AI ethics",
                "🎓 Consider pursuing research opportunities or advanced degrees"
            ]
        },
        "Data Science & Big Data Analytics": {
            "Beginner": [
                "🐍 Learn Python/R programming and statistical concepts",
                "📊 Master data manipulation with pandas and data cleaning techniques",
                "📈 Understand exploratory data analysis and data visualization",
                "🤖 Learn basic machine learning algorithms and when to use them",
                "💼 Practice with real datasets and build your first analytics projects",
                "📖 Develop storytelling skills and learn to present insights effectively"
            ],
            "Intermediate": [
                "🚀 Advance your machine learning skills with ensemble methods and feature engineering",
                "☁️ Learn big data technologies like Spark, Hadoop, or cloud platforms",
                "📊 Master advanced visualization techniques and dashboard creation",
                "🧪 Understand A/B testing, experimental design, and causal inference",
                "💼 Work on end-to-end data science projects with business impact",
                "⚖️ Learn about data ethics, bias, and responsible analytics"
            ],
            "Advanced": [
                "🧠 Specialize in advanced techniques like deep learning or time series analysis",
                "🏭 Build production data pipelines and implement MLOps practices",
                "👥 Lead data science initiatives and mentor team members",
                "🏢 Develop domain expertise in specific industries or use cases",
                "🌟 Contribute to open-source projects and the data science community",
                "📚 Stay current with research and emerging technologies in the field"
            ]
        },
        "Cybersecurity & Ethical Hacking": {
            "Beginner": [
                "🌐 Learn Computer Networks Fundamentals (TCP/IP, OSI Model)",
                "💻 Understanding Operating Systems (Windows/Linux security)",
                "🐍 Basic Programming (Python/Bash scripting for security)",
                "🔒 Introduction to Information Security Principles (CIA Triad)",
                "🛡️ Network Security Basics (Firewalls, VPNs, IDS/IPS)",
                "🔧 Hands-on with Security Tools (Nmap, Wireshark, Metasploit)",
                "🎯 Practice on Platforms like TryHackMe or HackTheBox"
            ],
            "Intermediate": [
                "🚀 Advanced Network Security (VLAN, Network Segmentation)",
                "🎯 Penetration Testing Fundamentals (OWASP Top 10)",
                "🔍 Vulnerability Assessment Techniques and Tools",
                "🕵️ Digital Forensics Basics and Evidence Handling",
                "📋 Security Frameworks (NIST, ISO 27001, CIS Controls)",
                "🚨 Incident Response Procedures and Threat Hunting",
                "🤖 Advanced Scripting for Security Automation"
            ],
            "Advanced": [
                "🔴 Advanced Penetration Testing & Red Team Operations",
                "🦠 Malware Analysis & Reverse Engineering",
                "☁️ Cloud Security (AWS/Azure/GCP Security Architecture)",
                "🔬 Advanced Digital Forensics and Memory Analysis",
                "🏗️ Security Architecture & Design for Enterprise",
                "👥 Leading Security Teams & Risk Management",
                "📚 Research & Staying Updated with Latest Threats and APTs"
            ]
        },
        "Full-Stack Web Development": {
            "Beginner": [
                "📝 Master HTML5 semantic markup and CSS3 styling fundamentals",
                "⚡ Learn JavaScript ES6+ features and DOM manipulation",
                "📱 Understand responsive design principles and CSS frameworks",
                "🔧 Build static websites and practice with version control (Git)",
                "🌐 Learn basic backend concepts and API consumption",
                "💼 Create your first full-stack application with a simple database"
            ],
            "Intermediate": [
                "⚛️ Master a frontend framework (React, Vue, or Angular)",
                "🖥️ Learn backend development with Node.js or another server technology",
                "🗄️ Understand database design and work with both SQL and NoSQL databases",
                "🔐 Implement authentication, authorization, and security best practices",
                "🧪 Learn about testing, CI/CD, and deployment strategies",
                "🏗️ Build complex applications with proper architecture patterns"
            ],
            "Advanced": [
                "🚀 Master advanced frontend patterns and state management",
                "🏗️ Design scalable backend architectures and microservices",
                "☁️ Implement advanced DevOps practices and cloud deployment",
                "⚡ Optimize application performance and handle high traffic loads",
                "👥 Lead development teams and mentor junior developers",
                "🌟 Stay current with emerging technologies and contribute to the community"
            ]
        },
        "UI/UX Design": {
            "Beginner": [
                "🎨 Design Principles & Color Theory fundamentals",
                "📝 Typography & Layout design basics",
                "👥 User Research Basics & Creating User Personas",
                "📱 Wireframing & Prototyping Tools (Figma/Sketch)",
                "💻 Basic User Interface Design principles",
                "🧪 Usability Testing Fundamentals",
                "💼 Build Your First Design Portfolio"
            ],
            "Intermediate": [
                "🔍 Advanced User Research Methods and Analytics",
                "🗺️ Information Architecture & User Flow Design",
                "⚡ Advanced Prototyping & Interaction Design",
                "🎯 Design Systems & Component Libraries",
                "📱 Mobile App Design Patterns and Guidelines",
                "📊 A/B Testing & Design Analytics",
                "♿ Accessibility & Inclusive Design Principles"
            ],
            "Advanced": [
                "👑 Design Leadership & Strategic Design Thinking",
                "📊 Advanced User Research & Data-Driven Design",
                "🛣️ Service Design & Customer Journey Mapping",
                "⚙️ Design Operations & Team Management",
                "💻 Advanced Prototyping (Code-based prototypes)",
                "💼 Business Strategy & Design ROI Measurement",
                "🚀 Innovation & Future Design Trends Research"
            ]
        },
        "Cloud Computing & DevOps": {
            "Beginner": [
                "☁️ Cloud Computing Fundamentals (AWS/Azure/GCP basics)",
                "🐧 Linux System Administration and Command Line",
                "🔧 Version Control with Git and Collaboration",
                "📦 Containerization with Docker basics",
                "🚀 CI/CD Pipeline fundamentals",
                "📊 Basic Monitoring and Logging",
                "🔧 Infrastructure as Code introduction"
            ],
            "Intermediate": [
                "🏗️ Advanced Cloud Services and Architecture",
                "🐳 Container Orchestration with Kubernetes",
                "🤖 Advanced CI/CD and Automation",
                "📊 Monitoring, Alerting, and Observability",
                "🔒 Cloud Security and Compliance",
                "📈 Performance Optimization and Scaling",
                "💰 Cost Optimization and Resource Management"
            ],
            "Advanced": [
                "🏢 Enterprise Cloud Architecture and Multi-cloud",
                "🔄 Advanced DevOps Culture and Practices",
                "🤖 Site Reliability Engineering (SRE) principles",
                "🔒 Advanced Security and Compliance Automation",
                "👥 Leading DevOps Transformation",
                "📊 Advanced Monitoring and Chaos Engineering",
                "🌟 Innovation and Emerging Technologies"
            ]
        },
        "Product Management": {
            "Beginner": [
                "📋 Product Management Fundamentals & Core Concepts",
                "🎯 Understanding Customer Needs & Market Research",
                "📊 Basic Data Analysis and Product Metrics",
                "🗺️ Product Roadmapping & Strategy Basics",
                "👥 Working with Cross-functional Teams",
                "🔄 Agile & Scrum Methodologies for Product Managers",
                "💼 Build Your First Product Case Study"
            ],
            "Intermediate": [
                "📈 Advanced Product Strategy & Business Model Design",
                "🧪 A/B Testing, Experimentation & Data-Driven Decisions",
                "🎨 User Experience (UX) & Design Thinking for PMs",
                "💰 Pricing Strategy & Go-to-Market Planning",
                "📊 Advanced Product Analytics & KPI Management",
                "🚀 Product Launch & Growth Strategies",
                "👥 Leadership & Stakeholder Management"
            ],
            "Advanced": [
                "🏢 Strategic Product Leadership & Portfolio Management",
                "🌍 International Product Expansion & Scaling",
                "🤖 AI/ML Integration in Product Development",
                "💼 Product-Led Growth & Platform Strategy",
                "👑 Executive Communication & Board Presentations",
                "🎓 Mentoring Product Teams & Building Product Culture",
                "🚀 Innovation Management & Future Product Trends"
            ]
        },
        "Blockchain & Web3 Development": {
            "Beginner": [
                "⛓️ Blockchain Fundamentals & Cryptography Basics",
                "💰 Understanding Bitcoin, Ethereum & Cryptocurrency",
                "📝 Smart Contract Basics & Solidity Programming",
                "🔧 Setting up Development Environment (Remix, Truffle, Hardhat)",
                "💼 Creating Your First Smart Contract & DApp",
                "🌐 Web3 Integration & MetaMask Connection",
                "🎯 Understanding Gas, Transactions & Blockchain Networks"
            ],
            "Intermediate": [
                "🏗️ Advanced Smart Contract Development & Security",
                "🎨 NFT Development & Token Standards (ERC-20, ERC-721)",
                "🔄 DeFi Protocols & Decentralized Exchange Development",
                "⚡ Layer 2 Solutions & Scalability (Polygon, Arbitrum)",
                "🧪 Smart Contract Testing & Deployment Strategies",
                "📊 Blockchain Analytics & On-chain Data Analysis",
                "🌍 Multi-chain Development & Cross-chain Protocols"
            ],
            "Advanced": [
                "🏭 Enterprise Blockchain Solutions & Private Networks",
                "🔬 Advanced Cryptography & Zero-Knowledge Proofs",
                "🤖 MEV (Maximal Extractable Value) & Advanced Trading Bots",
                "🏢 DAO Development & Governance Mechanisms",
                "🔒 Blockchain Security Auditing & Formal Verification",
                "👥 Leading Blockchain Projects & Community Building",
                "🚀 Research & Innovation in Emerging Blockchain Technologies"
            ]
        },
        "Quantum Computing": {
            "Beginner": [
                "⚛️ Quantum Physics Fundamentals & Linear Algebra Review",
                "🔬 Quantum Mechanics Basics (Superposition, Entanglement, Qubits)",
                "💻 Introduction to Quantum Computing Concepts & Quantum Gates",
                "🐍 Programming with Qiskit (IBM) or Cirq (Google)",
                "🧮 Simple Quantum Algorithms (Deutsch-Jozsa, Grover's)",
                "📊 Quantum Measurement & Quantum State Visualization",
                "🎯 Hands-on with Quantum Simulators & Cloud Platforms"
            ],
            "Intermediate": [
                "🔢 Advanced Quantum Algorithms (Shor's, Quantum Fourier Transform)",
                "🧪 Quantum Error Correction & Noise Mitigation",
                "⚙️ NISQ (Noisy Intermediate-Scale Quantum) Computing",
                "🔬 Variational Quantum Algorithms & Quantum Machine Learning",
                "🌐 Quantum Networking & Quantum Communication Protocols",
                "📈 Quantum Advantage Analysis & Benchmarking",
                "🏗️ Quantum Software Development & Circuit Optimization"
            ],
            "Advanced": [
                "🔬 Quantum Hardware & Physical Implementations",
                "🧠 Advanced Quantum Machine Learning & Quantum AI",
                "🔐 Quantum Cryptography & Post-Quantum Security",
                "🏭 Quantum Computing for Industry Applications",
                "📚 Quantum Computing Research & Academic Contributions",
                "👥 Leading Quantum Computing Teams & Projects",
                "🚀 Emerging Quantum Technologies & Future Developments"
            ]
        },
        "Internet of Things (IoT) & Edge Computing": {
            "Beginner": [
                "🌐 IoT Fundamentals & Architecture Overview",
                "🔌 Electronics Basics & Sensor Integration",
                "💻 Microcontroller Programming (Arduino, Raspberry Pi)",
                "📡 Wireless Communication (WiFi, Bluetooth, LoRa)",
                "☁️ Cloud Platforms for IoT (AWS IoT, Azure IoT)",
                "📊 Data Collection & Basic Analytics",
                "🔧 Building Your First IoT Project"
            ],
            "Intermediate": [
                "⚙️ Advanced IoT Protocols (MQTT, CoAP, HTTP/2)",
                "🔒 IoT Security & Device Authentication",
                "🏗️ Edge Computing Architecture & Local Processing",
                "📈 IoT Data Processing & Real-time Analytics",
                "🤖 Machine Learning at the Edge",
                "🌍 Industrial IoT (IIoT) & Smart Manufacturing",
                "📱 Mobile App Development for IoT Control"
            ],
            "Advanced": [
                "🏭 Large-scale IoT Deployment & Management",
                "🔬 Advanced Edge AI & Federated Learning",
                "🌆 Smart City Solutions & Urban IoT",
                "⚡ Ultra-low Latency Applications & 5G Integration",
                "👥 IoT Project Leadership & System Architecture",
                "🔐 Advanced IoT Security & Threat Management",
                "🚀 Emerging IoT Technologies & Future Trends"
            ]
        },
        "Digital Marketing with AI Tools": {
            "Beginner": [
                "📱 Digital Marketing Fundamentals & Customer Journey",
                "🎯 SEO/SEM Basics & Content Marketing",
                "📊 Social Media Marketing & Platform Strategies",
                "🤖 Introduction to AI Marketing Tools & Automation",
                "📈 Google Analytics & Performance Tracking",
                "✉️ Email Marketing & Lead Generation",
                "💼 Creating Your First AI-Powered Marketing Campaign"
            ],
            "Intermediate": [
                "🧠 Advanced AI Tools (ChatGPT, Jasper, Copy.ai)",
                "🎨 AI-Generated Content & Creative Automation",
                "📊 Predictive Analytics & Customer Segmentation",
                "🎯 Programmatic Advertising & AI Bidding",
                "🔍 Advanced SEO with AI & Voice Search Optimization",
                "📱 Personalization & Dynamic Content Generation",
                "🤖 Chatbots & Conversational Marketing"
            ],
            "Advanced": [
                "🏢 Enterprise Marketing Automation & CRM Integration",
                "🧠 Advanced AI/ML for Marketing Attribution",
                "📊 Customer Lifetime Value & Predictive Modeling",
                "🎯 Advanced A/B Testing & Multivariate Analysis",
                "👥 Marketing Team Leadership & AI Strategy",
                "🚀 Emerging AI Marketing Technologies",
                "📈 ROI Optimization & Advanced Marketing Analytics"
            ]
        },
        "Software Testing & Automation": {
            "Beginner": [
                "🧪 Software Testing Fundamentals & SDLC",
                "📋 Test Planning & Test Case Design",
                "🔍 Manual Testing Techniques & Bug Reporting",
                "🤖 Introduction to Test Automation",
                "🐍 Programming Basics for Testers (Python/Java)",
                "🔧 Selenium WebDriver Basics",
                "📊 Test Management Tools & Bug Tracking"
            ],
            "Intermediate": [
                "🏗️ Advanced Test Automation Frameworks",
                "📱 Mobile App Testing (Android/iOS)",
                "🌐 API Testing & Service Testing",
                "⚡ Performance Testing & Load Testing",
                "🔒 Security Testing Fundamentals",
                "🔄 CI/CD Integration & DevOps Testing",
                "📊 Test Metrics & Reporting"
            ],
            "Advanced": [
                "🤖 AI/ML in Testing & Intelligent Test Automation",
                "🏢 Enterprise Test Strategy & Test Architecture",
                "👥 Leading QA Teams & Test Process Improvement",
                "🔬 Advanced Performance Engineering",
                "🛡️ Advanced Security Testing & Penetration Testing",
                "📈 Test Analytics & Predictive Quality Models",
                "🚀 Emerging Testing Technologies & Future Trends"
            ]
        },
        "Mobile App Development (Android/iOS)": {
            "Beginner": [
                "📱 Mobile Development Fundamentals & Platform Differences",
                "☕ Java/Kotlin for Android OR Swift for iOS",
                "🔧 Setting up Development Environment (Android Studio/Xcode)",
                "🎨 UI/UX Design for Mobile Apps",
                "📊 Data Storage & Local Databases",
                "🌐 API Integration & Networking",
                "📱 Publishing Your First App to App Stores"
            ],
            "Intermediate": [
                "🏗️ Advanced App Architecture (MVVM, Clean Architecture)",
                "🔄 Cross-platform Development (Flutter, React Native)",
                "🔔 Push Notifications & Background Processing",
                "📊 Analytics Integration & App Performance Monitoring",
                "💰 In-App Purchases & Monetization Strategies",
                "🔒 Mobile Security & Data Protection",
                "🧪 Advanced Testing & App Store Optimization"
            ],
            "Advanced": [
                "🤖 AI/ML Integration in Mobile Apps",
                "🥽 AR/VR Mobile Development",
                "⚡ Advanced Performance Optimization",
                "🏢 Enterprise Mobile App Development",
                "👥 Leading Mobile Development Teams",
                "🔐 Advanced Mobile Security & Compliance",
                "🚀 Emerging Mobile Technologies & Future Trends"
            ]
        },
        "AR/VR Development": {
            "Beginner": [
                "🥽 AR/VR Fundamentals & Technology Overview",
                "🎮 Unity 3D Basics & C# Programming",
                "📱 AR Development with ARCore/ARKit",
                "🌍 VR Development Basics & Oculus SDK",
                "🎨 3D Modeling Basics (Blender/Maya)",
                "🔧 Setting up Development Environment",
                "💼 Creating Your First AR/VR Experience"
            ],
            "Intermediate": [
                "🏗️ Advanced Unity Development & Optimization",
                "🤝 Multiplayer VR/AR Applications",
                "🎯 Hand Tracking & Gesture Recognition",
                "🔊 Spatial Audio & Haptic Feedback",
                "📱 WebXR Development & Browser-based AR/VR",
                "🧠 UX Design for Immersive Experiences",
                "📊 Performance Optimization for XR"
            ],
            "Advanced": [
                "🏭 Enterprise AR/VR Solutions",
                "🤖 AI Integration in AR/VR Applications",
                "🔬 Advanced Computer Vision & SLAM",
                "🏢 Mixed Reality Development (HoloLens)",
                "👥 Leading XR Development Teams",
                "🎓 XR for Education & Training Solutions",
                "🚀 Emerging XR Technologies & Future Trends"
            ]
        },
        "Game Development": {
            "Beginner": [
                "🎮 Game Development Fundamentals & Game Engines",
                "🔧 Unity Basics & C# Programming for Games",
                "🎨 2D Game Development & Sprite Animation",
                "🎯 Game Physics & Collision Detection",
                "🔊 Audio Integration & Sound Design Basics",
                "🎪 UI/UX Design for Games",
                "💼 Publishing Your First Game"
            ],
            "Intermediate": [
                "🌍 3D Game Development & Advanced Unity",
                "🤖 AI Programming for NPCs & Game Behavior",
                "🌐 Multiplayer Game Development & Networking",
                "📱 Mobile Game Development & Monetization",
                "🎨 Advanced Graphics & Shader Programming",
                "⚙️ Game Optimization & Performance Tuning",
                "🏪 Game Marketing & Community Building"
            ],
            "Advanced": [
                "🏭 AAA Game Development & Large Team Management",
                "🔧 Custom Game Engine Development",
                "🥽 VR/AR Game Development",
                "🤖 Advanced AI & Machine Learning in Games",
                "💼 Game Business & Publishing Strategies",
                "👥 Leading Game Development Teams",
                "🚀 Emerging Game Technologies & Future Trends"
            ]
        },
        "Data Engineering": {
            "Beginner": [
                "🗄️ Database Fundamentals (SQL & NoSQL)",
                "🐍 Python for Data Engineering",
                "📊 Data Modeling & ETL Basics",
                "☁️ Cloud Platforms for Data (AWS/Azure/GCP)",
                "🔧 Apache Spark Fundamentals",
                "📡 Data Pipeline Basics & Workflow Tools",
                "💼 Building Your First Data Pipeline"
            ],
            "Intermediate": [
                "🏗️ Advanced Data Architecture & Design Patterns",
                "⚡ Real-time Data Processing (Kafka, Kinesis)",
                "📊 Data Warehousing & Analytics Platforms",
                "🤖 Data Pipeline Automation & Orchestration",
                "🔒 Data Security & Privacy Compliance",
                "📈 Data Quality & Monitoring Systems",
                "☁️ Advanced Cloud Data Services"
            ],
            "Advanced": [
                "🏢 Enterprise Data Platform Architecture",
                "🤖 MLOps & Data Science Platform Integration",
                "📊 Advanced Analytics & Data Lake Management",
                "⚡ High-Performance Computing for Data",
                "👥 Leading Data Engineering Teams",
                "🔐 Advanced Data Governance & Compliance",
                "🚀 Emerging Data Technologies & Future Trends"
            ]
        },
        "DevOps & Agile Methodologies": {
            "Beginner": [
                "🔄 DevOps Fundamentals & Culture",
                "📋 Agile & Scrum Methodologies",
                "🔧 Version Control with Git",
                "🐧 Linux System Administration",
                "🚀 CI/CD Pipeline Basics",
                "📦 Containerization with Docker",
                "☁️ Cloud Platform Basics"
            ],
            "Intermediate": [
                "🤖 Advanced CI/CD & Automation",
                "🐳 Container Orchestration with Kubernetes",
                "📊 Monitoring & Observability",
                "🔧 Infrastructure as Code (Terraform, Ansible)",
                "🔒 DevSecOps & Security Integration",
                "📈 Performance Monitoring & Optimization",
                "👥 Team Collaboration & Communication"
            ],
            "Advanced": [
                "🏢 Enterprise DevOps Strategy & Transformation",
                "🤖 Site Reliability Engineering (SRE)",
                "🌍 Multi-cloud & Hybrid Cloud Strategies",
                "👑 DevOps Leadership & Cultural Change",
                "📊 Advanced Metrics & KPI Management",
                "🔐 Advanced Security & Compliance Automation",
                "🚀 Innovation & Emerging DevOps Technologies"
            ]
        }
    }
    
    return roadmaps.get(interest, {}).get(level, [
        "🔍 Research fundamentals in your chosen field",
        "📊 Practice hands-on projects", 
        "📝 Build a portfolio",
        "🌐 Network with professionals",
        "📅 Stay updated with industry trends"
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
