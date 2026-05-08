import { useLayoutEffect, useRef, useState } from "react";
import { REM_PX, ShowAllButton } from "./ClippedBlock";

export function AutoGrowTextarea({
  className,
  value,
  onChange,
  onKeyDown,
  placeholder,
  minRows,
  maxHeightRem,
}: {
  className?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  minRows: number;
  maxHeightRem: number;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const [expanded, setExpanded] = useState(false);
  const [clipped, setClipped] = useState(false);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    // Reset height so shrinking works, then set to natural content height.
    el.style.height = "auto";
    const maxPx = maxHeightRem * REM_PX;
    const natural = el.scrollHeight;
    if (!expanded && natural > maxPx) {
      el.style.height = `${maxPx}px`;
      setClipped(true);
    } else {
      el.style.height = `${natural}px`;
      setClipped(false);
    }
  }, [value, expanded, maxHeightRem]);

  return (
    <div className="autogrow-wrap">
      <textarea
        ref={ref}
        className={`${className ?? ""} autogrow-textarea`.trim()}
        rows={minRows}
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
      />
      {clipped && !expanded && <ShowAllButton onExpand={() => setExpanded(true)} />}
    </div>
  );
}
