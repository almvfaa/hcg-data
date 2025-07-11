#!/bin/bash

# Function to check command existence
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python
if command_exists python; then
    echo "Python is installed: $(python --version)"
else
    echo "Python is not installed."
fi

# Check for Node.js
if command_exists node; then
    echo "Node.js is installed: $(node --version)"
else
    echo "Node.js is not installed."
fi

# Check for npm
if command_exists npm; then
    echo "npm is installed: $(npm --version)"
else
    echo "npm is not installed."
fi

# Check for PostgreSQL
if command_exists psql; then
    echo "PostgreSQL is installed: $(psql --version)"
else
    echo "PostgreSQL is not installed."
fi

# Check for DATABASE_URL environment variable
if [ -n "$DATABASE_URL" ]; then
    echo "DATABASE_URL is set to: $DATABASE_URL"
else
    echo "DATABASE_URL is not set."
fi

# Check if backend dependencies are installed
if [ -d "backend/venv" ]; then
    echo "Backend virtual environment exists."
else
    echo "Backend virtual environment does not exist. Did 'pip install -r backend/requirements.txt' run?"
fi

# Check if frontend dependencies are installed
if [ -d "frontend/node_modules" ]; then
    echo "Frontend dependencies are installed."
else
    echo "Frontend dependencies are not installed. Did 'npm install --prefix frontend' run?"
fi

# Check if PostgreSQL is ready
if pg_isready -q -h localhost -p 5432 -U postgres; then
    echo "PostgreSQL is running."
else
    echo "PostgreSQL is not running."
fi

# Check if the database schema is applied
if psql "$DATABASE_URL" -c "\dt" | grep -q "articulo"; then
    echo "Database schema appears to be applied."
else
    echo "Database schema does not appear to be applied."
fi
