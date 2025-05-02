// // import { useEffect, useState } from "react";
// // import { Outlet } from "react-router-dom";
// // import { useDispatch } from "react-redux";
// // import { ModalProvider, Modal } from "../context/Modal";
// // import { thunkAuthenticate } from "../redux/session";
// // import Navigation from "../components/Navigation/Navigation";
// // import FooterCard from "../components/Footer/Footer";
// // import "./Layout.css";
// // import { gsap } from "gsap";
// // export default function Layout() {
// //   const dispatch = useDispatch();
// //   const [isLoaded, setIsLoaded] = useState(false);
// //   useEffect(() => {
// //     dispatch(thunkAuthenticate()).then(() => setIsLoaded(true));
// //   }, [dispatch]);







// //   const maxSnowflakes = 200;
// //   const snowflakes = [];
// //   const maxMouseflakes = 150; // limit active mouse particles
// //   let mouseflakes = [];
// //   let lastX = 0;
// //   let lastY = 0;
// //   let lastTime = Date.now();
// //   let lastTrailTime = 0;

// //   function createSnowflake() {
// //     if (snowflakes.length >= maxSnowflakes) return;

// //     const snowflake = document.createElement("div");
// //     snowflake.classList.add("snowflake");

// //     const size = Math.random() * 5 + 3;
// //     snowflake.style.width = `${size}px`;
// //     snowflake.style.height = `${size}px`;

// //     const startX = Math.random() * window.innerWidth;
// //     document.body.appendChild(snowflake);

// //     snowflakes.push(snowflake);

// //     gsap.set(snowflake, {
// //       x: startX,
// //       y: -10,
// //       opacity: Math.random() * 0.5 + 0.1,
// //       scale: Math.random() * 0.8 + 0.6
// //     });

// //     gsap.to(snowflake, {
// //       duration: 10 + Math.random() * 10,
// //       x: startX + (Math.random() - 0.5) * 200,
// //       y: window.innerHeight + 20,
// //       rotation: Math.random() * 360,
// //       ease: "linear",
// //       onComplete: () => {
// //         snowflake.remove();
// //         snowflakes.splice(snowflakes.indexOf(snowflake), 1);
// //       }
// //     });

// //     // 5% chance to create a magicflake
// //     if (Math.random() < 0.05) {
// //       createMagicFlake(startX);
// //     }
// //   }

// //   function createMagicFlake(startX) {
// //     const magicflake = document.createElement("div");
// //     magicflake.classList.add("magicflake");
// //     document.body.appendChild(magicflake);

// //     const offsetX = (Math.random() - 0.5) * 100;

// //     gsap.set(magicflake, {
// //       x: startX + offsetX,
// //       y: -20,
// //       scale: 1,
// //       opacity: 0.9
// //     });

// //     gsap.to(magicflake, {
// //       duration: 12 + Math.random() * 8,
// //       x: startX + offsetX + (Math.random() - 0.5) * 300,
// //       y: window.innerHeight + 30,
// //       scale: 1.5,
// //       opacity: 0,
// //       ease: "power1.inOut",
// //       onComplete: () => {
// //         magicflake.remove();
// //       }
// //     });
// //   }

// //   setInterval(() => {
// //     for (let i = 0; i < 2; i++) {
// //       createSnowflake();
// //     }
// //   }, 200);

// //   window.addEventListener("mousemove", (e) => {
// //     const now = Date.now();
// //     const deltaTime = now - lastTime;
// //     const deltaX = e.clientX - lastX;
// //     const deltaY = e.clientY - lastY;
// //     const speed = Math.sqrt(deltaX * deltaX + deltaY * deltaY) / deltaTime;

// //     lastX = e.clientX;
// //     lastY = e.clientY;
// //     lastTime = now;

// //     // Throttle trail creation to avoid flooding
// //     if (now - lastTrailTime > 30) {
// //       // create trail every 30ms
// //       const particleCount = Math.min(Math.floor(speed * 30), 6); // limit max

// //       for (let i = 0; i < particleCount; i++) {
// //         createMouseflake(e.clientX, e.clientY);
// //       }
// //       lastTrailTime = now;
// //     }
// //   });

// //   function createMouseflake(x, y) {
// //     if (mouseflakes.length >= maxMouseflakes) return; // hard limit active trails

// //     const mouseflake = document.createElement("div");
// //     mouseflake.classList.add("mouseflake");
// //     document.body.appendChild(mouseflake);

// //     mouseflakes.push(mouseflake);

// //     const size = Math.random() * 3 + 10;
// //     mouseflake.style.width = `${size}px`;
// //     mouseflake.style.height = `${size}px`;

// //     const driftX = (Math.random() - 0.5) * 80;
// //     const driftY = Math.random() * 100;

// //     gsap.set(mouseflake, {
// //       x: x - size / 2,
// //       y: y - size / 2,
// //       opacity: 1,
// //       scale: 1
// //     });

// //     gsap.to(mouseflake, {
// //       duration: 1.2,
// //       x: x + driftX,
// //       y: y + driftY,
// //       opacity: 0,
// //       scale: 0.5,
// //       ease: "power2.out",
// //       onComplete: () => {
// //         mouseflake.remove();
// //         mouseflakes.splice(mouseflakes.indexOf(mouseflake), 1); // clean
// //       }
// //     });
// //   }





// //   return (
// //     <div
// //     className="layout-container"
// //     >
// //         <h1
// //         className="Arcana-layout"
// //         >Arcana Academy</h1>

// //           <ModalProvider>
// //         <div
// //         className="layout"
// //         >
// //         <Navigation />
// //         {isLoaded && <Outlet />}

// //         <Modal />
// //         </div>
// //         <FooterCard />
// //       </ModalProvider>
// //     </div>
// //   );
// // }



// import { useEffect, useState } from "react";
// import { Outlet } from "react-router-dom";
// import { useDispatch } from "react-redux";
// import { ModalProvider, Modal } from "../context/Modal";
// import { thunkAuthenticate } from "../redux/session";
// import Navigation from "../components/Navigation/Navigation";
// import FooterCard from "../components/Footer/Footer";
// import { gsap } from "gsap";
// import "./Layout.css";

// export default function Layout() {
//   const dispatch = useDispatch();
//   const [isLoaded, setIsLoaded] = useState(false);

//   useEffect(() => {
//     dispatch(thunkAuthenticate()).then(() => setIsLoaded(true));
//   }, [dispatch]);

//   useEffect(() => {
//     const maxSnowflakes = 200;
//     const snowflakes = [];
//     const maxMouseflakes = 150; // limit active mouse particles
//     let mouseflakes = [];
//     let lastX = 0;
//     let lastY = 0;
//     let lastTime = Date.now();
//     let lastTrailTime = 0;

//     function createSnowflake() {
//       if (snowflakes.length >= maxSnowflakes) return;

//       const snowflake = document.createElement("div");
//       snowflake.classList.add("snowflake");

//       const size = Math.random() * 5 + 3;
//       snowflake.style.width = `${size}px`;
//       snowflake.style.height = `${size}px`;

//       const startX = Math.random() * window.innerWidth;
//       document.body.appendChild(snowflake);

//       snowflakes.push(snowflake);

//       gsap.set(snowflake, {
//         x: startX,
//         y: -10,
//         opacity: Math.random() * 0.5 + 0.1,
//         scale: Math.random() * 0.8 + 0.6
//       });

//       gsap.to(snowflake, {
//         duration: 10 + Math.random() * 10,
//         x: startX + (Math.random() - 0.5) * 200,
//         y: window.innerHeight + 20,
//         rotation: Math.random() * 360,
//         ease: "linear",
//         onComplete: () => {
//           snowflake.remove();
//           snowflakes.splice(snowflakes.indexOf(snowflake), 1);
//         }
//       });

//       // 5% chance to create a magicflake
//       if (Math.random() < 0.05) {
//         createMagicFlake(startX);
//       }
//     }

//     function createMagicFlake(startX) {
//       const magicflake = document.createElement("div");
//       magicflake.classList.add("magicflake");
//       document.body.appendChild(magicflake);

//       const offsetX = (Math.random() - 0.5) * 100;

//       gsap.set(magicflake, {
//         x: startX + offsetX,
//         y: -20,
//         scale: 1,
//         opacity: 0.9
//       });

//       gsap.to(magicflake, {
//         duration: 12 + Math.random() * 8,
//         x: startX + offsetX + (Math.random() - 0.5) * 300,
//         y: window.innerHeight + 30,
//         scale: 1.5,
//         opacity: 0,
//         ease: "power1.inOut",
//         onComplete: () => {
//           magicflake.remove();
//         }
//       });
//     }

//     const snowflakeInterval = setInterval(() => {
//       for (let i = 0; i < 2; i++) {
//         createSnowflake();
//       }
//     }, 200);

//     function createMouseflake(x, y) {
//       if (mouseflakes.length >= maxMouseflakes) return; // hard limit active trails

//       const mouseflake = document.createElement("div");
//       mouseflake.classList.add("mouseflake");
//       document.body.appendChild(mouseflake);

//       mouseflakes.push(mouseflake);

//       const size = Math.random() * 3 + 10;
//       mouseflake.style.width = `${size}px`;
//       mouseflake.style.height = `${size}px`;

//       const driftX = (Math.random() - 0.5) * 80;
//       const driftY = Math.random() * 100;

//       gsap.set(mouseflake, {
//         x: x - size / 2,
//         y: y - size / 2,
//         opacity: 1,
//         scale: 1
//       });

//       gsap.to(mouseflake, {
//         duration: 1.2,
//         x: x + driftX,
//         y: y + driftY,
//         opacity: 0,
//         scale: 0.5,
//         ease: "power2.out",
//         onComplete: () => {
//           mouseflake.remove();
//           mouseflakes.splice(mouseflakes.indexOf(mouseflake), 1); // clean
//         }
//       });
//     }

//     const handleMouseMove = (e) => {
//       const now = Date.now();
//       const deltaTime = now - lastTime;
//       const deltaX = e.clientX - lastX;
//       const deltaY = e.clientY - lastY;
//       const speed = Math.sqrt(deltaX * deltaX + deltaY * deltaY) / deltaTime;

//       lastX = e.clientX;
//       lastY = e.clientY;
//       lastTime = now;

//       // Throttle trail creation to avoid flooding
//       if (now - lastTrailTime > 30) {
//         // create trail every 30ms
//         const particleCount = Math.min(Math.floor(speed * 30), 6); // limit max

//         for (let i = 0; i < particleCount; i++) {
//           createMouseflake(e.clientX, e.clientY);
//         }
//         lastTrailTime = now;
//       }
//     };

//     window.addEventListener("mousemove", handleMouseMove);

//     // Cleanup function to prevent memory leaks
//     return () => {
//       clearInterval(snowflakeInterval);
//       window.removeEventListener("mousemove", handleMouseMove);
//       // Remove any remaining snowflakes
//       snowflakes.forEach(snowflake => snowflake.remove());
//       mouseflakes.forEach(mouseflake => mouseflake.remove());
//     };
//   }, []);

//   return (
//     <>
//       <h1 className="Arcana-layout">Arcana Academy</h1>
//       <ModalProvider>
//         <div className="layout">
//           <Navigation />
//           {isLoaded && <Outlet />}
//           <Modal />
//         </div>
//         <FooterCard />
//       </ModalProvider>
//     </>
//   );
// }





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
    const maxSnowflakes = 200;
    const snowflakes = [];
    const maxMouseflakes = 150;
    let mouseflakes = [];
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
        y: docHeight + 20, // Use document height instead of window height
        rotation: Math.random() * 360,
        ease: "linear",
        onComplete: () => {
          if (snowflake.parentNode) {
            snowflake.parentNode.removeChild(snowflake);
          }
          snowflakes.splice(snowflakes.indexOf(snowflake), 1);
        }
      });

      // 5% chance to create a magicflake
      if (Math.random() < 0.05) {
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
        y: docHeight + 30, // Use document height
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

      const driftX = (Math.random() - 0.5) * 80;
      const driftY = Math.random() * 100;

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

    const snowflakeInterval = setInterval(() => {
      for (let i = 0; i < 2; i++) {
        createSnowflake();
      }
    }, 200);

    const handleMouseMove = (e) => {
      const now = Date.now();
      const deltaTime = now - lastTime;
      const deltaX = e.clientX - lastX;
      const deltaY = e.clientY - lastY;
      const speed = Math.sqrt(deltaX * deltaX + deltaY * deltaY) / deltaTime;

      lastX = e.clientX;
      lastY = e.clientY;
      lastTime = now;

      if (now - lastTrailTime > 30) {
        const particleCount = Math.min(Math.floor(speed * 30), 6);

        for (let i = 0; i < particleCount; i++) {
          createMouseflake(e.clientX, e.clientY);
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
        const currentY = gsap.getProperty(snowflake, "y");
        const progress = currentY / (window.innerHeight + 20);

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

    // Cleanup function
    return () => {
      clearInterval(snowflakeInterval);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("scroll", handleResize);

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
    <>
      <h1 className="Arcana-layout">Arcana Academy</h1>

      {/* Snow container that covers the entire page */}
      <div ref={snowContainerRef} className="snow-container">


      </div>
      <ModalProvider>
        <div className="layout">
          <Navigation />
          {isLoaded && <Outlet />}
          <Modal />
        </div>
        <FooterCard />
      </ModalProvider>

    </>
  );
}
