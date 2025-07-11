# ---- Base Image ----
# This is the small, secure image that will run in production.
FROM python:3.11-slim

# ---- Set Working Directory ----
# Set the working directory inside the container.
WORKDIR /app

# ---- Environment Variables ----
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/appuser
ENV APP_HOME=/home/appuser/web
ENV PYTHONPATH="/app"

# ---- Install Dependencies ----
# Copy only the requirements file to leverage Docker's layer caching.
# This layer only gets rebuilt if requirements.txt changes.
COPY requirements.txt .

# Install the dependencies.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ---- Copy Application Code ----
# Copy the application code into the final image.
COPY . .

# ---- Copy Start-up Script ----
# Copy the start-up script and make it executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# ---- Command to Run the Application ----
# Use the script to start the service
CMD ["/app/start.sh"]
