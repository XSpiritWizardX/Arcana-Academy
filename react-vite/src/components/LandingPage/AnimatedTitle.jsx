import { useLayoutEffect, useRef } from "react";
import { gsap } from "gsap";
import "./AnimatedTitle.css";

export default function AnimatedTitle() {
  const svgRef = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const q = gsap.utils.selector(svgRef);
      const strokes = q(".arcana-letter");

      strokes.forEach((el) => {
        const len = el.getComputedTextLength ? el.getComputedTextLength() : 800;
        gsap.set(el, {
          strokeDasharray: len,
          strokeDashoffset: len,
          opacity: 1,
        });
      });

      gsap.to(strokes, {
        strokeDashoffset: 0,
        duration: 16,
        ease: "none",
        stagger: 0.18,
      });

      gsap.fromTo(
        q(".arcana-title-fill"),
        { opacity: 0 },
        {
          opacity: 1,
          duration: 3,
          delay: 14,
          ease: "power1.out",
        }
      );
    }, svgRef);

    return () => ctx.revert();
  }, []);

  return (
    <div className="arcana-title-wrap">
      <svg
        ref={svgRef}
        className="arcana-title-svg"
        viewBox="0 0 1200 220"
        role="img"
        aria-label="Arcana Academy"
      >
        <g className="arcana-title-group">
          <text x="50%" y="60%" textAnchor="middle" className="arcana-letter">
            Arcana Academy
          </text>
          <text x="50%" y="60%" textAnchor="middle" className="arcana-title-fill">
            Arcana Academy
          </text>
        </g>
      </svg>
      <p className="arcana-tagline">A world you shape with your imagination</p>
    </div>
  );
}
