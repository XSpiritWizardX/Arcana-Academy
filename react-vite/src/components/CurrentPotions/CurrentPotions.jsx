import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchPotions } from "../../redux/potion";
import OpenModalButton from "../OpenModalButton/OpenModalButton";

import PotionForm from "../PotionForm/PotionForm";

import { NavLink } from 'react-router-dom';
import './CurrentPotions.css'



function PotionCard() {
  const dispatch = useDispatch();
  const potions = useSelector(state => state.potion.potions || [])
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchPotions())
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, user]);

  if (isLoading) {
    return <div className="potions-container">Loading potions...</div>;
  }



  return (
    <div className="potion-list-container">
        <div>

            <div
            className="title-cont"
            >
                <h1
                className="potion-list-title"
                >YOUR POTIONS</h1>
                      <OpenModalButton
                className="create-potion-button"
                buttonText="Create A New Potion"

                modalComponent={<PotionForm />}
              />
            </div>

          <div
          className="potion-list"
          >

          {potions?.map((potion) => (
            <div key={potion.id} className="potion-card">
              <NavLink
              to={`/potions/${potion.id}`}
              className="potion-image-container"
              >
              <h2
              className="potion-name"
              >{potion.name}</h2>

              <img className="potion-image" src={potion.url} alt={potion.name} />



              <p
              className="potion-description"
              >{potion.description}</p>
              <p
              className="potion-element"
              >element: {potion.element}</p>
              <p
              className="potion-cost"
              >gold cost: {potion.cost}</p>
              <p
              className="potion-mana-cost"
              >type: {potion.type}</p>
              <p
              className="potion-damage"
              >regeneration: {potion.regeneration}</p>

              </NavLink>



            </div>
          ))}




          </div>



        </div>

    </div>
  );
}

export default PotionCard;
