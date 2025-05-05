import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllSwords } from "../../redux/sword";
import { NavLink } from 'react-router-dom';
import './SwordList.css'



function SwordCard() {
  const dispatch = useDispatch();
  // Access the swords array from the correct location in state
  const swords = useSelector(state => state.sword.swords || []);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    dispatch(fetchAllSwords())
      .then(() => setIsLoading(false))
      .catch(() => setIsLoading(false));
  }, [dispatch]);

  if (isLoading) {
    return <div className="swords-container">Loading swords...</div>;
  }

  return (
    <div className="sword-list-container">
      <div>
        <h1 className="sword-list-title">SWORDS</h1>
        <div className="sword-list">
          {swords?.map((sword) => (
            <div key={sword.id} className="sword-card">
              <NavLink to={`/swords/${sword.id}`} className="sword-nav-link">
                <h2 className="sword-name">{sword.name}</h2>
                <img className="sword-image" src={sword.url} alt={sword.name} />
                <p className="sword-description">Description: {sword.description}</p>
                <p className="sword-element">element: {sword.element}</p>
                <p className="sword-cost">gold cost: {sword.cost}</p>
                <p className="sword-mana-cost">mana cost: {sword.mana_cost}</p>
                <p className="sword-damage">Damage: {sword.damage}</p>
              </NavLink>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}



export default SwordCard;
