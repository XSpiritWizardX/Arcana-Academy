
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
    const maxSnowflakes = 130;
    const snowflakes = [];
    const maxGreenSnowflakes = 130;
    const greenSnowflakes = [];
    const maxRedSnowflakes = 130;
    const redSnowflakes = [];


    const maxMouseflakes = 150;
    const mouseflakes = [];
    const maxGreenMouseflakes = 150;
    const greenMouseflakes = [];
    const maxRedMouseflakes = 150;
    const redMouseflakes = [];
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
    }






    function createGreenSnowflake() {
      if (greenSnowflakes.length >= maxGreenSnowflakes) return;

      const greenSnowflake = document.createElement("div");
      greenSnowflake.classList.add("snowflake", "green-snowflake");

      const size = Math.random() * 5 + 3;
      greenSnowflake.style.width = `${size}px`;
      greenSnowflake.style.height = `${size}px`;

      const startX = Math.random() * window.innerWidth;
      container.appendChild(greenSnowflake);

      greenSnowflakes.push(greenSnowflake);

      gsap.set(greenSnowflake, {
        x: startX,
        y: -10,
        opacity: Math.random() * 0.5 + 0.1,
        scale: Math.random() * 0.8 + 0.6
      });

      // Use the full document height for animation
      const docHeight = getDocHeight();

      gsap.to(greenSnowflake, {
        duration: 10 + Math.random() * 10,
        x: startX + (Math.random() - 0.5) * 200,
        y: docHeight + 20,
        rotation: Math.random() * 360,
        ease: "linear",
        onComplete: () => {
          if (greenSnowflake.parentNode) {
            greenSnowflake.parentNode.removeChild(greenSnowflake);
          }
          greenSnowflakes.splice(greenSnowflakes.indexOf(greenSnowflake), 1);
        }
      });
    }



    function createRedSnowflake() {
      if (redSnowflakes.length >= maxRedSnowflakes) return;

      const redSnowflake = document.createElement("div");
      redSnowflake.classList.add("snowflake", "red-snowflake");

      const size = Math.random() * 5 + 3;
      redSnowflake.style.width = `${size}px`;
      redSnowflake.style.height = `${size}px`;

      const startX = Math.random() * window.innerWidth;
      container.appendChild(redSnowflake);

      redSnowflakes.push(redSnowflake);

      gsap.set(redSnowflake, {
        x: startX,
        y: -10,
        opacity: Math.random() * 0.5 + 0.1,
        scale: Math.random() * 0.8 + 0.6
      });

      // Use the full document height for animation
      const docHeight = getDocHeight();

      gsap.to(redSnowflake, {
        duration: 10 + Math.random() * 10,
        x: startX + (Math.random() - 0.5) * 200,
        y: docHeight + 20,
        rotation: Math.random() * 360,
        ease: "linear",
        onComplete: () => {
          if (redSnowflake.parentNode) {
            redSnowflake.parentNode.removeChild(redSnowflake);
          }
          redSnowflakes.splice(redSnowflakes.indexOf(redSnowflake), 1);
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
        duration: 1,
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






    function createGreenMouseflake(x, y) {
      if (greenMouseflakes.length >= maxGreenMouseflakes) return;

      const greenMouseflake = document.createElement("div");
      greenMouseflake.classList.add("mouseflake", "green-mouseflake");
      container.appendChild(greenMouseflake);

      greenMouseflakes.push(greenMouseflake);

      const size = Math.random() * 3 + 10;
      greenMouseflake.style.width = `${size}px`;
      greenMouseflake.style.height = `${size}px`;

      // Reduced drift to make particles appear more directly at cursor position
      const driftX = (Math.random() - 0.5) * 40;
      const driftY = (Math.random() - 0.5) * 40;

      // Position exactly at cursor position
      gsap.set(greenMouseflake, {
        x: x - size / 2,
        y: y - size / 2,
        opacity: 1,
        scale: 1
      });

      gsap.to(greenMouseflake, {
        duration: 1,
        x: x + driftX,
        y: y + driftY,
        opacity: 0,
        scale: 0.5,
        ease: "power2.out",
        onComplete: () => {
          if (greenMouseflake.parentNode) {
            greenMouseflake.parentNode.removeChild(greenMouseflake);
          }
          greenMouseflakes.splice(greenMouseflakes.indexOf(greenMouseflake), 1);
        }
      });
    }





    function createRedMouseflake(x, y) {
      if (redMouseflakes.length >= maxRedMouseflakes) return;

      const redMouseflake = document.createElement("div");
      redMouseflake.classList.add("mouseflake", "red-mouseflake");
      container.appendChild(redMouseflake);

      redMouseflakes.push(redMouseflake);

      const size = Math.random() * 3 + 10;
      redMouseflake.style.width = `${size}px`;
      redMouseflake.style.height = `${size}px`;

      // Reduced drift to make particles appear more directly at cursor position
      const driftX = (Math.random() - 0.5) * 40;
      const driftY = (Math.random() - 0.5) * 40;

      // Position exactly at cursor position
      gsap.set(redMouseflake, {
        x: x - size / 2,
        y: y - size / 2,
        opacity: 1,
        scale: 1
      });

      gsap.to(redMouseflake, {
        duration: 1,
        x: x + driftX,
        y: y + driftY,
        opacity: 0,
        scale: 0.5,
        ease: "power2.out",
        onComplete: () => {
          if (redMouseflake.parentNode) {
            redMouseflake.parentNode.removeChild(redMouseflake);
          }
          redMouseflakes.splice(redMouseflakes.indexOf(redMouseflake), 1);
        }
      });
    }









    const snowflakeInterval = setInterval(() => {
      for (let i = 0; i < 2; i++) {
        createSnowflake();
         createGreenSnowflake();
          createRedSnowflake();
        // Occasionally create green snowflakes
        if (Math.random() < 0.3) {
          createGreenSnowflake();
          createRedSnowflake();
        }
      }
    }, 100);

    // Magic flake interval for occasional special effects
    const magicFlakeInterval = setInterval(() => {
      // Create a burst of green snowflakes at random positions
      if (Math.random() < 0.1) {
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * getDocHeight() * 0.7;
        for (let i = 0; i < 10; i++) {
          setTimeout(() => {
            createGreenMouseflake(x, y);
            createRedMouseflake(x, y);
          }, i * 50);
        }
      }
    }, 5000);





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
        const particleCount = Math.min(Math.floor(speed * 10), 8);

        for (let i = 0; i < particleCount; i++) {
          createMouseflake(e.clientX, e.clientY);
          // Occasionally create green mouse flakes
          if (Math.random() < 0.2) {
            createGreenMouseflake(e.clientX, e.clientY);
          }
          if (Math.random() < 0.2) {
            createRedMouseflake(e.clientX, e.clientY);
          }
        }
        lastTrailTime = now;
      }
    };




    const handleClick = (e) => {
      // Create a burst of particles on click
      for (let i = 0; i < 20; i++) {
        setTimeout(() => {
          createMouseflake(e.clientX, e.clientY);
          createGreenMouseflake(e.clientX, e.clientY);
          createRedMouseflake(e.clientX, e.clientY);

        }, i * 20);
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




      // Update existing green snowflakes to the new document height
      greenSnowflakes.forEach(greenSnowflake => {
        gsap.killTweensOf(greenSnowflake);
        gsap.to(greenSnowflake, {
          duration: 10 + Math.random() * 10,
          y: docHeight + 20,
          ease: "linear",
          onComplete: () => {
            if (greenSnowflake.parentNode) {
              greenSnowflake.parentNode.removeChild(greenSnowflake);
            }
            greenSnowflakes.splice(greenSnowflakes.indexOf(greenSnowflake), 1);
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

      // Remove any remaining green snowflakes
      greenSnowflakes.forEach(greenSnowflake => {
        if (greenSnowflake.parentNode) {
          greenSnowflake.parentNode.removeChild(greenSnowflake);
        }
      });

      redSnowflakes.forEach(redSnowflake => {
        if (redSnowflake.parentNode) {
          redSnowflake.parentNode.removeChild(redSnowflake);
        }
      });




      mouseflakes.forEach(mouseflake => {
        if (mouseflake.parentNode) {
          mouseflake.parentNode.removeChild(mouseflake);
        }
      });

      greenMouseflakes.forEach(greenMouseflake => {
        if (greenMouseflake.parentNode) {
          greenMouseflake.parentNode.removeChild(greenMouseflake);
        }
      });

      redMouseflakes.forEach(redMouseflake => {
        if (redMouseflake.parentNode) {
          redMouseflake.parentNode.removeChild(redMouseflake);
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
