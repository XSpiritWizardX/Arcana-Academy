import "./Footer.css";
import { NavLink } from "react-router-dom";


function FooterCard() {

  return (
    <div className="foot-container">

      <footer
      className="foot"
      >
        <div
        className="resource-col"
        >
          <h5
          className="gets"
          >Get Connected</h5>

        <div
        to='/coming-soon'
        className='foot-links'
        >

        <NavLink to='/coming-soon'
        className='foot-links'
        >
          Connectivity
          </NavLink>
        </div>

        <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Dashboard
          </NavLink>
          </div>

          <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Terms of Service
          </NavLink>
        </div>

        <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Privacy Policy
          </NavLink>
          </div>

          <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Third-Party Cookies
          </NavLink>
          </div>

        </div>

        <div
        className="resource-col"
        >

          <h5>Resources</h5>

          <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Using Arcana Academy</NavLink>
          </div>

          <a
          href='https://github.com/XSpiritWizardX/Arcana-Academy/wiki'
          target="_self"
          className='foot-links'
          >Docs
          </a>

          <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Support
          </NavLink>
          </div>

          <div
        to='/coming-soon'
        className='foot-links'
        >
          <NavLink
          to='/coming-soon'
          className='foot-links'
          >Supported Hardware
          </NavLink>
          </div>
      </div>

      <div
      className="resource-col"
      >
        <h5>Pricing</h5>

        <div
      to='/coming-soon'
      className='foot-links'
      >
      <NavLink to='/coming-soon'
      className='foot-links'
      >
        Pricing Overview
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Flexible Plans
        </NavLink>
          </div>

          <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >High Volume Data
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Free Version
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <a
        to='/coming-soon'
        className='foot-links'
        >Subscriptions
        </a>
        </div>

      </div>

        {/* DEVELOPERS */}
      <div
      className="resource-col"
      >
        <h5>Developers</h5>

        <div
      to='/coming-soon'
      className='foot-links'
      >
      <NavLink to='/coming-soon'
      className='foot-links'
      >
        Forum
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >
          Projects
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >
          Team Comments
        </NavLink>
        </div>

      </div>

        {/* COMPANY */}
      <div
      className="resource-col"
      >

        <h5>Company</h5>

        <div
      to='/coming-soon'
      className='foot-links'
      >
      <NavLink to='/coming-soon'
      className='foot-links'
      >
        About Us
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Blog
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Partnerships
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Affiliate Program
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Careers
        </NavLink>
        </div>
      </div>

        {/* SOCIAL */}

      <div
      className="resource-col"
      >

        <h5>Social</h5>

        <div
      to='/coming-soon'
      className='foot-links'
      >
      <NavLink to='/coming-soon'
      className='foot-links'
      >
        Twitter
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Facebook
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Linkedin
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Github
        </NavLink>
        </div>

        <div
      to='/coming-soon'
      className='foot-links'
      >
        <NavLink
        to='/coming-soon'
        className='foot-links'
        >Discord
        </NavLink>
        </div>

      </div>

    </footer>

      <p
      className="copyright-text"
      >@2025 ArcanaAcademy</p>

    </div>
  );
}

export default FooterCard;
