import { Task } from '../models';

// Simple in-memory cache implementation
// In production, you would use Redis or similar
class InMemoryCache {
  private cache: Map<string, any> = new Map();
  private timeouts: Map<string, NodeJS.Timeout> = new Map();

  set(key: string, value: any, ttl: number = 300000) { // Default TTL: 5 minutes
    // Clear any existing timeout
    if (this.timeouts.has(key)) {
      clearTimeout(this.timeouts.get(key)!);
      this.timeouts.delete(key);
    }

    // Set the value
    this.cache.set(key, value);

    // Set expiration timeout
    const timeout = setTimeout(() => {
      this.cache.delete(key);
      this.timeouts.delete(key);
    }, ttl);

    this.timeouts.set(key, timeout);
  }

  get(key: string) {
    return this.cache.get(key);
  }

  has(key: string) {
    return this.cache.has(key);
  }

  delete(key: string) {
    this.cache.delete(key);
    if (this.timeouts.has(key)) {
      clearTimeout(this.timeouts.get(key)!);
      this.timeouts.delete(key);
    }
  }

  clear() {
    this.cache.clear();
    this.timeouts.forEach(timeout => clearTimeout(timeout));
    this.timeouts.clear();
  }
}

export const cache = new InMemoryCache();

// Cache key generators
export const getTasksCacheKey = (userId: string, filters: any = {}) => {
  const filterStr = Object.entries(filters)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}:${value}`)
    .join('|');
  
  return `tasks:${userId}:${filterStr}`;
};

export const getTaskCacheKey = (taskId: string) => {
  return `task:${taskId}`;
};