import { useEffect, useState } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";
import { csrfFetch } from "../../redux/csrf";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import "./AdventurePortalBar.css";

const GAME_DAY_MS = 6 * 60 * 60 * 1000;

const COLLECTION_LINKS = [
  { to: "/spells/all", label: "Spells" },
  { to: "/swords/all", label: "Swords" },
  { to: "/potions/all", label: "Potions" },
  { to: "/coming-soon", label: "Bestiary" },
];

const ACADEMY_LINKS = [
  { screen: "town", to: "/adventure", label: "Academy Square" },
  { screen: "forest", to: "/adventure?screen=forest", label: "The Forest" },
  { screen: "healer", to: "/adventure?screen=healer", label: "Healer" },
  { screen: "weapons", to: "/adventure?screen=weapons", label: "Weapon Shop" },
  { screen: "armor", to: "/adventure?screen=armor", label: "Armor Shop" },
  { screen: "bank", to: "/adventure?screen=bank", label: "Academy Bank" },
];

const USER_LINKS = [
  { to: "/players", label: "Your Players" },
  { to: "/spells", label: "Your Spells" },
  { to: "/potions", label: "Your Potions" },
  { to: "/swords", label: "Your Swords" },
];

function formatCountdown(milliseconds) {
  const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return [hours, minutes, seconds].map((value) => String(value).padStart(2, "0")).join(":");
}

export default function AdventurePortalBar() {
  const user = useSelector((store) => store.session.user);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const initial = user?.username?.[0]?.toUpperCase() || "?";
  const [advState, setAdvState] = useState(null);
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (!user) {
      setAdvState(null);
      return undefined;
    }

    let cancelled = false;

    const loadAdventureState = async () => {
      try {
        const response = await csrfFetch("/api/adventure/state");
        const data = await response.json();
        if (!cancelled && data.state) setAdvState(data.state);
      } catch {
        if (!cancelled) setAdvState(null);
      }
    };

    const receiveAdventureState = (event) => {
      if (event.detail) setAdvState(event.detail);
    };

    loadAdventureState();
    const poller = window.setInterval(loadAdventureState, 4000);
    window.addEventListener("arcana:adventure-state", receiveAdventureState);

    return () => {
      cancelled = true;
      window.clearInterval(poller);
      window.removeEventListener("arcana:adventure-state", receiveAdventureState);
    };
  }, [user]);

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  const logout = async () => {
    await dispatch(thunkLogout());
    navigate("/");
  };

  const hpPercent = advState
    ? Math.max(0, Math.min(100, (advState.hp / Math.max(1, advState.max_hp)) * 100))
    : 0;
  const manaPercent = advState
    ? Math.max(0, Math.min(100, (advState.mana / Math.max(1, advState.max_mana)) * 100))
    : 0;
  const xpPercent = advState
    ? Math.min(100, (advState.xp / Math.max(1, advState.xp_required)) * 100)
    : 0;
  const nextNewDayAt = advState ? (Number(advState.game_day) + 1) * GAME_DAY_MS : 0;
  const remainingUntilNewDay = advState ? Math.max(0, nextNewDayAt - now) : 0;
  const newDayReady = Boolean(advState) && remainingUntilNewDay <= 0;
  const nextNewDayLocalTime = advState
    ? new Date(nextNewDayAt).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })
    : "";
  const requestedAdventureScreen = location.pathname === "/adventure"
    ? new URLSearchParams(location.search).get("screen") || "town"
    : null;
  const activeAdventureScreen = ACADEMY_LINKS.some((link) => link.screen === requestedAdventureScreen)
    ? requestedAdventureScreen
    : location.pathname === "/adventure" ? "town" : null;

  return (
    <aside className="adventure-portal-bar" aria-label="Arcana Academy navigation">
      <div className="adventure-portal-account adventure-portal-account-top">
        <div className="adventure-portal-avatar" aria-hidden="true">{initial}</div>
        <div className="adventure-portal-usercopy">
          <strong>{user ? user.username : "Guest"}</strong>
          <span>{user ? user.email : "Sign in to enter the Academy"}</span>
        </div>
      </div>

      <div className="adventure-portal-brand">
        <div className="adventure-portal-mark">AA</div>
        <div>
          <strong>Arcana Academy</strong>
          <span>A legend you write yourself</span>
        </div>
      </div>

      {user && (
        <div className="adventure-portal-sticky">
          {advState ? (
            <section className="adventure-portal-stats" aria-label="Adventure character stats">
              <div className="adventure-portal-stats-heading">
                <span className="adventure-portal-label">Character</span>
                <strong>{advState.title}</strong>
              </div>

              <div className="adventure-portal-stat"><span>Level</span><strong>{advState.level}</strong></div>
              <div className="adventure-portal-stat"><span>HP</span><strong>{advState.hp}/{advState.max_hp}</strong></div>
              <div className="adventure-portal-meter hp"><div style={{ width: `${hpPercent}%` }} /></div>
              <div className="adventure-portal-stat"><span>Mana</span><strong>{advState.mana}/{advState.max_mana}</strong></div>
              <div className="adventure-portal-meter mana"><div style={{ width: `${manaPercent}%` }} /></div>
              <div className="adventure-portal-stat"><span>Forest Fights</span><strong>{advState.turns}/{advState.max_forest_fights}</strong></div>

              <div className={`adventure-portal-new-day${newDayReady ? " ready" : ""}`} aria-live="polite">
                <span>Next New Day</span>
                <strong>{newDayReady ? "NEW DAY READY" : formatCountdown(remainingUntilNewDay)}</strong>
                <small>{newDayReady ? "Next action refreshes turns." : `Reset at ${nextNewDayLocalTime}`}</small>
              </div>

              <div className="adventure-portal-stat"><span>Gold</span><strong>{advState.gold}</strong></div>
              <div className="adventure-portal-stat"><span>Bank</span><strong>{advState.bank_gold}</strong></div>
              <div className="adventure-portal-stat"><span>Gems</span><strong>{advState.gems}</strong></div>
              <div className="adventure-portal-stat"><span>Attack</span><strong>{advState.effective_attack}</strong></div>
              <div className="adventure-portal-stat"><span>Defense</span><strong>{advState.effective_defense}</strong></div>
              <div className="adventure-portal-stat"><span>Dragon Kills</span><strong>{advState.dragon_kills}</strong></div>
              <div className="adventure-portal-stat"><span>Dragon Points</span><strong>{advState.dragon_points}</strong></div>

              <div className="adventure-portal-xp">
                <span>Experience {advState.xp}/{advState.xp_required}</span>
                <div className="adventure-portal-meter xp"><div style={{ width: `${xpPercent}%` }} /></div>
              </div>

              <div className="adventure-portal-equipment">
                <span>{advState.weapon?.name || "No weapon"}</span>
                <span>{advState.armor?.name || "No armor"}</span>
              </div>
            </section>
          ) : (
            <section className="adventure-portal-stats adventure-portal-stats-loading">
              <span className="adventure-portal-label">Character</span>
              <strong>Loading character stats…</strong>
            </section>
          )}

          <nav className="adventure-portal-adventure-nav" aria-label="Academy destinations">
            <span className="adventure-portal-label">Academy</span>
            {ACADEMY_LINKS.map((link) => (
              <Link
                key={link.screen}
                to={link.to}
                className={`adventure-portal-link${activeAdventureScreen === link.screen ? " active" : ""}`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
      )}

      <nav className="adventure-portal-group" aria-label="Collections navigation">
        <span className="adventure-portal-label">Collections</span>
        {COLLECTION_LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
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
