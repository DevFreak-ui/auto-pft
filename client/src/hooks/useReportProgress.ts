import { useEffect, useState } from "react";

export function useReportProgress() {
  const [stage, setStage] = useState<1 | 2 | 3>(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setStage((prev) => (prev === 3 ? 1 : (prev + 1) as 1 | 2 | 3));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return stage;
} 