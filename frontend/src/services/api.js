const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';

export async function request(path, options = {}) {
  const userId = localStorage.getItem('x_user_id') || 'demo-user';
  
  // 10-second timeout controller so it NEVER gets stuck loading infinitely
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': userId,
        ...(options.headers || {})
      }
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errBody = await response.json().catch(() => ({ error: 'Network failure' }));
      throw new Error(errBody.error || `Error ${response.status}`);
    }

    return await response.json();
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error('Server took too long to respond (10s timeout). Please verify the backend is running.');
    }
    throw err;
  }
}