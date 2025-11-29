import { useEffect, useRef } from "react";
import "./CursorRibbon.css";

export default function CursorRibbon() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMove = (e) => {
      const createDot = (offsetX, offsetY, hueShift = 0) => {
        const dot = document.createElement("span");
        dot.className = "ribbon-dot";
        const size = 6 + Math.random() * 10;
        const hue = 200 + Math.random() * 120 + hueShift;
        dot.style.left = `${e.clientX + offsetX}px`;
        dot.style.top = `${e.clientY + offsetY}px`;
        dot.style.width = `${size}px`;
        dot.style.height = `${size}px`;
        dot.style.setProperty("--ribbon-hue", hue);
        container.appendChild(dot);
        setTimeout(() => {
          if (dot.parentNode) dot.parentNode.removeChild(dot);
        }, 1200);
      };

      const createStreak = () => {
        const streak = document.createElement("span");
        streak.className = "ribbon-streak";
        const length = 30 + Math.random() * 40;
        const hue = 200 + Math.random() * 120;
        const angle = -20 + Math.random() * 40;
        streak.style.left = `${e.clientX}px`;
        streak.style.top = `${e.clientY}px`;
        streak.style.width = `${length}px`;
        streak.style.transform = `translate(-50%, -50%) rotate(${angle}deg)`;
        streak.style.setProperty("--ribbon-hue", hue);
        container.appendChild(streak);
        setTimeout(() => {
          if (streak.parentNode) streak.parentNode.removeChild(streak);
        }, 900);
      };

      createDot(0, 0, 0);
      createDot((Math.random() - 0.5) * 12, (Math.random() - 0.5) * 12, 40);
      createDot((Math.random() - 0.5) * 18, (Math.random() - 0.5) * 18, -40);
      createStreak();
    };

    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, []);

  return <div className="ribbon-container" ref={containerRef} />;
}
