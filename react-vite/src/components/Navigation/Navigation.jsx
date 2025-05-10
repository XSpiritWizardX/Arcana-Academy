import { NavLink } from "react-router-dom";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";

function Navigation() {
  return (
    <div
    className="nav-bar"
    >

      <ProfileButton
     className="profile-button"
      />


        <NavLink to="/"
        className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1746905940/jhNonsuSc8ShAi6pP60N--0--x7uaq_bg-rmvd_sf5lbe.png"  />
        HOME
        </NavLink>



        <NavLink to="/coming-soon"
        className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460859/TiisO45JvVhdMXUaM7ow--0--b4glo_bg-rmvd_rbtkpx.png"  />
        EVENTS
        </NavLink>


        <NavLink to="/spells/all"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745484826/Am7bR1jx4aUXvJbRpWQw--0--cw7p8_bg-rmvd_jr24ip.png"  />
        SPELLS
        </NavLink>

        <NavLink to="/potions/all"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745484971/GiJw0GJ1Rdwf8p5r7KUS--0--d0hqh_bg-rmvd_nki2rx.png"  />
        POTIONS
        </NavLink>


        <NavLink to="/swords/all"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485348/wklz2vTQExQbcA60FuJc--0--tooyc_bg-rmvd_i2vsng.png"  />
        SWORDS
        </NavLink>


        <NavLink to="/coming-soon"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460862/3WM05YxM5PzHXWcGmasV--0--93a4s_bg-rmvd_unzcvg.png"  />
        BESTIARY
        </NavLink>



    </div>
  );
}

export default Navigation;
