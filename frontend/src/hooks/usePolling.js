import { useEffect, useRef } from 'react';

export function usePolling(fn, active, interval = 2000, maxTries = 20) {
  const tries = useRef(0);

  useEffect(() => {
    if (!active) {
      tries.current = 0;
      return;
    }
    const timer = setInterval(async () => {
      tries.current += 1;
      const shouldStop = await fn();
      if (shouldStop || tries.current >= maxTries) {
        clearInterval(timer);
      }
    }, interval);

    return () => clearInterval(timer);
  }, [fn, active, interval, maxTries]);
}