// Basic configuration for API URL
// Vercel will set VITE_API_URL environment variable
// Local development falls back to localhost:8000

export const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : 'https://cyber-resilience-quiz.onrender.com');

