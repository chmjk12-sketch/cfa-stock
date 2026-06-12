# ===== Stage 1: Build Frontend =====
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN NEXT_EXPORT=true npx next build

# ===== Stage 2: Python Backend =====
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir aiosqlite

# Copy backend code
COPY backend/ .

# Copy built frontend
COPY --from=frontend-builder /app/frontend/out /app/frontend/out

# Copy entrypoint
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
