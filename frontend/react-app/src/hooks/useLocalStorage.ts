import { useState, useEffect } from "react";

/*
 * Like useState, but persists the value to localStorage under `key`.
 * Reads any existing value on first load, and writes back whenever it changes —
 * used to keep the auth token and user across page refreshes.
 */

function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

export default useLocalStorage;
