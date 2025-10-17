# Development Dockerfile for NoteHub Frontend
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY package*.json ./

# Copy all files
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start development server
# The --host flag allows access from outside the container
CMD ["sh", "-c", "npm install && npm run dev -- --host"]
