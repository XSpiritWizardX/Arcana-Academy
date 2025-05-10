import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { thunkLogout } from "../../redux/session";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./ProfileButton.css";

function ProfileButton() {
  const dispatch = useDispatch();
  const [showMenu, setShowMenu] = useState(false);
  const user = useSelector((store) => store.session.user);
  // const session = useSelector((store) => store.session);
  const ulRef = useRef();
  const navigate = useNavigate();

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
    navigate('/')
  };

  return (
    <>


      <img
      onClick={toggleMenu}
      className="nav-logo"
      src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460861/hm1Zq9Ih3p0Adhj7eGLp--0--ulhyr_bg-rmvd_wikfdy.png"></img>
      <h1
      className="user-interface"
      >MENU</h1>


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

              <NavLink to="coming-soon"
              className="pro-bar-text"
              >
              BATTLE
              </NavLink>

              <NavLink to="/players/"
              className="pro-bar-text"
              >
              YOUR PLAYERS
              </NavLink>

              <NavLink to="/spells/"
              className="pro-bar-text"
              >
              YOUR SPELLS
              </NavLink>

              <NavLink to="/potions/"
              className="pro-bar-text"
              >
              YOUR POTIONS
              </NavLink>

              <NavLink to="/swords/"
              className="pro-bar-text"
              >
              YOUR SWORDS
              </NavLink>






              <NavLink to="/coming-soon"
              className="pro-bar-text"
              >
              YOUR SCHEDULE
              </NavLink>


              <NavLink to="/coming-soon"
              className="pro-bar-text"
              >
              YOUR EVENTS
              </NavLink>


              <NavLink to="/coming-soon"
              className="pro-bar-text"
              >
              YOUR REVIEWS
              </NavLink>

              <NavLink to="/coming-soon"
              className="pro-bar-text"
              >
              ANGEL REBIRTH
              </NavLink>


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
                className="auth-button-login"
                buttonText="Log In"
                onButtonClick={closeMenu}
                modalComponent={<LoginFormModal />}
              />
              <OpenModalButton
                className="auth-button-signup"
                buttonText="Sign Up"
                onButtonClick={closeMenu}
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
