import { NavLink, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import "./AdventurePortalBar.css";

const COMMUNITY_LINKS = [
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
    <aside className="adventure-portal-bar" aria-label="Arcana Academy navigation">
      <div className="adventure-portal-brand">
        <div className="adventure-portal-mark">AA</div>
        <div>
          <strong>Arcana Academy</strong>
          <span>A legend you write yourself</span>
        </div>
      </div>

      <div className="adventure-portal-account">
        <div className="adventure-portal-avatar" aria-hidden="true">{initial}</div>
        <div className="adventure-portal-usercopy">
          <strong>{user ? user.username : "Guest"}</strong>
          <span>{user ? user.email : "Sign in to enter the Academy"}</span>
        </div>
      </div>

      <nav className="adventure-portal-group" aria-label="Community navigation">
        <span className="adventure-portal-label">Community</span>
        {COMMUNITY_LINKS.map((link) => (
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
        <nav className="adventure-portal-group" aria-label="Your stuff navigation">
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

      {user ? (
        <div className="adventure-portal-group adventure-portal-account-actions">
          <span className="adventure-portal-label">Account</span>
          <button className="adventure-portal-logout" type="button" onClick={logout}>Logout</button>
        </div>
      ) : (
        <div className="adventure-portal-auth" aria-label="Account actions">
          <span className="adventure-portal-label">Account</span>
          <OpenModalButton
            className="adventure-portal-auth-button"
            buttonText="Log In"
            modalComponent={<LoginFormModal />}
          />
          <OpenModalButton
            className="adventure-portal-auth-button"
            buttonText="Sign Up"
            modalComponent={<SignupFormModal />}
          />
        </div>
      )}
    </aside>
  );
}
