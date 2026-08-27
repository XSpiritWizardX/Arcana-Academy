import { NavLink, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";
import "./AdventurePortalBar.css";

const WORLD_LINKS = [
  { to: "/", label: "Town" },
  { to: "/adventure", label: "Adventure" },
  { to: "/spells/all", label: "Spells" },
  { to: "/swords/all", label: "Swords" },
  { to: "/potions/all", label: "Potions" },
  { to: "/coming-soon", label: "Bestiary" },
];

const USER_LINKS = [
  { to: "/players", label: "Players" },
  { to: "/spells", label: "My Spells" },
  { to: "/potions", label: "My Potions" },
  { to: "/swords", label: "My Swords" },
];

export default function AdventurePortalBar() {
  const user = useSelector((store) => store.session.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const initial = user?.username?.[0]?.toUpperCase() || "?";

  const logout = async () => {
    await dispatch(thunkLogout());
    navigate("/");
  };

  return (
    <header className="adventure-portal-bar">
      <div className="adventure-portal-topline">
        <div className="adventure-portal-brand">
          <div className="adventure-portal-mark">AA</div>
          <div>
            <strong>Arcana Academy</strong>
            <span>A legend you write yourself</span>
          </div>
        </div>

        {user && (
          <div className="adventure-portal-account">
            <div className="adventure-portal-avatar" aria-hidden="true">{initial}</div>
            <div className="adventure-portal-usercopy">
              <strong>{user.username}</strong>
              <span>{user.email}</span>
            </div>
            <button type="button" onClick={logout}>Logout</button>
          </div>
        )}
      </div>

      <div className="adventure-portal-navrow">
        <nav className="adventure-portal-group" aria-label="Arcana world navigation">
          <span className="adventure-portal-label">World</span>
          {WORLD_LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/" || link.to === "/adventure"}
              className={({ isActive }) => `adventure-portal-link${isActive ? " active" : ""}`}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        {user && (
          <nav className="adventure-portal-group" aria-label="Player content navigation">
            <span className="adventure-portal-label">Your Stuff</span>
            {USER_LINKS.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => `adventure-portal-link${isActive ? " active" : ""}`}
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
