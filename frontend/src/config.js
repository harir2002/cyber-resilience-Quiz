// Basic configuration for API URL
// Vercel will set VITE_API_URL environment variable
// Local development falls back to localhost:8000

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
