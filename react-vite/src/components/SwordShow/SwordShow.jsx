import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchOneSword } from "../../redux/sword";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import UpdateSwordForm from "../UpdateSwordForm/UpdateSwordForm"
import DeleteSwordModal from "../DeleteSword/DeleteSwordModal";
import { useParams } from "react-router-dom";
import './SwordShow.css'


function SwordShow() {
  const dispatch = useDispatch();
  const currentSword = useSelector(state => state.sword.currentSword || [])
//   const spells = useSelector(state => state.spell.spell || [])
const swordUserId = currentSword.user_id
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);
    const {swordId} = useParams()
    console.log("currentSwordId:", swordId)
  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchOneSword(swordId))
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, swordId]);

  if (isLoading) {
    return <div className="sword-container">Loading sword...</div>;
  }



  return (
    <div className="sword-show-container">

      <h1
      className="sword-list-title"
      >SWORD DETAILS</h1>
    { swordUserId === user?.id ? (

          <div
          className="sword-show-card"
          >
            <h2>{currentSword.name}</h2>
            <img
            className="sword-show-image"
            src={currentSword.url}
            />
            <br/>
            <p
            className="sword-show-text"
            >{currentSword.description}</p>


            <p
            className="sword-show-text"
            >Element :  {currentSword.element}</p>

            <p
            className="sword-show-text-gold"
            >Gold Cost : {currentSword.cost}</p>


            <p
            className="sword-show-text-blue"
            >Mana Cost : {currentSword.mana_cost}</p>


            <p
            className="sword-show-text-red"
            >Damage : {currentSword.damage}</p>



<div
                className="sword-modal-buttons"
                >
                <OpenModalButton
                className="update-sword-button"
                buttonText="UPDATE"

                modalComponent={<UpdateSwordForm swordId={currentSword.id}/>}
              />
              <OpenModalButton
                className="delete-sword-button"
                buttonText="DELETE"

                modalComponent={<DeleteSwordModal swordId={currentSword.id}/>}
              />
                </div>



          </div>
    ):(
      <div
      className="sword-show-card"
      >
        <h2>{currentSword.name}</h2>
        <img
        className="sword-show-image"
        src={currentSword.url}
        />
        <br/>
        <p
        className="sword-show-text"
        >{currentSword.description}</p>


        <p
        className="sword-show-text"
        >Element :  {currentSword.element}</p>

        <p
        className="sword-show-text-gold"
        >Gold Cost : {currentSword.cost}</p>


        <p
        className="sword-show-text-blue"
        >Mana Cost : {currentSword.mana_cost}</p>


        <p
        className="sword-show-text-red"
        >Damage : {currentSword.damage}</p>





      </div>
    )}








    </div>



  );
}

export default SwordShow;
