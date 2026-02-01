/**
 * Utility functions for date formatting
 */

/**
 * Format a Date object to YYYY-MM-DD for HTML date inputs
 */
export function formatDateForInput(date: Date): string {
  return date.toISOString().split('T')[0];
}

/**
 * Format a Date object to ISO string
 */
export function formatDateTimeISO(date: Date): string {
  return date.toISOString();
}

/**
 * Parse ISO date string to Date object
 */
export function parseISODate(dateString: string): Date {
  return new Date(dateString);
}

/**
 * Get date range for today
 */
export function getTodayRange(): { start: Date; end: Date } {
  const start = new Date();
  start.setHours(0, 0, 0, 0);
  
  const end = new Date();
  end.setHours(23, 59, 59, 999);
  
  return { start, end };
}
