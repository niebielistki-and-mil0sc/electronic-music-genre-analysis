# Use a base Node image
FROM node:14-slim

# Set working directory
WORKDIR /app

# Argument to specify environment: production or development
ARG ENV=production

# Copy project files into the Docker image
COPY . /app

# Use the argument to decide which .env file to copy
COPY .env.${ENV} ./.env

# Install dependencies and build the project
RUN npm install
RUN npm run build

# Install serve and set the command to serve the app
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose port 3000
EXPOSE 3000
