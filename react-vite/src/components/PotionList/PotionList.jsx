import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllPotions } from "../../redux/potion";
import { NavLink } from 'react-router-dom';
import './PotionList.css'



function PotionCard() {
  const dispatch = useDispatch();
  const potions = useSelector(state => state.potion.potions || [])
  // const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchAllPotions())
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch]);

  if (isLoading) {
    return <div className="potions-container">Loading potions...</div>;
  }



  return (
    <div className="potion-list-container">
        <div>
          <h1
          className="potion-list-title"
          >POTIONS</h1>

          <div
          className="potion-list"
          >

          {potions?.map((potion) => (
            <div key={potion.id} className="potion-card">
                 <NavLink
              to={`/potions/${potion.id}`}
              className="potion-nav-link"
              >
              <h2
              className="potion-name"
              >{potion.name}</h2>
              <img className="potion-image" src={potion.url} alt={potion.name} />
              <p
              className="potion-description"
              >Description: {potion.description}</p>
              <p
              className="potion-element"
              >element: {potion.element}</p>
              <p
              className="potion-cost"
              >Gold cost: {potion.cost}</p>
              <p
              className="potion-type"
              >Type: {potion.type}</p>
              <p
              className="potion-regeneration"
              >Regeneration: {potion.regeneration}</p>
              </NavLink>
            </div>
          ))}

          </div>



        </div>

    </div>
  );
}

export default PotionCard;
