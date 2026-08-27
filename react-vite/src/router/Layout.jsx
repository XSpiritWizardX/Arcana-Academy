import { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";
import AdventurePortalBar from "../components/Adventure/AdventurePortalBar";
import CursorRibbon from "../components/CursorRibbon/CursorRibbon";
import Snowfall from "../components/Snowfall/Snowfall";
import "./Layout.css";

export default function Layout() {
  const dispatch = useDispatch();
  const location = useLocation();
  const [isLoaded, setIsLoaded] = useState(false);
  const adventureMode = location.pathname === "/adventure";

  useEffect(() => {
    dispatch(thunkAuthenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <ModalProvider>
      <div className="layout">
        <Snowfall />
        <CursorRibbon />
        {!adventureMode && <Navigation />}
        <div className={`layout-container${adventureMode ? " adventure-layout-container" : ""}`}>
          <div className={`content-area${adventureMode ? " adventure-content-area" : ""}`}>
            {adventureMode && isLoaded && <AdventurePortalBar />}
            {isLoaded && <Outlet />}
          </div>
        </div>
        <Modal />
      </div>
    </ModalProvider>
  );
}
