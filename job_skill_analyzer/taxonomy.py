"""Skill taxonomy definitions and canonical dictionary.

Provides a structured, maintainable taxonomy of recognized skills,
their categories, default weights, and normalization aliases.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from job_skill_analyzer.models import PriorityLevel, SkillCategory, SkillDefinition

# Standard technical skill taxonomy
SKILL_DEFINITIONS: Tuple[SkillDefinition, ...] = (
    # --- PROGRAMMING LANGUAGES ---
    SkillDefinition(
        name="Python",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("python", "python3", "py"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Java",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("java", "core java", "java8", "java11", "java17"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="JavaScript",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("javascript", "js", "ecmascript", "es6"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="TypeScript",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("typescript", "ts"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="C++",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("c++", "cpp"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="C#",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("c#", "csharp", "c-sharp"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="C",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("c", "ansi c"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Go",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("go", "golang"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Rust",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("rust", "rustlang"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="PHP",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("php", "php7", "php8"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Ruby",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("ruby",),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="SQL",
        category=SkillCategory.PROGRAMMING_LANGUAGE,
        aliases=("sql", "structured query language"),
        default_weight=PriorityLevel.HIGH,
    ),

    # --- FRAMEWORKS / LIBRARIES ---
    SkillDefinition(
        name="React",
        category=SkillCategory.FRAMEWORK,
        aliases=("react", "react.js", "reactjs"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Angular",
        category=SkillCategory.FRAMEWORK,
        aliases=("angular", "angular.js", "angularjs", "angular2+"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Vue",
        category=SkillCategory.FRAMEWORK,
        aliases=("vue", "vue.js", "vuejs", "vue3"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Node.js",
        category=SkillCategory.FRAMEWORK,
        aliases=("node.js", "nodejs", "node"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Express",
        category=SkillCategory.FRAMEWORK,
        aliases=("express", "express.js", "expressjs"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="FastAPI",
        category=SkillCategory.FRAMEWORK,
        aliases=("fastapi", "fast api"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Flask",
        category=SkillCategory.FRAMEWORK,
        aliases=("flask",),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Django",
        category=SkillCategory.FRAMEWORK,
        aliases=("django", "django rest framework", "drf"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Spring",
        category=SkillCategory.FRAMEWORK,
        aliases=("spring", "spring boot", "spring framework", "springboot"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name=".NET",
        category=SkillCategory.FRAMEWORK,
        aliases=(".net", "dotnet", ".net core", "asp.net", "asp.net core"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="TensorFlow",
        category=SkillCategory.FRAMEWORK,
        aliases=("tensorflow", "tf"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="PyTorch",
        category=SkillCategory.FRAMEWORK,
        aliases=("pytorch", "torch"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="scikit-learn",
        category=SkillCategory.FRAMEWORK,
        aliases=("scikit-learn", "sklearn", "scikit learn"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Pandas",
        category=SkillCategory.FRAMEWORK,
        aliases=("pandas",),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="NumPy",
        category=SkillCategory.FRAMEWORK,
        aliases=("numpy",),
        default_weight=PriorityLevel.MEDIUM,
    ),

    # --- DATABASES ---
    SkillDefinition(
        name="PostgreSQL",
        category=SkillCategory.DATABASE,
        aliases=(
            "postgresql",
            "postgres",
            "postgres db",
            "postgres database",
            "pgsql",
            "postgresql database",
        ),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="MySQL",
        category=SkillCategory.DATABASE,
        aliases=("mysql", "my sql", "mysql database"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="MongoDB",
        category=SkillCategory.DATABASE,
        aliases=("mongodb", "mongo", "mongo db", "mongodb database"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Redis",
        category=SkillCategory.DATABASE,
        aliases=("redis", "redis cache"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="SQLite",
        category=SkillCategory.DATABASE,
        aliases=("sqlite", "sqlite3"),
        default_weight=PriorityLevel.LOW,
    ),
    SkillDefinition(
        name="Oracle",
        category=SkillCategory.DATABASE,
        aliases=("oracle", "oracle db", "oracle database"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="SQL Server",
        category=SkillCategory.DATABASE,
        aliases=(
            "sql server",
            "ms sql",
            "mssql",
            "ms sql server",
            "microsoft sql server",
        ),
        default_weight=PriorityLevel.MEDIUM,
    ),

    # --- CLOUD ---
    SkillDefinition(
        name="AWS",
        category=SkillCategory.CLOUD,
        aliases=("aws", "amazon web services"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Azure",
        category=SkillCategory.CLOUD,
        aliases=("azure", "microsoft azure"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Google Cloud",
        category=SkillCategory.CLOUD,
        aliases=("google cloud", "gcp", "google cloud platform"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="EC2",
        category=SkillCategory.CLOUD,
        aliases=("ec2", "amazon ec2", "aws ec2"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="S3",
        category=SkillCategory.CLOUD,
        aliases=("s3", "amazon s3", "aws s3"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Lambda",
        category=SkillCategory.CLOUD,
        aliases=("lambda", "aws lambda", "serverless lambda"),
        default_weight=PriorityLevel.MEDIUM,
    ),

    # --- DEVOPS / INFRASTRUCTURE ---
    SkillDefinition(
        name="Docker",
        category=SkillCategory.DEVOPS,
        aliases=("docker", "docker containers", "docker containerization"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Kubernetes",
        category=SkillCategory.DEVOPS,
        aliases=("kubernetes", "k8s"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Jenkins",
        category=SkillCategory.DEVOPS,
        aliases=("jenkins", "jenkins ci"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="GitHub Actions",
        category=SkillCategory.DEVOPS,
        aliases=("github actions", "gh actions", "github action"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Terraform",
        category=SkillCategory.DEVOPS,
        aliases=("terraform", "iac terraform"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="CI/CD",
        category=SkillCategory.DEVOPS,
        aliases=(
            "ci/cd",
            "cicd",
            "ci-cd",
            "ci / cd",
            "continuous integration",
            "continuous deployment",
        ),
        default_weight=PriorityLevel.MEDIUM,
    ),

    # --- API / BACKEND ---
    SkillDefinition(
        name="REST API",
        category=SkillCategory.API_BACKEND,
        aliases=(
            "rest api",
            "restful api",
            "rest apis",
            "restful apis",
            "restful",
            "rest",
        ),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="GraphQL",
        category=SkillCategory.API_BACKEND,
        aliases=("graphql", "graph ql"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="WebSocket",
        category=SkillCategory.API_BACKEND,
        aliases=("websocket", "websockets", "web socket", "web sockets"),
        default_weight=PriorityLevel.MEDIUM,
    ),
    SkillDefinition(
        name="Microservices",
        category=SkillCategory.API_BACKEND,
        aliases=("microservices", "micro-services", "microservice", "microservice architecture"),
        default_weight=PriorityLevel.HIGH,
    ),

    # --- AI / DATA ---
    SkillDefinition(
        name="Machine Learning",
        category=SkillCategory.AI_DATA,
        aliases=("machine learning", "ml"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Deep Learning",
        category=SkillCategory.AI_DATA,
        aliases=("deep learning", "dl"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Natural Language Processing",
        category=SkillCategory.AI_DATA,
        aliases=("natural language processing", "nlp"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Computer Vision",
        category=SkillCategory.AI_DATA,
        aliases=("computer vision", "cv"),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Data Science",
        category=SkillCategory.AI_DATA,
        aliases=("data science",),
        default_weight=PriorityLevel.HIGH,
    ),
    SkillDefinition(
        name="Data Analysis",
        category=SkillCategory.AI_DATA,
        aliases=("data analysis", "data analytics"),
        default_weight=PriorityLevel.MEDIUM,
    ),

    # --- TOOLS / DEVELOPMENT ---
    SkillDefinition(
        name="Git",
        category=SkillCategory.TOOLS,
        aliases=("git", "git version control"),
        default_weight=PriorityLevel.LOW,
    ),
    SkillDefinition(
        name="GitHub",
        category=SkillCategory.TOOLS,
        aliases=("github",),
        default_weight=PriorityLevel.LOW,
    ),
    SkillDefinition(
        name="GitLab",
        category=SkillCategory.TOOLS,
        aliases=("gitlab",),
        default_weight=PriorityLevel.LOW,
    ),
    SkillDefinition(
        name="Linux",
        category=SkillCategory.TOOLS,
        aliases=("linux", "gnu/linux", "unix"),
        default_weight=PriorityLevel.MEDIUM,
    ),
)


def get_canonical_map() -> Dict[str, str]:
    """Build a mapping from all lowercased terms/aliases to their canonical name.

    Returns:
        Dictionary mapping lowercased alias/name to canonical name.
    """
    canonical_map: Dict[str, str] = {}
    for item in SKILL_DEFINITIONS:
        # Map canonical name itself (lowercased)
        canonical_map[item.name.lower()] = item.name
        for alias in item.aliases:
            canonical_map[alias.lower()] = item.name
    return canonical_map


def get_definition_map() -> Dict[str, SkillDefinition]:
    """Build a mapping from canonical skill names to their full SkillDefinition.

    Returns:
        Dictionary mapping canonical name to SkillDefinition.
    """
    return {item.name: item for item in SKILL_DEFINITIONS}


def get_skills_by_category() -> Dict[SkillCategory, List[str]]:
    """Group canonical skill names by their respective category.

    Returns:
        Dictionary mapping SkillCategory to a list of canonical skill names.
    """
    categorized: Dict[SkillCategory, List[str]] = {cat: [] for cat in SkillCategory}
    for item in SKILL_DEFINITIONS:
        categorized[item.category].append(item.name)
    return categorized
