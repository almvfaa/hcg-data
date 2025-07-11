# ---- Builder Stage ----
# This stage installs build-time dependencies and compiles Python packages.
FROM python:3.11-slim AS builder

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS-level dependencies required for compiling some Python packages (e.g., psycopg2)
# Using --no-install-recommends keeps the image lean.
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev

WORKDIR /app

# Copy only the requirements file to leverage Docker's layer caching.
# This layer only gets rebuilt if requirements.txt changes.
COPY requirements.txt .

# Create a wheelhouse for all dependencies.
# This pre-compiles the packages for faster installation in the final stage.
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# ---- Final Stage ----
# This is the small, secure image that will run in production.
FROM python:3.11-slim

# Create a non-privileged user to run the application for better security.
RUN addgroup --system app && adduser --system --no-create-home --ingroup app appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/appuser
ENV APP_HOME=/home/appuser/web
ENV PYTHONPATH "${PYTHONPATH}:${APP_HOME}"

# Create the working directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Copy the pre-compiled wheels from the builder stage.
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the dependencies from the wheels.
# This is much faster than compiling them again.
RUN pip install --no-cache /wheels/*

# Copy the application code into the final image.
COPY . .

# Copy the start-up script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Change ownership of the app directory to the non-privileged user.
RUN chown -R appuser:app $APP_HOME
RUN chown appuser:app /start.sh

# Switch to the non-privileged user.
USER appuser

# Expose the port the application runs on.
EXPOSE 8000

# The command to run the application using Gunicorn for production.
# Note: Ensure 'main:app' matches your application's entrypoint.
CMD ["/start.sh"]
