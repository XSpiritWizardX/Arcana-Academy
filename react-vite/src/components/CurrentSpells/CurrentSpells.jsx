import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchSpells } from "../../redux/spell";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import UpdateSpellForm from "../UpdateSpellForm/UpdateSpellForm"
import DeleteSpellModal from "../DeleteSpell/DeleteSpellModal";
import SpellForm from "../SpellForm/SpellForm";

import { NavLink } from 'react-router-dom';
import './CurrentSpells.css'



function SpellCard() {
  const dispatch = useDispatch();
  const spells = useSelector(state => state.spell.spell || [])
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchSpells())
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, user]);

  if (isLoading) {
    return <div className="spells-container">Loading spells...</div>;
  }

//   const closeMenu = (e) => {
//     if (ulRef.current && !ulRef.current.contains(e.target)) {
//       setShowMenu(false);
//     }
//   };

  return (
    <div className="spell-list-container">
        <div>

            <div
            className="title-cont"
            >
                <h1
                className="spell-list-title"
                >YOUR SPELLS</h1>
                      <OpenModalButton
                className="create-spell-button"
                buttonText="Create A New Spell"

                modalComponent={<SpellForm />}
              />
            </div>

          <div
          className="spell-list"
          >

          {spells?.spells?.map((spell) => (
            <div key={spell.id} className="spell-card">
              <h2
              className="spell-name"
              >{spell.name}</h2>

              <NavLink
              to={`/spells/${spell.id}`}
              className="spell-image-container"
              >
              <img className="spell-image" src={spell.url} alt={spell.name} />

              </NavLink>


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

                <div
                className="spell-modal-buttons"
                >
                <OpenModalButton
                className="update-spell-button"
                buttonText="UPDATE"

                modalComponent={<UpdateSpellForm spellId={spell.id}/>}
              />
              <OpenModalButton
                className="delete-spell-button"
                buttonText="DELETE"

                modalComponent={<DeleteSpellModal spellId={spell.id}/>}
              />
                </div>


            </div>
          ))}




          </div>



        </div>

    </div>
  );
}

export default SpellCard;
