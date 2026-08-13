# --- Stage 1: Build Stage ---
FROM node:20-alpine AS builder

WORKDIR /app

# 1. Install dependencies (cached if package files don't change)
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# 2. Copy source files and build static assets
COPY . .
RUN npm run build

# --- Stage 2: Production Runner Stage ---
FROM nginx:alpine AS runner

# Copy custom Nginx configuration if needed, or use default public dir
# Copy built static files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]