import { NavLink } from "react-router-dom";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";

function Navigation() {


  return (

    <div className="navigation-container">

      <NavLink
      to="/"
      className="nav-link"
      >
        <img src="https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745460813/PigZ34Z1EbOSrle1I22d--0--qafvf_bg-rmvd_bofljj.png" alt="Arcana Academy Logo" className="logo" />
      </NavLink>

      <ProfileButton
      className="profile-button"
      />

      </div>


  );
}

export default Navigation;
