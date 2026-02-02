#!/usr/bin/env node

// Check the JWT token to see what user ID it contains
const jwt = require('jsonwebtoken');

// This is a sample token from our earlier successful login
// In a real scenario, you'd get this from localStorage
const sampleToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYTdkNGM3Mi1hOGJjLTRjMjctYmEyZS0zNWRmNjU2YzU1MTIiLCJlbWFpbCI6InRlc3R1c2VyOUBleGFtcGxlLmNvbSIsImV4cCI6MTc2OTcwODE0MX0.hYQsVsrqN5m37o6gjYL8M1Vsm1knyxnDd1rZtEzEaU0";

try {
    // Decode the token without verifying (just to see the contents)
    const decoded = jwt.decode(sampleToken);
    console.log('Decoded token payload:', decoded);
    console.log('User ID from token (sub):', decoded.sub);
} catch (error) {
    console.error('Error decoding token:', error);
}