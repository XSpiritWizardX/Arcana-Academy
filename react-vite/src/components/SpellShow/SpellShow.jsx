import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchOneSpell } from "../../redux/spell";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import UpdateSpellForm from "../UpdateSpellForm/UpdateSpellForm"
import DeleteSpellModal from "../DeleteSpell/DeleteSpellModal";
import { useParams } from "react-router-dom";
import './SpellShow.css'


function SpellShow() {
  const dispatch = useDispatch();
  const currentSpell = useSelector(state => state.spell.currentSpell || [])
//   const spells = useSelector(state => state.spell.spell || [])
const spellUserId = currentSpell.user_id
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);
    const {spellId} = useParams()
    console.log("currentSpellId:", spellId)
  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchOneSpell(spellId))
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, spellId]);

  if (isLoading) {
    return <div className="spell-container">Loading spell...</div>;
  }



  return (
    <div className="spell-show-container">

      <h1
      className="spell-list-title"
      >SPELL DETAILS</h1>
    { spellUserId === user?.id ? (

          <div
          className="spell-show-card"
          >
            <h2>{currentSpell.name}</h2>
            <img
            className="spell-show-image"
            src={currentSpell.url}
            />
            <br/>
            <p
            className="spell-show-text"
            >{currentSpell.description}</p>


            <p
            className="spell-show-text"
            >Element :  {currentSpell.element}</p>

            <p
            className="spell-show-text-gold"
            >Gold Cost : {currentSpell.cost}</p>


            <p
            className="spell-show-text-blue"
            >Mana Cost : {currentSpell.mana_cost}</p>


            <p
            className="spell-show-text-red"
            >Damage : {currentSpell.damage}</p>



<div
                className="spell-modal-buttons"
                >
                <OpenModalButton
                className="update-spell-button"
                buttonText="UPDATE"

                modalComponent={<UpdateSpellForm spellId={currentSpell.id}/>}
              />
              <OpenModalButton
                className="delete-spell-button"
                buttonText="DELETE"

                modalComponent={<DeleteSpellModal spellId={currentSpell.id}/>}
              />
                </div>



          </div>
    ):(
      <div
      className="spell-show-card"
      >
        <h2>{currentSpell.name}</h2>
        <img
        className="spell-show-image"
        src={currentSpell.url}
        />
        <br/>
        <p
        className="spell-show-text"
        >{currentSpell.description}</p>


        <p
        className="spell-show-text"
        >Element :  {currentSpell.element}</p>

        <p
        className="spell-show-text-gold"
        >Gold Cost : {currentSpell.cost}</p>


        <p
        className="spell-show-text-blue"
        >Mana Cost : {currentSpell.mana_cost}</p>


        <p
        className="spell-show-text-red"
        >Damage : {currentSpell.damage}</p>





      </div>
    )}








    </div>



  );
}

export default SpellShow;
