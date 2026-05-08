import { useLayoutEffect, useRef, useState } from "react";

export const REM_PX = 16;

export function ShowAllButton({ onExpand }: { onExpand: () => void }) {
  return (
    <button
      type="button"
      className="clipped-block-expand"
      onClick={(e) => {
        e.stopPropagation();
        onExpand();
      }}
    >
      Show all ↓
    </button>
  );
}

export function ClippedBlock({
  maxHeightRem,
  contentClassName,
  contentKey,
  children,
}: {
  maxHeightRem: number;
  contentClassName?: string;
  /** Stable string used as the measurement effect's dependency, so we don't
   * remeasure on every parent re-render that constructs new `children`. */
  contentKey?: string;
  children: React.ReactNode;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [expanded, setExpanded] = useState(false);
  const [clipped, setClipped] = useState(false);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    setClipped(el.scrollHeight > maxHeightRem * REM_PX + 1);
  }, [contentKey, maxHeightRem]);

  const innerClass = ["clipped-block-content", contentClassName].filter(Boolean).join(" ");
  return (
    <div className="clipped-block">
      <div
        ref={ref}
        className={innerClass}
        style={expanded ? undefined : { maxHeight: `${maxHeightRem}rem`, overflow: "hidden" }}
      >
        {children}
      </div>
      {clipped && !expanded && <ShowAllButton onExpand={() => setExpanded(true)} />}
    </div>
  );
}
