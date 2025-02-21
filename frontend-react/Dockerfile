# Build stage
FROM node:20-slim as development

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including devDependencies)
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Production stage
FROM node:20-slim as production

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --production

# Copy built files
COPY . .

# Build the app
RUN npm run build

# Use nginx to serve the app
FROM nginx:alpine as nginx

# Copy built files
COPY --from=production /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 