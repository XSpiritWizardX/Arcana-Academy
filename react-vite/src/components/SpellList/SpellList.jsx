import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllSpells } from "../../redux/spell";
// import { NavLink } from 'react-router-dom';
import './SpellList.css'



function SpellCard() {
  const dispatch = useDispatch();
  const spells = useSelector(state => state.spell.spell || [])
  // const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchAllSpells())
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch]);

  if (isLoading) {
    return <div className="spells-container">Loading spells...</div>;
  }



  return (
    <div className="spell-list-container">
        <div>
          <h1
          className="spell-list-title"
          >SPELLS</h1>
          {/* <NavLink to="/spells" className="all-spells-link">
          All Spells
          </NavLink> */}
          <div
          className="spell-list"
          >

          {spells?.spells?.map((spell) => (
            <div key={spell.id} className="spell-card">
              <h2
              className="spell-name"
              >{spell.name}</h2>
              <img className="spell-image" src={spell.url} alt={spell.name} />
              <p
              className="spell-description"
              >Description: {spell.description}</p>
              <p
              className="spell-element"
              >element: {spell.element}</p>
              <p
              className="spell-cost"
              >gold cost: {spell.cost}</p>
              <p
              className="spell-mana-cost"
              >mana cost: {spell.mana_cost}</p>
              <p
              className="spell-damage"
              >Damage: {spell.damage}</p>

            </div>
          ))}

          </div>



        </div>

    </div>
  );
}

export default SpellCard;
