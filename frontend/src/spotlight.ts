import { useSearchParams } from "react-router-dom";

export interface Spotlight {
  spotlightId: string | null;
  setSpotlight: (id: string | null) => void;
}

export function useSpotlight(): Spotlight {
  const [params, setParams] = useSearchParams();
  const spotlightId = params.get("spotlight") || null;

  const setSpotlight = (id: string | null) => {
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        if (id) next.set("spotlight", id);
        else next.delete("spotlight");
        return next;
      },
      { replace: true },
    );
  };

  return { spotlightId, setSpotlight };
}
