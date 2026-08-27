import { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { thunkAuthenticate } from "../redux/session";
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
        {isLoaded && (
          <div className={`arcana-app-shell${adventureMode ? " adventure-mode" : ""}`}>
            <AdventurePortalBar />
            <div className={`content-area${adventureMode ? " adventure-content-area" : " standard-content-area"}`}>
              <Outlet />
            </div>
          </div>
        )}
        <Modal />
      </div>
    </ModalProvider>
  );
}
