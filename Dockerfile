
# Use latest Python image
FROM python:latest

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt update && apt upgrade -y && \
    apt install -y git python3-pip ffmpeg

# Copy requirements and install them
COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Copy rest of the files
COPY . .

# Expose port for Render (only needed for webhook servers)
EXPOSE 8080

# Run the bot
CMD ["python3", "bot.py"]
