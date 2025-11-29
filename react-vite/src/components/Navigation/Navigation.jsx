import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import LogoutButton from "./LogoutButton";
import "./Navigation.css";

function Navigation() {
  const user = useSelector((state) => state.session.user);
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

  return (
    <aside className="nav-shell">
      <div className="nav-title">Arcana Academy</div>
      <div className="nav-subtitle">A legend you write yourself</div>
      <nav className="nav-links">
        {[...baseLinks, ...contentLinks].map((link) => (
          <NavLink key={link.to} to={link.to} className="nav-link">
            {link.label}
          </NavLink>
        ))}
        {userLinks.length > 0 && (
          <>
            <div className="nav-section">Your Stuff</div>
            {userLinks.map((link) => (
              <NavLink key={link.to} to={link.to} className="nav-link">
                {link.label}
              </NavLink>
            ))}
            <div className="nav-section user-info">
              <div>{user.username}</div>
              <div className="muted">{user.email}</div>
            </div>
            <LogoutButton />
          </>
        )}
        {!user && (
          <div className="nav-auth">
            <NavLink to="/login" className="nav-link">
              Log In
            </NavLink>
            <NavLink to="/signup" className="nav-link">
              Sign Up
            </NavLink>
          </div>
        )}
      </nav>
    </aside>
  );
}

export default Navigation;
