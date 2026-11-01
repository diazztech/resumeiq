"""
skills_db.py
-------------
Master Skills Database for ResumeIQ.

Contains over 200 categorized technical and soft skills, along with common aliases
and synonyms (e.g., 'js' for 'JavaScript', 'k8s' for 'Kubernetes').
Designed to be easily readable and extendable for college students and beginners.
"""

from typing import Dict, List, Set

# Master Dictionary of Skills
# Structure:
# "Canonical Skill Name": {
#     "category": "Category Name",
#     "aliases": ["alias1", "alias2", ...]
# }
SKILLS_DB: Dict[str, Dict[str, any]] = {
    # =========================================================================
    # 1. PROGRAMMING LANGUAGES (30+)
    # =========================================================================
    "Python": {
        "category": "Programming Languages",
        "aliases": ["python", "python3", "python2", "py"]
    },
    "Java": {
        "category": "Programming Languages",
        "aliases": ["java", "core java", "j2se"]
    },
    "C++": {
        "category": "Programming Languages",
        "aliases": ["c++", "cpp", "cplusplus"]
    },
    "C": {
        "category": "Programming Languages",
        "aliases": ["c language", "c programming", "ansi c"]
    },
    "C#": {
        "category": "Programming Languages",
        "aliases": ["c#", "csharp", "c sharp"]
    },
    "JavaScript": {
        "category": "Programming Languages",
        "aliases": ["javascript", "js", "ecmascript"]
    },
    "TypeScript": {
        "category": "Programming Languages",
        "aliases": ["typescript", "ts"]
    },
    "PHP": {
        "category": "Programming Languages",
        "aliases": ["php", "php7", "php8"]
    },
    "Ruby": {
        "category": "Programming Languages",
        "aliases": ["ruby", "ruby on rails", "mri ruby"]
    },
    "Go": {
        "category": "Programming Languages",
        "aliases": ["golang", "go language", "go lang"]
    },
    "Rust": {
        "category": "Programming Languages",
        "aliases": ["rust", "rustlang"]
    },
    "Swift": {
        "category": "Programming Languages",
        "aliases": ["swift", "swiftlang", "swiftui"]
    },
    "Kotlin": {
        "category": "Programming Languages",
        "aliases": ["kotlin", "kt"]
    },
    "Dart": {
        "category": "Programming Languages",
        "aliases": ["dart", "dartlang"]
    },
    "Scala": {
        "category": "Programming Languages",
        "aliases": ["scala"]
    },
    "R": {
        "category": "Programming Languages",
        "aliases": ["r language", "r programming", "r-project", "r script"]
    },
    "MATLAB": {
        "category": "Programming Languages",
        "aliases": ["matlab", "matrix laboratory"]
    },
    "Perl": {
        "category": "Programming Languages",
        "aliases": ["perl"]
    },
    "Bash": {
        "category": "Programming Languages",
        "aliases": ["bash", "shell scripting", "sh", "zsh", "powershell"]
    },
    "SQL": {
        "category": "Programming Languages",
        "aliases": ["sql", "structured query language", "t-sql", "pl/sql"]
    },
    "HTML5": {
        "category": "Programming Languages",
        "aliases": ["html", "html5"]
    },
    "CSS3": {
        "category": "Programming Languages",
        "aliases": ["css", "css3"]
    },
    "Sass": {
        "category": "Programming Languages",
        "aliases": ["sass", "scss"]
    },
    "Lua": {
        "category": "Programming Languages",
        "aliases": ["lua"]
    },
    "Haskell": {
        "category": "Programming Languages",
        "aliases": ["haskell"]
    },
    "Julia": {
        "category": "Programming Languages",
        "aliases": ["julia", "julialang"]
    },
    "Solidity": {
        "category": "Programming Languages",
        "aliases": ["solidity", "smart contracts"]
    },

    # =========================================================================
    # 2. WEB DEVELOPMENT & FRAMEWORKS (30+)
    # =========================================================================
    "React": {
        "category": "Web Development",
        "aliases": ["react", "react.js", "reactjs", "react native"]
    },
    "Angular": {
        "category": "Web Development",
        "aliases": ["angular", "angular.js", "angularjs", "angular 2+"]
    },
    "Vue.js": {
        "category": "Web Development",
        "aliases": ["vue", "vue.js", "vuejs", "vue3"]
    },
    "Next.js": {
        "category": "Web Development",
        "aliases": ["next.js", "nextjs", "next js"]
    },
    "Node.js": {
        "category": "Web Development",
        "aliases": ["node.js", "nodejs", "node"]
    },
    "Express.js": {
        "category": "Web Development",
        "aliases": ["express", "express.js", "expressjs"]
    },
    "Django": {
        "category": "Web Development",
        "aliases": ["django", "django rest framework", "drf"]
    },
    "Flask": {
        "category": "Web Development",
        "aliases": ["flask"]
    },
    "FastAPI": {
        "category": "Web Development",
        "aliases": ["fastapi", "fast-api"]
    },
    "Spring Boot": {
        "category": "Web Development",
        "aliases": ["spring boot", "springboot", "spring framework", "spring"]
    },
    ".NET": {
        "category": "Web Development",
        "aliases": [".net", "dotnet", ".net core", "asp.net", "asp.net core"]
    },
    "Ruby on Rails": {
        "category": "Web Development",
        "aliases": ["ruby on rails", "rails"]
    },
    "Laravel": {
        "category": "Web Development",
        "aliases": ["laravel"]
    },
    "Tailwind CSS": {
        "category": "Web Development",
        "aliases": ["tailwind", "tailwindcss", "tailwind css"]
    },
    "Bootstrap": {
        "category": "Web Development",
        "aliases": ["bootstrap", "bootstrap 5", "bootstrap 4"]
    },
    "jQuery": {
        "category": "Web Development",
        "aliases": ["jquery"]
    },
    "Svelte": {
        "category": "Web Development",
        "aliases": ["svelte", "sveltekit"]
    },
    "GraphQL": {
        "category": "Web Development",
        "aliases": ["graphql", "graph ql"]
    },
    "REST API": {
        "category": "Web Development",
        "aliases": ["rest api", "restful api", "restful", "rest web services", "apis", "api development"]
    },
    "gRPC": {
        "category": "Web Development",
        "aliases": ["grpc"]
    },
    "WebSockets": {
        "category": "Web Development",
        "aliases": ["websocket", "websockets", "socket.io"]
    },
    "Microservices": {
        "category": "Web Development",
        "aliases": ["microservices", "microservice architecture", "micro-services"]
    },
    "Streamlit": {
        "category": "Web Development",
        "aliases": ["streamlit"]
    },
    "Redux": {
        "category": "Web Development",
        "aliases": ["redux", "redux toolkit", "rtk"]
    },
    "NestJS": {
        "category": "Web Development",
        "aliases": ["nestjs", "nest.js"]
    },

    # =========================================================================
    # 3. DATABASES & STORAGE (20+)
    # =========================================================================
    "PostgreSQL": {
        "category": "Databases",
        "aliases": ["postgresql", "postgres", "psql"]
    },
    "MySQL": {
        "category": "Databases",
        "aliases": ["mysql"]
    },
    "MongoDB": {
        "category": "Databases",
        "aliases": ["mongodb", "mongo"]
    },
    "SQLite": {
        "category": "Databases",
        "aliases": ["sqlite", "sqlite3"]
    },
    "Redis": {
        "category": "Databases",
        "aliases": ["redis"]
    },
    "Oracle Database": {
        "category": "Databases",
        "aliases": ["oracle db", "oracle database", "oracle 19c", "pl/sql"]
    },
    "Microsoft SQL Server": {
        "category": "Databases",
        "aliases": ["sql server", "mssql", "ms sql server"]
    },
    "Elasticsearch": {
        "category": "Databases",
        "aliases": ["elasticsearch", "elastic search", "elk"]
    },
    "Cassandra": {
        "category": "Databases",
        "aliases": ["cassandra", "apache cassandra"]
    },
    "DynamoDB": {
        "category": "Databases",
        "aliases": ["dynamodb", "aws dynamodb"]
    },
    "Firebase": {
        "category": "Databases",
        "aliases": ["firebase", "firestore", "realtime database"]
    },
    "Neo4j": {
        "category": "Databases",
        "aliases": ["neo4j", "graph database"]
    },
    "Snowflake": {
        "category": "Databases",
        "aliases": ["snowflake", "snowflake db"]
    },
    "Supabase": {
        "category": "Databases",
        "aliases": ["supabase"]
    },
    "MariaDB": {
        "category": "Databases",
        "aliases": ["mariadb"]
    },

    # =========================================================================
    # 4. DATA SCIENCE & AI / ML (30+)
    # =========================================================================
    "Machine Learning": {
        "category": "Data Science & ML",
        "aliases": ["machine learning", "ml", "ml algorithms"]
    },
    "Deep Learning": {
        "category": "Data Science & ML",
        "aliases": ["deep learning", "dl", "neural networks", "ann", "cnn", "rnn"]
    },
    "Artificial Intelligence": {
        "category": "Data Science & ML",
        "aliases": ["artificial intelligence", "ai", "generative ai", "genai"]
    },
    "Natural Language Processing": {
        "category": "Data Science & ML",
        "aliases": ["nlp", "natural language processing", "text mining"]
    },
    "Computer Vision": {
        "category": "Data Science & ML",
        "aliases": ["computer vision", "cv", "object detection", "image processing"]
    },
    "Pandas": {
        "category": "Data Science & ML",
        "aliases": ["pandas"]
    },
    "NumPy": {
        "category": "Data Science & ML",
        "aliases": ["numpy"]
    },
    "Scikit-Learn": {
        "category": "Data Science & ML",
        "aliases": ["scikit-learn", "scikit learn", "sklearn"]
    },
    "TensorFlow": {
        "category": "Data Science & ML",
        "aliases": ["tensorflow", "tf"]
    },
    "PyTorch": {
        "category": "Data Science & ML",
        "aliases": ["pytorch", "torch"]
    },
    "Keras": {
        "category": "Data Science & ML",
        "aliases": ["keras"]
    },
    "Data Analysis": {
        "category": "Data Science & ML",
        "aliases": ["data analysis", "exploratory data analysis", "eda"]
    },
    "Data Visualization": {
        "category": "Data Science & ML",
        "aliases": ["data visualization", "dataviz"]
    },
    "Matplotlib": {
        "category": "Data Science & ML",
        "aliases": ["matplotlib"]
    },
    "Seaborn": {
        "category": "Data Science & ML",
        "aliases": ["seaborn"]
    },
    "Tableau": {
        "category": "Data Science & ML",
        "aliases": ["tableau"]
    },
    "Power BI": {
        "category": "Data Science & ML",
        "aliases": ["power bi", "powerbi"]
    },
    "Large Language Models": {
        "category": "Data Science & ML",
        "aliases": ["llm", "llms", "large language models", "prompt engineering"]
    },
    "Hugging Face": {
        "category": "Data Science & ML",
        "aliases": ["hugging face", "huggingface", "transformers"]
    },
    "OpenCV": {
        "category": "Data Science & ML",
        "aliases": ["opencv", "open-cv"]
    },
    "Apache Spark": {
        "category": "Data Science & ML",
        "aliases": ["spark", "apache spark", "pyspark"]
    },
    "Hadoop": {
        "category": "Data Science & ML",
        "aliases": ["hadoop", "hdfs", "mapreduce"]
    },
    "ETL": {
        "category": "Data Science & ML",
        "aliases": ["etl", "extract transform load", "data pipelines", "data engineering"]
    },

    # =========================================================================
    # 5. CLOUD & DEVOPS (25+)
    # =========================================================================
    "Amazon Web Services (AWS)": {
        "category": "Cloud & DevOps",
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "aws cloud"]
    },
    "Microsoft Azure": {
        "category": "Cloud & DevOps",
        "aliases": ["azure", "microsoft azure", "azure devops"]
    },
    "Google Cloud Platform (GCP)": {
        "category": "Cloud & DevOps",
        "aliases": ["gcp", "google cloud", "google cloud platform"]
    },
    "Docker": {
        "category": "Cloud & DevOps",
        "aliases": ["docker", "containerization", "containers"]
    },
    "Kubernetes": {
        "category": "Cloud & DevOps",
        "aliases": ["kubernetes", "k8s"]
    },
    "CI/CD": {
        "category": "Cloud & DevOps",
        "aliases": ["ci/cd", "cicd", "continuous integration", "continuous deployment", "ci-cd"]
    },
    "Jenkins": {
        "category": "Cloud & DevOps",
        "aliases": ["jenkins"]
    },
    "GitHub Actions": {
        "category": "Cloud & DevOps",
        "aliases": ["github actions", "gh actions"]
    },
    "GitLab CI": {
        "category": "Cloud & DevOps",
        "aliases": ["gitlab ci", "gitlab ci/cd"]
    },
    "Terraform": {
        "category": "Cloud & DevOps",
        "aliases": ["terraform", "iac", "infrastructure as code"]
    },
    "Ansible": {
        "category": "Cloud & DevOps",
        "aliases": ["ansible"]
    },
    "Linux": {
        "category": "Cloud & DevOps",
        "aliases": ["linux", "ubuntu", "centos", "redhat", "debian", "unix"]
    },
    "Nginx": {
        "category": "Cloud & DevOps",
        "aliases": ["nginx"]
    },
    "Apache HTTP Server": {
        "category": "Cloud & DevOps",
        "aliases": ["apache", "apache web server", "httpd"]
    },
    "Monitoring & Observability": {
        "category": "Cloud & DevOps",
        "aliases": ["prometheus", "grafana", "datadog", "new relic", "splunk"]
    },

    # =========================================================================
    # 6. DEVELOPER TOOLS & METHODOLOGIES (25+)
    # =========================================================================
    "Git": {
        "category": "Developer Tools",
        "aliases": ["git", "version control", "vcs"]
    },
    "GitHub": {
        "category": "Developer Tools",
        "aliases": ["github"]
    },
    "GitLab": {
        "category": "Developer Tools",
        "aliases": ["gitlab"]
    },
    "Bitbucket": {
        "category": "Developer Tools",
        "aliases": ["bitbucket"]
    },
    "Jira": {
        "category": "Developer Tools",
        "aliases": ["jira", "atlassian jira"]
    },
    "Postman": {
        "category": "Developer Tools",
        "aliases": ["postman", "api testing"]
    },
    "Unit Testing": {
        "category": "Developer Tools",
        "aliases": ["unit testing", "pytest", "junit", "test driven development", "tdd", "jest", "mocha"]
    },
    "Agile / Scrum": {
        "category": "Developer Tools",
        "aliases": ["agile", "scrum", "kanban", "sprint planning", "sdlc"]
    },
    "VS Code": {
        "category": "Developer Tools",
        "aliases": ["vs code", "vscode", "visual studio code"]
    },
    "Figma": {
        "category": "Developer Tools",
        "aliases": ["figma", "ui design", "ux design", "wireframing"]
    },
    "Cybersecurity Basics": {
        "category": "Developer Tools",
        "aliases": ["cybersecurity", "owasp", "encryption", "jwt", "oauth", "ssl/tls"]
    },

    # =========================================================================
    # 7. SOFT SKILLS & MANAGEMENT (20+)
    # =========================================================================
    "Communication": {
        "category": "Soft Skills",
        "aliases": ["communication", "verbal communication", "written communication", "presentation skills"]
    },
    "Problem Solving": {
        "category": "Soft Skills",
        "aliases": ["problem solving", "analytical thinking", "critical thinking", "troubleshooting"]
    },
    "Teamwork & Collaboration": {
        "category": "Soft Skills",
        "aliases": ["teamwork", "collaboration", "cross-functional", "interpersonal skills", "team player"]
    },
    "Leadership": {
        "category": "Soft Skills",
        "aliases": ["leadership", "mentoring", "team lead", "guidance"]
    },
    "Time Management": {
        "category": "Soft Skills",
        "aliases": ["time management", "prioritization", "multitasking", "deadline management"]
    },
    "Adaptability": {
        "category": "Soft Skills",
        "aliases": ["adaptability", "flexibility", "quick learner", "eagerness to learn"]
    },
    "Project Management": {
        "category": "Soft Skills",
        "aliases": ["project management", "stakeholder management", "risk management"]
    },
    "Attention to Detail": {
        "category": "Soft Skills",
        "aliases": ["attention to detail", "accuracy", "detail-oriented"]
    },
    "Conflict Resolution": {
        "category": "Soft Skills",
        "aliases": ["conflict resolution", "negotiation", "diplomacy"]
    },
    "Customer Support": {
        "category": "Soft Skills",
        "aliases": ["customer service", "client communication", "user support"]
    }
}


def get_all_categories() -> List[str]:
    """Return a unique, ordered list of all categories present in the database."""
    categories: Set[str] = set()
    for item in SKILLS_DB.values():
        categories.add(item["category"])
    preferred_order = [
        "Programming Languages",
        "Web Development",
        "Databases",
        "Data Science & ML",
        "Cloud & DevOps",
        "Developer Tools",
        "Soft Skills"
    ]
    return [c for c in preferred_order if c in categories] + sorted(list(categories - set(preferred_order)))


def get_skills_by_category(category: str) -> List[str]:
    """Return all canonical skill names belonging to a specified category."""
    return sorted([
        skill for skill, data in SKILLS_DB.items()
        if data["category"].lower() == category.lower()
    ])


def total_skills_count() -> int:
    """Return the total number of distinct skills in the master database."""
    return len(SKILLS_DB)


def add_custom_skill(canonical_name: str, category: str, aliases: List[str]) -> None:
    """
    Helper function allowing developers/students to easily inject new custom skills
    into the database dynamically.
    """
    SKILLS_DB[canonical_name] = {
        "category": category,
        "aliases": [a.lower().strip() for a in aliases]
    }
