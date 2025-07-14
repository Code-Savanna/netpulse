FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy configuration files
COPY tailwind.config.js ./
COPY postcss.config.js ./
COPY craco.config.js ./

# Copy source code
COPY . .

EXPOSE 3000

# Use craco for proper Tailwind CSS compilation
CMD ["npm", "start"]
