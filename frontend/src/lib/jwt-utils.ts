/**
 * Utility functions for JWT token handling
 */

/**
 * Decode a JWT token to extract its payload
 * @param token The JWT token string
 * @returns The decoded payload object
 */
export function decodeToken(token: string): any {
  try {
    // Split the token into its three parts: header.payload.signature
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token format');
    }

    // The payload is the second part (index 1)
    // It's base64url encoded, so we need to convert it
    const payload = parts[1];

    // Replace URL-safe base64 characters with standard base64
    let base64 = payload.replace(/-/g, '+').replace(/_/g, '/');

    // Add padding if needed
    let pad = base64.length % 4;
    if (pad) {
      if (pad === 1) throw new Error('Invalid token');
      base64 = base64 + new Array(5 - pad).join('=');
    }

    // Decode the base64 string to JSON
    const decodedPayload = atob(base64);
    return JSON.parse(decodedPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    throw new Error('Invalid token');
  }
}

/**
 * Get the user ID from a JWT token
 * @param token The JWT token string
 * @returns The user ID (sub field) from the token
 */
export function getUserIdFromToken(token: string): string {
  const payload = decodeToken(token);
  return payload.sub; // 'sub' is the standard JWT claim for subject/user ID
}

/**
 * Check if a JWT token is expired
 * @param token The JWT token string
 * @returns True if the token is expired, false otherwise
 */
export function isTokenExpired(token: string): boolean {
  try {
    const payload = decodeToken(token);
    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
    return payload.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true; // If we can't decode the token, treat it as expired
  }
}

/**
 * Get the current authenticated user ID from localStorage token
 * @returns The user ID from the stored token, or null if not available/expired
 */
/**
 * Get the stored authentication token from any available location
 * @returns The authentication token string, or null if not available/expired
 */
export function getStoredToken(): string | null {
  // Check for various token storage locations in order of preference
  const token = localStorage.getItem('access_token') ||
                sessionStorage.getItem('access_token') ||
                localStorage.getItem('better-auth.session_token');

  if (!token) {
    return null;
  }

  // Check if token is expired
  if (isTokenExpired(token)) {
    // Clear expired token from all possible locations
    localStorage.removeItem('access_token');
    sessionStorage.removeItem('access_token');
    localStorage.removeItem('better-auth.session_token');
    localStorage.removeItem('user_id');
    sessionStorage.removeItem('user_id');
    return null;
  }

  return token;
}

export function getCurrentUserId(): string | null {
  try {
    const token = getStoredToken();

    if (!token) {
      return null;
    }

    const payload = decodeToken(token);
    return payload.sub || null; // Return the subject (user ID) from the token payload
  } catch (error) {
    console.error('Error getting current user ID:', error);
    return null;
  }
}