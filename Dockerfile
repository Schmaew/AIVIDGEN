# =============================================================================
# AIVidGen/ShortGPT Docker Image
# =============================================================================

FROM python:3.11-slim-bullseye

# Install FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages not in requirements.txt
RUN pip install --no-cache-dir google-genai

# Copy the entire project
COPY . /app

# Create necessary directories
RUN mkdir -p /app/videos /app/.database /app/.logs

# Expose the Gradio port
EXPOSE 31415

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the main application
CMD ["python", "-u", "./runShortGPT.py"]