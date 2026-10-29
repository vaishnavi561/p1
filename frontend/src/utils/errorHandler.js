

export function parseApiError(err, defaultMessage = "An unexpected error occurred.") {
  if (!err.response) {
    return err.message || defaultMessage;
  }

  const data = err.response.data;

  if (typeof data === 'string') {
    return data;
  }

  if (typeof data === 'object' && data !== null) {
    // If DRF returned field-specific errors, grab the first message of the first field
    const keys = Object.keys(data);
    if (keys.length > 0) {
      const firstFieldErrors = data[keys[0]];
      if (Array.isArray(firstFieldErrors) && firstFieldErrors.length > 0) {
        return `${keys[0]}: ${firstFieldErrors[0]}`;
      }
      if (typeof firstFieldErrors === 'string') {
        return `${keys[0]}: ${firstFieldErrors}`;
      }
    }
    // Fallback JSON stringify if format is unfamiliar
    return JSON.stringify(data);
  }

  return defaultMessage;
}