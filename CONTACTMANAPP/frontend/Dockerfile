# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./

# Install all dependencies
RUN npm install

# Copy the rest of the files
COPY . .

# Build the react app
RUN npm run build

# Install and use a simple HTTP server for the frontend
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the build folder
CMD ["serve", "-s", "build", "-l", "3000"]

