import { useEffect, useRef } from "react";
import "./CursorRibbon.css";

export default function CursorRibbon() {
  const containerRef = useRef(null);
  const lastPos = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMove = (e) => {
      const offsetY = 10;
      const x = e.clientX;
      const y = e.clientY + offsetY;

      if (lastPos.current) {
        const { x: lx, y: ly } = lastPos.current;
        const dx = x - lx;
        const dy = y - ly;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 0.5) {
          const angle = Math.atan2(dy, dx) * (180 / Math.PI);
          const midX = (x + lx) / 2;
          const midY = (y + ly) / 2;
          const line = document.createElement("span");
          line.className = "ribbon-line";
          const hue = 200 + Math.random() * 40;
          line.style.left = `${midX}px`;
          line.style.top = `${midY}px`;
          line.style.width = `${dist + 12}px`;
          line.style.transform = `translate(-50%, -50%) rotate(${angle}deg)`;
          line.style.setProperty("--ribbon-hue", hue);
          line.style.setProperty("--ribbon-warm", Math.random() < 0.4 ? 1 : 0);
          container.appendChild(line);
          setTimeout(() => {
            if (line.parentNode) line.parentNode.removeChild(line);
          }, 950);
        }
      }

      lastPos.current = { x, y };
    };

    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, []);

  return <div className="ribbon-container" ref={containerRef} />;
}
