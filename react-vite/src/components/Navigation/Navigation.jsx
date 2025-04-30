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
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460813/PigZ34Z1EbOSrle1I22d--0--qafvf_bg-rmvd_bofljj.png"  />
        HOME
        </NavLink>



        <NavLink to="/"
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

        <NavLink to="/"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745484971/GiJw0GJ1Rdwf8p5r7KUS--0--d0hqh_bg-rmvd_nki2rx.png"  />
        POTIONS
        </NavLink>


        <NavLink to="/"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485348/wklz2vTQExQbcA60FuJc--0--tooyc_bg-rmvd_i2vsng.png"  />
        SWORDS
        </NavLink>

        <NavLink to="/"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460862/3WM05YxM5PzHXWcGmasV--0--93a4s_bg-rmvd_unzcvg.png"  />
        BESTIARY
        </NavLink>

        <NavLink to="/"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460861/52pMCncY7299YlmPJExv--0--61l2j_bg-rmvd_nhsmvi.png"  />
        ANGEL REBIRTH
        </NavLink>

        <NavLink to="/"
         className="nav-bar-text"
        >
        <img
        className="nav-logo"
        src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460813/PigZ34Z1EbOSrle1I22d--0--qafvf_bg-rmvd_bofljj.png"  />
        BATTLE
        </NavLink>

    </div>
  );
}

export default Navigation;
