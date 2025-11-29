import { useEffect, useRef } from "react";
import "./Snowfall.css";

export default function Snowfall() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const makeFlake = () => {
      const flake = document.createElement("span");
      flake.className = "snowflake";
      const size = 4 + Math.random() * 6;
      flake.style.width = `${size}px`;
      flake.style.height = `${size}px`;
      flake.style.left = `${Math.random() * 100}vw`;
      flake.style.animationDuration = `${5 + Math.random() * 5}s`;
      flake.style.animationDelay = `${Math.random() * 2}s`;
      container.appendChild(flake);
      setTimeout(() => {
        if (flake.parentNode) flake.parentNode.removeChild(flake);
      }, 12000);
    };

    const interval = setInterval(makeFlake, 200);
    return () => clearInterval(interval);
  }, []);

  return <div className="snow-container" ref={containerRef} />;
}
