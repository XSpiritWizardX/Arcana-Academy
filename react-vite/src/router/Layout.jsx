import { useEffect, useState, useRef } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";
import FooterCard from "../components/Footer/Footer";
import { gsap } from "gsap";
import "./Layout.css";

export default function Layout() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  const snowContainerRef = useRef(null);

  useEffect(() => {
    dispatch(thunkAuthenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  useEffect(() => {
    if (!snowContainerRef.current) return;

    const container = snowContainerRef.current;
    const maxSnowflakes = 400;
    const snowflakes = [];
    const maxMouseflakes = 350;
    const mouseflakes = [];
    let lastX = 0;
    let lastY = 0;
    let lastTime = Date.now();
    let lastTrailTime = 0;

    // Function to get the full document height
    const getDocHeight = () => {
      return Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight,
        document.body.offsetHeight,
        document.documentElement.offsetHeight,
        document.body.clientHeight,
        document.documentElement.clientHeight,
        window.innerHeight
      );
    };

    function createSnowflake() {
      if (snowflakes.length >= maxSnowflakes) return;

      const snowflake = document.createElement("div");
      snowflake.classList.add("snowflake");

      const size = Math.random() * 5 + 3;
      snowflake.style.width = `${size}px`;
      snowflake.style.height = `${size}px`;

      const startX = Math.random() * window.innerWidth;
      container.appendChild(snowflake);

      snowflakes.push(snowflake);

      gsap.set(snowflake, {
        x: startX,
        y: -10,
        opacity: Math.random() * 0.5 + 0.1,
        scale: Math.random() * 0.8 + 0.6
      });

      // Use the full document height for animation
      const docHeight = getDocHeight();

      gsap.to(snowflake, {
        duration: 10 + Math.random() * 10,
        x: startX + (Math.random() - 0.5) * 200,
        y: docHeight + 20,
        rotation: Math.random() * 360,
        ease: "linear",
        onComplete: () => {
          if (snowflake.parentNode) {
            snowflake.parentNode.removeChild(snowflake);
          }
          snowflakes.splice(snowflakes.indexOf(snowflake), 1);
        }
      });

      // 15% chance to create a magicflake (increased from 5%)
      if (Math.random() < 0.15) {
        createMagicFlake(startX);
      }
    }

    function createMagicFlake(startX) {
      const magicflake = document.createElement("div");
      magicflake.classList.add("magicflake");
      container.appendChild(magicflake);

      const offsetX = (Math.random() - 0.5) * 100;
      const docHeight = getDocHeight();

      gsap.set(magicflake, {
        x: startX + offsetX,
        y: -20,
        scale: 1,
        opacity: 0.9
      });

      gsap.to(magicflake, {
        duration: 12 + Math.random() * 8,
        x: startX + offsetX + (Math.random() - 0.5) * 300,
        y: docHeight + 30,
        scale: 1.5,
        opacity: 0,
        ease: "power1.inOut",
        onComplete: () => {
          if (magicflake.parentNode) {
            magicflake.parentNode.removeChild(magicflake);
          }
        }
      });
    }

    function createMouseflake(x, y) {
      if (mouseflakes.length >= maxMouseflakes) return;

      const mouseflake = document.createElement("div");
      mouseflake.classList.add("mouseflake");
      container.appendChild(mouseflake);

      mouseflakes.push(mouseflake);

      const size = Math.random() * 3 + 10;
      mouseflake.style.width = `${size}px`;
      mouseflake.style.height = `${size}px`;

      // Reduced drift to make particles appear more directly at cursor position
      const driftX = (Math.random() - 0.5) * 40;
      const driftY = (Math.random() - 0.5) * 40;

      // Position exactly at cursor position
      gsap.set(mouseflake, {
        x: x - size / 2,
        y: y - size / 2,
        opacity: 1,
        scale: 1
      });

      gsap.to(mouseflake, {
        duration: 1.2,
        x: x + driftX,
        y: y + driftY,
        opacity: 0,
        scale: 0.5,
        ease: "power2.out",
        onComplete: () => {
          if (mouseflake.parentNode) {
            mouseflake.parentNode.removeChild(mouseflake);
          }
          mouseflakes.splice(mouseflakes.indexOf(mouseflake), 1);
        }
      });
    }

    // Create a magical moment with a burst of magic flakes
    function createMagicalMoment() {
      const centerX = Math.random() * window.innerWidth;
      const burstCount = Math.floor(Math.random() * 10) + 15;

      for (let i = 0; i < burstCount; i++) {
        setTimeout(() => {
          createMagicFlake(centerX + (Math.random() - 0.5) * 100);
        }, i * 100); // Stagger the creation for a more magical effect
      }
    }

    // Handle click events to create magic flake bursts
    const handleClick = (e) => {
      // Create a burst of 5-10 magic flakes at the click position
      const burstCount = Math.floor(Math.random() * 6) + 5;
      for (let i = 0; i < burstCount; i++) {
        createMagicFlake(e.clientX);
      }
    };

    const snowflakeInterval = setInterval(() => {
      for (let i = 0; i < 2; i++) {
        createSnowflake();
      }
    }, 200);

    // Create magic flakes at regular intervals
    const magicFlakeInterval = setInterval(() => {
      // Create 1-2 magic flakes at random positions
      const count = Math.floor(Math.random() * 2) + 1;
      for (let i = 0; i < count; i++) {
        const randomX = Math.random() * window.innerWidth;
        createMagicFlake(randomX);
      }
    }, 1000); // Every second

    // Create a magical moment every 15-30 seconds
    const magicalMomentInterval = setInterval(() => {
      createMagicalMoment();
    }, Math.random() * 15000 + 15000);

    const handleMouseMove = (e) => {
      const now = Date.now();
      const deltaTime = now - lastTime;
      const deltaX = e.clientX - lastX;
      const deltaY = e.clientY - lastY;
      const speed = Math.sqrt(deltaX * deltaX + deltaY * deltaY) / deltaTime;

      lastX = e.clientX;
      lastY = e.clientY;
      lastTime = now;

      // Create particles more frequently for smoother trail
      if (now - lastTrailTime > 20) {
        const particleCount = Math.min(Math.floor(speed * 30), 8);

        for (let i = 0; i < particleCount; i++) {
          createMouseflake(e.clientX, e.clientY);

          // 10% chance to create a magic flake with the cursor
          if (Math.random() < 0.1) {
            createMagicFlake(e.clientX);
          }
        }
        lastTrailTime = now;
      }
    };

    // Update snowflake animations when window is resized
    const handleResize = () => {
      // Recalculate document height and update animations
      const docHeight = getDocHeight();

      // Update existing snowflakes to the new document height
      snowflakes.forEach(snowflake => {
        // Simply kill the current tween and start a new one
        gsap.killTweensOf(snowflake);
        gsap.to(snowflake, {
          duration: 10 + Math.random() * 10,
          y: docHeight + 20,
          ease: "linear",
          onComplete: () => {
            if (snowflake.parentNode) {
              snowflake.parentNode.removeChild(snowflake);
            }
            snowflakes.splice(snowflakes.indexOf(snowflake), 1);
          }
        });
      });
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("resize", handleResize);
    window.addEventListener("scroll", handleResize);
    window.addEventListener("click", handleClick);

    // Cleanup function
    return () => {
      clearInterval(snowflakeInterval);
      clearInterval(magicFlakeInterval);
      clearInterval(magicalMomentInterval);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("scroll", handleResize);
      window.removeEventListener("click", handleClick);

      // Remove any remaining snowflakes
      snowflakes.forEach(snowflake => {
        if (snowflake.parentNode) {
          snowflake.parentNode.removeChild(snowflake);
        }
      });

      mouseflakes.forEach(mouseflake => {
        if (mouseflake.parentNode) {
          mouseflake.parentNode.removeChild(mouseflake);
        }
      });
    };
  }, []);

  return (
    <div className="page-wrapper">
      <h1 className="arcana-title">Arcana Academy</h1>

      {/* Snow container that covers the entire page */}
      <div ref={snowContainerRef} className="snow-container"></div>

      <ModalProvider>
        <div className="layout">
          <Navigation />
          <main className="content-area">
            {isLoaded && <Outlet />}
          </main>
          <Modal />
        </div>
        <FooterCard />
      </ModalProvider>
    </div>
  );
}
