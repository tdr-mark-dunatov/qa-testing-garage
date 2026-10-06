/**
 * 🏁 Shared Constants for Webhook Pitstop Monorepo
 * Used across all apps (API, Web, CLI, etc.)
 */

export const HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'];

export const METHOD_COLORS = {
  GET: { text: 'text-blue-600', bg: 'bg-blue-50' },
  POST: { text: 'text-green-600', bg: 'bg-green-50' },
  PUT: { text: 'text-yellow-600', bg: 'bg-yellow-50' },
  DELETE: { text: 'text-red-600', bg: 'bg-red-50' },
  PATCH: { text: 'text-purple-600', bg: 'bg-purple-50' },
  OPTIONS: { text: 'text-gray-600', bg: 'bg-gray-50' },
};

export const DEFAULT_REQUEST_LIMIT = 50;
export const WEBSOCKET_PING_INTERVAL = 30000; // 30 seconds

export const RACING_EMOJIS = {
  FLAG: '🏁',
  LIGHTNING: '⚡',
  WRENCH: '🔧',
  FIRE: '🔥',
  STOPWATCH: '⏱️',
  TROPHY: '🏆',
};
