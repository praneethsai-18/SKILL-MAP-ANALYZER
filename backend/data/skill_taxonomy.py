# data/skill_taxonomy.py
# Master skill taxonomy — 500+ skills used by spaCy matcher + BERT

SKILL_TAXONOMY = {
    "languages": {
        "weight": 1.0,
        "color": "#6c63ff",
        "skills": [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C",
            "Go", "Rust", "Kotlin", "Swift", "Ruby", "PHP", "Scala", "R",
            "MATLAB", "Perl", "Haskell", "Dart", "Lua", "Julia", "Groovy",
            "Bash", "Shell", "PowerShell", "SQL", "PL/SQL", "T-SQL",
            "GraphQL", "HTML", "CSS", "SASS", "LESS", "Solidity"
        ]
    },
    "frontend": {
        "weight": 0.95,
        "color": "#00d4aa",
        "skills": [
            "React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte",
            "Redux", "Zustand", "Recoil", "MobX", "React Query", "SWR",
            "Tailwind CSS", "Bootstrap", "Material UI", "Ant Design",
            "Chakra UI", "Styled Components", "Framer Motion", "GSAP",
            "Three.js", "D3.js", "Recharts", "Chart.js", "Storybook",
            "Webpack", "Vite", "Parcel", "Jest", "Cypress", "Playwright",
            "React Testing Library", "Vitest", "Gatsby", "Remix", "Astro"
        ]
    },
    "backend": {
        "weight": 0.95,
        "color": "#4db8ff",
        "skills": [
            "Node.js", "Express.js", "FastAPI", "Django", "Flask", "FastAPI",
            "Spring Boot", "Spring MVC", "Laravel", "Ruby on Rails",
            "ASP.NET", "NestJS", "Fastify", "Koa", "Hapi.js",
            "REST API", "GraphQL API", "gRPC", "WebSockets",
            "Microservices", "Event-Driven Architecture", "CQRS",
            "Domain-Driven Design", "JWT", "OAuth2", "OpenID Connect"
        ]
    },
    "ml_ai": {
        "weight": 1.0,
        "color": "#ffd166",
        "skills": [
            "Machine Learning", "Deep Learning", "Neural Networks",
            "Natural Language Processing", "NLP", "Computer Vision",
            "Reinforcement Learning", "Transfer Learning",
            "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
            "Hugging Face", "Transformers", "BERT", "GPT", "LLaMA",
            "XGBoost", "LightGBM", "CatBoost", "Random Forest",
            "Feature Engineering", "Model Deployment", "MLOps",
            "MLflow", "Weights and Biases", "DVC", "Kubeflow",
            "OpenCV", "NLTK", "spaCy", "Gensim",
            "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
            "Plotly", "Jupyter", "Google Colab", "ONNX"
        ]
    },
    "data_engineering": {
        "weight": 0.95,
        "color": "#ff6b6b",
        "skills": [
            "Apache Spark", "Apache Kafka", "Apache Flink", "Apache Airflow",
            "Apache Hadoop", "Apache Hive", "dbt", "Fivetran", "Airbyte",
            "Snowflake", "BigQuery", "Redshift", "Databricks", "Delta Lake",
            "Apache Iceberg", "Tableau", "Power BI", "Looker", "Metabase",
            "ETL", "ELT", "Data Pipelines", "Stream Processing",
            "Data Modeling", "Data Warehousing", "Data Lake",
            "Data Quality", "Data Governance", "dask"
        ]
    },
    "databases": {
        "weight": 0.9,
        "color": "#c084fc",
        "skills": [
            "PostgreSQL", "MySQL", "SQLite", "MariaDB", "Oracle",
            "Microsoft SQL Server", "MongoDB", "Cassandra", "DynamoDB",
            "Redis", "Memcached", "Elasticsearch", "Neo4j",
            "Firebase", "Supabase", "InfluxDB", "ClickHouse",
            "Pinecone", "Weaviate", "ChromaDB", "pgvector",
            "Database Design", "Query Optimization", "Indexing", "Sharding"
        ]
    },
    "cloud_devops": {
        "weight": 0.9,
        "color": "#38bdf8",
        "skills": [
            "AWS", "Google Cloud Platform", "Microsoft Azure",
            "AWS Lambda", "AWS EC2", "AWS S3", "AWS ECS", "AWS EKS",
            "AWS RDS", "AWS CloudFormation",
            "Docker", "Kubernetes", "Helm", "Istio",
            "Terraform", "Ansible", "Pulumi",
            "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI",
            "CircleCI", "ArgoCD", "Prometheus", "Grafana",
            "ELK Stack", "Datadog", "Linux", "Bash Scripting",
            "Infrastructure as Code", "Site Reliability Engineering",
            "DevSecOps", "GitOps", "Nginx", "Apache"
        ]
    },
    "mobile": {
        "weight": 0.9,
        "color": "#f472b6",
        "skills": [
            "React Native", "Flutter", "Swift", "SwiftUI", "Kotlin",
            "Jetpack Compose", "Android SDK", "iOS", "Expo",
            "Firebase", "Push Notifications", "App Store Deployment"
        ]
    },
    "security": {
        "weight": 0.85,
        "color": "#ef4444",
        "skills": [
            "Cybersecurity", "Penetration Testing", "OWASP",
            "Network Security", "Application Security", "Cloud Security",
            "Cryptography", "SSL/TLS", "OAuth2", "JWT", "SAML",
            "Zero Trust", "IAM", "RBAC", "CISSP", "CEH",
            "SOC 2", "ISO 27001", "GDPR", "HIPAA"
        ]
    },
    "soft_skills": {
        "weight": 0.5,
        "color": "#94a3b8",
        "skills": [
            "Leadership", "Team Management", "Mentoring",
            "Communication", "Technical Writing", "Presentation",
            "Problem Solving", "Critical Thinking", "Agile", "Scrum",
            "Project Management", "Stakeholder Management",
            "Cross-functional Collaboration", "Time Management"
        ]
    }
}

# Role requirement profiles — what each role needs
ROLE_PROFILES = {
    "Frontend Engineer": {
        "required": ["JavaScript", "TypeScript", "React", "CSS", "HTML",
                     "Redux", "Jest", "Git", "REST API", "Webpack", "Vite"],
        "nice_to_have": ["Next.js", "GraphQL", "Cypress", "Storybook",
                         "React Testing Library", "Tailwind CSS", "Figma"],
        "category_weights": {
            "languages": 0.25, "frontend": 0.40, "backend": 0.10,
            "cloud_devops": 0.10, "databases": 0.05, "soft_skills": 0.10
        },
        "salary_range": "INR 8-22 LPA / $70k-$130k"
    },
    "Backend Engineer": {
        "required": ["Python", "Node.js", "PostgreSQL", "Redis", "Docker",
                     "AWS", "REST API", "Git", "SQL", "System Design"],
        "nice_to_have": ["Go", "Kafka", "Kubernetes", "gRPC", "GraphQL",
                         "Elasticsearch", "Microservices"],
        "category_weights": {
            "languages": 0.25, "frontend": 0.05, "backend": 0.35,
            "cloud_devops": 0.15, "databases": 0.15, "soft_skills": 0.05
        },
        "salary_range": "INR 10-25 LPA / $80k-$150k"
    },
    "Full Stack Developer": {
        "required": ["JavaScript", "TypeScript", "React", "Node.js",
                     "PostgreSQL", "MongoDB", "REST API", "Docker", "Git", "SQL"],
        "nice_to_have": ["GraphQL", "Redis", "AWS", "Next.js", "CI/CD"],
        "category_weights": {
            "languages": 0.20, "frontend": 0.25, "backend": 0.25,
            "cloud_devops": 0.10, "databases": 0.15, "soft_skills": 0.05
        },
        "salary_range": "INR 12-28 LPA / $90k-$160k"
    },
    "Data Scientist": {
        "required": ["Python", "Machine Learning", "Pandas", "NumPy",
                     "Scikit-learn", "SQL", "Matplotlib", "Jupyter",
                     "Statistics", "Feature Engineering"],
        "nice_to_have": ["TensorFlow", "PyTorch", "Spark", "MLflow",
                         "Deep Learning", "NLP"],
        "category_weights": {
            "languages": 0.20, "ml_ai": 0.45, "data_engineering": 0.15,
            "databases": 0.10, "cloud_devops": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 12-30 LPA / $90k-$160k"
    },
    "ML Engineer": {
        "required": ["Python", "PyTorch", "TensorFlow", "Machine Learning",
                     "Deep Learning", "MLOps", "Docker", "AWS", "Git", "SQL"],
        "nice_to_have": ["Hugging Face", "Transformers", "ONNX", "Kubeflow",
                         "Feature Engineering", "Kubernetes", "Spark"],
        "category_weights": {
            "languages": 0.20, "ml_ai": 0.40, "cloud_devops": 0.20,
            "data_engineering": 0.10, "databases": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 15-40 LPA / $110k-$200k"
    },
    "Data Engineer": {
        "required": ["Python", "SQL", "Apache Spark", "Apache Kafka",
                     "Apache Airflow", "dbt", "Snowflake", "Docker", "Git"],
        "nice_to_have": ["Scala", "Apache Flink", "Delta Lake", "Databricks",
                         "BigQuery", "Terraform", "dask"],
        "category_weights": {
            "languages": 0.20, "data_engineering": 0.40, "databases": 0.20,
            "cloud_devops": 0.10, "ml_ai": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 12-32 LPA / $100k-$175k"
    },
    "DevOps Engineer": {
        "required": ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD",
                     "GitHub Actions", "Linux", "Bash", "Python", "Git"],
        "nice_to_have": ["ArgoCD", "Helm", "Ansible", "Prometheus",
                         "Grafana", "ELK Stack", "Istio"],
        "category_weights": {
            "languages": 0.15, "cloud_devops": 0.55, "backend": 0.15,
            "databases": 0.05, "security": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 10-28 LPA / $90k-$160k"
    },
    "Cloud Architect": {
        "required": ["AWS", "Terraform", "Kubernetes", "Docker",
                     "Microservices", "System Design", "Security",
                     "Networking", "CI/CD", "Infrastructure as Code"],
        "nice_to_have": ["Google Cloud Platform", "Azure", "Pulumi",
                         "Service Mesh", "FinOps"],
        "category_weights": {
            "languages": 0.10, "cloud_devops": 0.55, "backend": 0.15,
            "security": 0.10, "databases": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 20-50 LPA / $130k-$220k"
    },
    "Cybersecurity Analyst": {
        "required": ["Cybersecurity", "Penetration Testing", "OWASP",
                     "Network Security", "Linux", "Python", "Bash",
                     "Application Security", "AWS", "Git"],
        "nice_to_have": ["CISSP", "CEH", "OSCP", "SIEM", "SOC",
                         "Docker", "Kubernetes Security"],
        "category_weights": {
            "security": 0.50, "languages": 0.15, "cloud_devops": 0.20,
            "databases": 0.05, "backend": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 8-22 LPA / $75k-$140k"
    },
    "Mobile Developer": {
        "required": ["React Native", "JavaScript", "TypeScript",
                     "Redux", "REST API", "Firebase", "Git", "iOS", "Android"],
        "nice_to_have": ["Swift", "Kotlin", "Expo", "Push Notifications",
                         "App Store Deployment"],
        "category_weights": {
            "languages": 0.20, "mobile": 0.50, "backend": 0.10,
            "databases": 0.10, "cloud_devops": 0.05, "soft_skills": 0.05
        },
        "salary_range": "INR 8-22 LPA / $80k-$140k"
    },
    "UI/UX Designer": {
        "required": ["Figma", "UI Design", "UX Design", "Wireframing",
                     "Prototyping", "User Research", "Design Systems",
                     "Accessibility", "Communication"],
        "nice_to_have": ["Adobe XD", "Framer", "Motion Design",
                         "HTML", "CSS", "A/B Testing"],
        "category_weights": {
            "frontend": 0.30, "soft_skills": 0.30, "languages": 0.10,
            "backend": 0.05, "cloud_devops": 0.05, "databases": 0.05
        },
        "salary_range": "INR 6-18 LPA / $60k-$120k"
    },
    "Product Manager": {
        "required": ["Product Thinking", "Agile", "Scrum",
                     "Stakeholder Management", "Communication",
                     "Problem Solving", "SQL", "Leadership"],
        "nice_to_have": ["Python", "Data Analysis", "Figma", "JIRA", "OKRs"],
        "category_weights": {
            "soft_skills": 0.50, "databases": 0.15, "languages": 0.10,
            "frontend": 0.10, "cloud_devops": 0.05, "ml_ai": 0.10
        },
        "salary_range": "INR 12-35 LPA / $100k-$180k"
    },
    "Data Analyst": {
        "required": ["SQL", "Python", "Tableau", "Power BI", "Excel",
                     "Pandas", "Statistics", "Data Visualization", "Git"],
        "nice_to_have": ["Looker", "BigQuery", "Snowflake", "dbt",
                         "Machine Learning", "R"],
        "category_weights": {
            "languages": 0.20, "data_engineering": 0.25, "ml_ai": 0.25,
            "databases": 0.20, "soft_skills": 0.10
        },
        "salary_range": "INR 5-15 LPA / $55k-$100k"
    }
}

# Course recommendations per skill
COURSE_RECOMMENDATIONS = {
    "Python": [
        {"title": "Python for Everybody", "platform": "Coursera", "duration": "8 months", "free": False},
        {"title": "Python Full Course", "platform": "YouTube (freeCodeCamp)", "duration": "4h", "free": True}
    ],
    "React": [
        {"title": "React - The Complete Guide", "platform": "Udemy", "duration": "48h", "free": False},
        {"title": "React Official Tutorial", "platform": "react.dev", "duration": "Self-paced", "free": True}
    ],
    "Machine Learning": [
        {"title": "ML Specialization", "platform": "Coursera (Andrew Ng)", "duration": "3 months", "free": False},
        {"title": "Kaggle ML Courses", "platform": "Kaggle", "duration": "Self-paced", "free": True}
    ],
    "Docker": [
        {"title": "Docker & Kubernetes Guide", "platform": "Udemy", "duration": "24h", "free": False},
        {"title": "Docker Official Get Started", "platform": "docs.docker.com", "duration": "Self-paced", "free": True}
    ],
    "AWS": [
        {"title": "AWS Certified Developer", "platform": "Coursera", "duration": "4 months", "free": False},
        {"title": "AWS Free Tier Tutorials", "platform": "aws.amazon.com", "duration": "Self-paced", "free": True}
    ],
    "PostgreSQL": [
        {"title": "PostgreSQL Bootcamp", "platform": "Udemy", "duration": "20h", "free": False},
        {"title": "PostgreSQL Full Tutorial", "platform": "YouTube (freeCodeCamp)", "duration": "4h", "free": True}
    ],
    "PyTorch": [
        {"title": "PyTorch for Deep Learning", "platform": "Udemy", "duration": "25h", "free": False},
        {"title": "PyTorch Official Tutorials", "platform": "pytorch.org", "duration": "Self-paced", "free": True}
    ],
    "Apache Spark": [
        {"title": "Apache Spark with Python", "platform": "Udemy", "duration": "12h", "free": False},
        {"title": "Spark Official Docs", "platform": "spark.apache.org", "duration": "Self-paced", "free": True}
    ],
    "Kubernetes": [
        {"title": "Kubernetes Certified Developer", "platform": "Udemy", "duration": "16h", "free": False},
        {"title": "Kubernetes Official Tutorial", "platform": "kubernetes.io", "duration": "Self-paced", "free": True}
    ],
    "TensorFlow": [
        {"title": "Deep Learning Specialization", "platform": "Coursera (DeepLearning.AI)", "duration": "5 months", "free": False},
        {"title": "TensorFlow Official Tutorials", "platform": "tensorflow.org", "duration": "Self-paced", "free": True}
    ]
}

def get_courses_for_skill(skill_name: str) -> list:
    """Return course recommendations for a skill."""
    if skill_name in COURSE_RECOMMENDATIONS:
        return COURSE_RECOMMENDATIONS[skill_name]
    return [
        {"title": f"Learn {skill_name} — Official Documentation", "platform": "Official Docs", "duration": "Self-paced", "free": True},
        {"title": f"{skill_name} Full Course", "platform": "YouTube", "duration": "3-10h", "free": True},
        {"title": f"{skill_name} Bootcamp", "platform": "Udemy", "duration": "10-20h", "free": False}
    ]

def get_all_skills() -> list:
    """Return flat list of all skills."""
    return [skill for cat in SKILL_TAXONOMY.values() for skill in cat["skills"]]

def get_skill_category(skill_name: str) -> str:
    """Return category name for a skill."""
    for cat_name, cat_data in SKILL_TAXONOMY.items():
        if any(s.lower() == skill_name.lower() for s in cat_data["skills"]):
            return cat_name
    return "general"

def get_skill_weight(skill_name: str) -> float:
    """Return scoring weight for a skill."""
    for cat_data in SKILL_TAXONOMY.values():
        if any(s.lower() == skill_name.lower() for s in cat_data["skills"]):
            return cat_data["weight"]
    return 0.5
