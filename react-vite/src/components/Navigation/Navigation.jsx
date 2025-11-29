import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import LogoutButton from "./LogoutButton";
import { useEffect, useState } from "react";
import { csrfFetch } from "../../redux/csrf";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import "./Navigation.css";

function Navigation() {
  const user = useSelector((state) => state.session.user);
  const [advState, setAdvState] = useState(null);

  const baseLinks = [
    { to: "/", label: "Town" },
    { to: "/adventure", label: "Adventure" },
    { to: "/battle", label: "Battle" },
  ];
  const contentLinks = [
    { to: "/spells/all", label: "Spells" },
    { to: "/swords/all", label: "Swords" },
    { to: "/potions/all", label: "Potions" },
    { to: "/coming-soon", label: "Bestiary" },
  ];
  const userLinks = user
    ? [
        { to: "/players", label: "Your Players" },
        { to: "/spells", label: "Your Spells" },
        { to: "/potions", label: "Your Potions" },
        { to: "/swords", label: "Your Swords" },
      ]
    : [];

  useEffect(() => {
    const loadAdventure = async () => {
      try {
        const res = await csrfFetch("/api/adventure/state");
        const data = await res.json();
        setAdvState(data.state);
      } catch (err) {
        setAdvState(null);
      }
    };
    if (user) {
      loadAdventure();
    } else {
      setAdvState(null);
    }
  }, [user]);

  return (
    <aside className="nav-shell">
      <div className="nav-title">Arcana Academy</div>
      <div className="nav-subtitle">A legend you write yourself</div>

      <div className="nav-usercard">
        <div className="user-box">

        <div className="avatar-circle">{user ? user.username?.[0]?.toUpperCase() : "?"}</div>
        <div className="user-lines">
          <div className="user-line">{user ? user.username : "Guest"}</div>
          <div className="user-line muted">{user ? user.email : "Sign in to play"}</div>
        </div>
        </div>

            { advState && (
              <div className="user-stats-block">
                <div>Level: <span className="stat-value">{advState.level}</span></div>
                <div>HP: <span className="stat-value">{advState.hp}/{advState.max_hp}</span></div>
                <div>Attack: <span className="stat-value">{advState.attack}</span></div>
                <div>Defense: <span className="stat-value">{advState.defense}</span></div>
                <div>Gold: <span className="stat-value">{advState.gold}</span></div>
                <div>Bank: <span className="stat-value">{advState.bank_gold}</span></div>
                <div>XP: <span className="stat-value">{advState.xp}</span></div>
                <div>Turns: <span className="stat-value">{advState.turns}</span></div>
                <div>Location: <span className="stat-value">{advState.location}</span></div>
                <div>Weapon: <span className="stat-value">todo</span></div>
                <div>Armor: <span className="stat-value">todo</span></div>
              </div>
            )}

      </div>



      <div

      className="nav-links-container">

      <nav className="nav-links">
        <div className="nav-section">community</div>
        {[...baseLinks, ...contentLinks].map((link) => (
          <NavLink key={link.to} to={link.to} className="nav-link">
            {link.label}
          </NavLink>
        ))}


      </nav>

      <nav className="nav-links">

        {userLinks.length > 0 && (
          <>
            <div className="nav-section">Your Stuff</div>
            {userLinks.map((link) => (
              <NavLink key={link.to} to={link.to} className="nav-link">
                {link.label}
              </NavLink>
            ))}


            <LogoutButton />
          </>
        )}
        {!user && (
          <div className="nav-auth">
            <OpenModalButton
              className="nav-modal-btn"
              buttonText="Log In"
              modalComponent={<LoginFormModal />}
            />
            <OpenModalButton
              className="nav-modal-btn"
              buttonText="Sign Up"
              modalComponent={<SignupFormModal />}
            />
          </div>
        )}
      </nav>
        </div>




    </aside>
  );
}

export default Navigation;
