import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FaUserCircle } from 'react-icons/fa';
import { thunkLogout } from "../../redux/session";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import "./ProfileButton.css";

function ProfileButton() {
  const dispatch = useDispatch();
  const [showMenu, setShowMenu] = useState(false);
  const user = useSelector((store) => store.session.user);
  const session = useSelector((store) => store.session);
  const ulRef = useRef();

  const toggleMenu = (e) => {
    e.stopPropagation(); // Keep from bubbling up to document and triggering closeMenu
    setShowMenu(!showMenu);
  };

  useEffect(() => {
    if (!showMenu) return;

    const closeMenu = (e) => {
      if (ulRef.current && !ulRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", closeMenu);

    return () => document.removeEventListener("click", closeMenu);
  }, [showMenu]);

  const closeMenu = () => setShowMenu(false);

  const logout = (e) => {
    e.preventDefault();
    dispatch(thunkLogout());
    closeMenu();
  };

  return (
    <>
      <button

      onClick={toggleMenu}
      className="profile-button">
        <FaUserCircle />
      </button>
      {showMenu && (
        <div className={"profile-dropdown"} ref={ulRef}>
          {user ? (
            <div
            className="profile-dropdown-container">
            <p
            className="user-stats"
            >

              {user.username}
            </p>

            <p
            className="user-stats"
            >
              {user.email}
            </p>

              <div
              className="divider"
              >

              </div>
            <p
            className="user-stats-level"
            >
              Level: {session.level}
            </p>

            <p
            className="user-stats-xp"
            >
            Experience: {session.experience}
              </p>

            <p
            className="user-stats-health"
            >
            Health: {session.health}
              </p>

              <p
              className="user-stats-mana"
              >Mana: {session.mana}
              </p>

            <p
            className="user-stats-gold"
            >
            Gold: {session.gold}
              </p>

              <p
              className="user-stats"
              >
                Power: {session.power}
              </p>

            <p
            className="user-stats"
            >
              Speed: {session.speed}
            </p>



              <button
              className="logout-button"
              onClick={logout}
              >Log Out
              </button>

            </div>
          ) : (
            <div
            className="auth-button-container"
            >
              <OpenModalButton
                className="auth-button"
                buttonText="Log In"
                onItemClick={closeMenu}
                modalComponent={<LoginFormModal />}
              />
              <OpenModalButton
                className="auth-button"
                buttonText="Sign Up"
                onItemClick={closeMenu}
                modalComponent={<SignupFormModal />}
              />
            </div>
          )}
        </div>
      )}
    </>
  );
}

export default ProfileButton;
