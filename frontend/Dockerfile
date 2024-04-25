# Use an official Node.js runtime as a parent image
FROM node:14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in package.json
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variables
ENV NODE_ENV=production

# Build the app
RUN npm run build

# Install serve to serve the built application
RUN npm install -g serve

# Run serve when the container launches
CMD ["serve", "-s", "build", "-l", "3000"]
