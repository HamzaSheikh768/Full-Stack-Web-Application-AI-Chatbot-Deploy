FROM node:20-alpine

# Set the working directory
WORKDIR /src

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install only production dependencies
RUN npm install --only=production

# Install development dependencies for building the app
RUN npm install

# Copy the rest of the application code
COPY . .

# ensure environment variables are available
COPY .env .env

# Expose the port the app runs on
EXPOSE 3000

# Set environment variables for production
ENV NODE_ENV=production

# Start the Next.js application in production mode
CMD ["npm", "start"]