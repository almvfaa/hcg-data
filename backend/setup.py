from setuptools import setup, find_packages

setup(
    name="backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "psycopg2-binary",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "pydantic-settings",
        "celery",
        "redis",
        "pandas",
        "scikit-learn",
        "prophet"
    ],
)
