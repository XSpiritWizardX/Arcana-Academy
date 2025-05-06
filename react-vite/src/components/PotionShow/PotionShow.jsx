import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchOnePotion } from "../../redux/potion";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import UpdatePotionForm from "../UpdatePotionForm/UpdatePotionForm"
import DeletePotionModal from "../DeletePotion/DeletePotionModal";
import { useParams } from "react-router-dom";
import './PotionShow.css'


function PotionShow() {
  const dispatch = useDispatch();
  const currentPotion = useSelector(state => state.potion.currentPotion || [])
const potionUserId = currentPotion.user_id
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);
    const {potionId} = useParams()
    console.log("currentPotionId:", potionId)
  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchOnePotion(potionId))
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, potionId]);

  if (isLoading) {
    return <div className="potion-container">Loading potion...</div>;
  }



  return (
    <div className="potion-show-container">

      <h1
      className="potion-list-title"
      >POTION DETAILS</h1>
    { potionUserId === user?.id ? (

          <div
          className="potion-show-card"
          >
            <h2>{currentPotion.name}</h2>
            <img
            className="potion-show-image"
            src={currentPotion.url}
            />
            <br/>
            <p
            className="potion-show-text"
            >{currentPotion.description}</p>


            <p
            className="potion-show-text"
            >Element :  {currentPotion.element}</p>

            <p
            className="potion-show-text-gold"
            >Gold Cost : {currentPotion.cost}</p>


            <p
            className="potion-show-text-blue"
            >Type : {currentPotion.type}</p>


            <p
            className="potion-show-text-red"
            >Regeneration : {currentPotion.regeneration}</p>



<div
                className="potion-modal-buttons"
                >
                <OpenModalButton
                className="update-potion-button"
                buttonText="UPDATE"

                modalComponent={<UpdatePotionForm potionId={currentPotion.id}/>}
              />
              <OpenModalButton
                className="delete-potion-button"
                buttonText="DELETE"

                modalComponent={<DeletePotionModal potionId={currentPotion.id}/>}
              />
                </div>



          </div>
    ):(
      <div
      className="potion-show-card"
      >
        <h2>{currentPotion.name}</h2>
        <img
        className="potion-show-image"
        src={currentPotion.url}
        />
        <br/>
        <p
        className="potion-show-text"
        >{currentPotion.description}</p>


        <p
        className="potion-show-text"
        >Element :  {currentPotion.element}</p>

        <p
        className="potion-show-text-gold"
        >Gold Cost : {currentPotion.cost}</p>


        <p
        className="potion-show-text-blue"
        >Type : {currentPotion.type}</p>


        <p
        className="potion-show-text-red"
        >Regeneration : {currentPotion.regeneration}</p>





      </div>
    )}








    </div>



  );
}

export default PotionShow;
