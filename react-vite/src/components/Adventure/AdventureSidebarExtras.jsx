import { NavLink, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";

const WORLD_LINKS = [
  { to: "/", label: "Town" },
  { to: "/adventure", label: "Adventure" },
  { to: "/spells/all", label: "Spells" },
  { to: "/swords/all", label: "Swords" },
  { to: "/potions/all", label: "Potions" },
  { to: "/coming-soon", label: "Bestiary" },
];

const USER_LINKS = [
  { to: "/players", label: "Your Players" },
  { to: "/spells", label: "Your Spells" },
  { to: "/potions", label: "Your Potions" },
  { to: "/swords", label: "Your Swords" },
];

export function AdventureIdentity() {
  const user = useSelector((store) => store.session.user);
  const initial = user?.username?.[0]?.toUpperCase() || "?";

  return (
    <section className="adventure-identity">
      <div className="adventure-brand">Arcana Academy</div>
      <div className="adventure-tagline">A legend you write yourself</div>
      <div className="adventure-player-card">
        <div className="adventure-avatar" aria-hidden="true">{initial}</div>
        <div className="adventure-player-copy">
          <strong>{user?.username || "Guest"}</strong>
          <span>{user?.email || "Sign in to play"}</span>
        </div>
      </div>
    </section>
  );
}

export function AdventurePortalLinks() {
  const user = useSelector((store) => store.session.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const logout = async () => {
    await dispatch(thunkLogout());
    navigate("/");
  };

  return (
    <section className="adventure-portal-links" aria-label="Arcana navigation">
      <div className="adventure-link-group">
        <div className="adventure-link-heading">World</div>
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
      </div>

      {user && (
        <div className="adventure-link-group">
          <div className="adventure-link-heading">Your Stuff</div>
          {USER_LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `adventure-portal-link${isActive ? " active" : ""}`}
            >
              {link.label}
            </NavLink>
          ))}
          <button className="adventure-logout" type="button" onClick={logout}>Logout</button>
        </div>
      )}
    </section>
  );
}
