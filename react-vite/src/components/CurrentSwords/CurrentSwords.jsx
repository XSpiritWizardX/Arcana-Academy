import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchSwords } from "../../redux/sword";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import SwordForm from "../../components/SwordForm/SwordForm"

import { NavLink } from 'react-router-dom';
import './CurrentSwords.css'



function SwordCard() {
  const dispatch = useDispatch();
  const swords = useSelector(state => state.sword.swords || [])
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchSwords())
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, user]);

  if (isLoading) {
    return <div className="swords-container">Loading swords...</div>;
  }



  return (
    <div className="sword-list-container">
        <div>

            <div
            className="title-cont"
            >
                <h1
                className="sword-list-title"
                >YOUR SWORDS</h1>
                      <OpenModalButton
                className="create-sword-button"
                buttonText="Create A New Sword"

                modalComponent={<SwordForm />}
              />
            </div>

          <div
          className="sword-list"
          >

          {swords?.map((sword) => (
            <div key={sword.id} className="sword-card">
              <NavLink
              to={`/swords/${sword.id}`}
              className="sword-image-container"
              >
              <h2
              className="sword-name"
              >{sword.name}</h2>

              <img className="sword-image" src={sword.url} alt={sword.name} />



              <p
              className="sword-description"
              >{sword.description}</p>
              <p
              className="sword-element"
              >element: {sword.element}</p>
              <p
              className="sword-cost"
              >gold cost: {sword.cost}</p>
              <p
              className="sword-mana-cost"
              >mana cost: {sword.mana_cost}</p>
              <p
              className="sword-damage"
              >Damage: {sword.damage}</p>

              </NavLink>



            </div>
          ))}




          </div>



        </div>

    </div>
  );
}

export default SwordCard;
