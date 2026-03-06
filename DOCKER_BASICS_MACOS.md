# 🐳 Basic Docker Commands for macOS

## Prerequisites
1. **Install Docker Desktop for Mac**: Download from [docker.com](https://www.docker.com/products/docker-desktop/)
2. After installation, launch Docker Desktop and wait for it to start (whale icon in menu bar)

---

## 🔑 Essential Docker Commands

### 1. Check Docker Installation
```bash
docker --version
docker info
```

### 2. Pull an Image
Download a pre-built image from Docker Hub:
```bash
docker pull hello-world
docker pull python:3.10 
```

### 3. List Images
```bash
docker images
```

### 4. Run a Container
```bash
# Simple run
docker run hello-world

# Run interactively with terminal
docker run -it python:3.10 bash

# Run in background (detached)
docker run -d nginx
```

### 5. List Running Containers
```bash
# Running containers only
docker ps

# All containers (including stopped)
docker ps -a
```

### 6. Stop a Container
```bash
docker stop <container_id_or_name>
```

### 7. Remove a Container
```bash
docker rm <container_id_or_name>

# Force remove running container
docker rm -f <container_id_or_name>
```

### 8. Remove an Image
```bash
docker rmi <image_name>
```

---

## 🏗️ Building Images

### Build from Dockerfile
```bash
# In directory with Dockerfile
docker build -t my-app-name .

# With specific tag
docker build -t my-app-name:v1.0 .
```

---

## 📁 Volume Mounting (Share Files)
```bash
# Mount current directory to /app in container
docker run -v $(pwd):/app python:3.10 bash
```

---

## 🌐 Port Mapping
```bash
# Map host port 8080 to container port 80
docker run -p 8080:80 nginx
```

---

## 🧹 Cleanup Commands
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything unused (careful!)
docker system prune
```

---

## 📝 Quick Reference Table

| Command | Description |
|---------|-------------|
| `docker pull <image>` | Download image |
| `docker run <image>` | Create & start container |
| `docker ps` | List running containers |
| `docker stop <id>` | Stop container |
| `docker rm <id>` | Remove container |
| `docker images` | List images |
| `docker rmi <image>` | Remove image |
| `docker build -t <name> .` | Build image |
| `docker logs <id>` | View container logs |
| `docker exec -it <id> bash` | Enter running container |

---

## 🎯 Practice Exercise

1. Pull the `hello-world` image
2. Run it
3. Check `docker ps -a` to see the container
4. Remove the container
5. Remove the image

```bash
docker pull hello-world
docker run hello-world
docker ps -a
docker rm <container_id>
docker rmi hello-world
```

---

## Next Step
Once comfortable with these basics, proceed to setting up the **ShortGPT** project using the project's `Dockerfile`.
