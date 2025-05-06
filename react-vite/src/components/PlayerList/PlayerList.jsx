import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllPlayers } from "../../redux/player";
import { NavLink } from 'react-router-dom';
import './PlayerList.css'



function PlayerCard() {
  const dispatch = useDispatch();
  const players = useSelector(state => state.player.players || [])
  // const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchAllPlayers())
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch]);

  if (isLoading) {
    return <div className="players-container">Loading players...</div>;
  }



  return (
    <div className="player-list-container">
        <div>
          <h1
          className="player-list-title"
          >PLAYERS</h1>

          <div
          className="player-list"
          >

{players?.map((player) => (
            <div key={player.id} className="player-card">
              <NavLink
              to={`/players/${player.id}`}
              className="player-image-container"
              >
              <h2
              className="player-name"
              >{player.name}</h2>

              <img className="player-image" src={player.url} alt={player.name} />



              <p
              className="player-magic_class"
              >{player.magic_class}</p>

              <p
              className="player-element"
              >element: {player.element}</p>

              <p
              className="player-level"
              >level: {player.level}</p>

              <p
              className="player-xp"
              >xp: {player.xp}</p>

              <p
              className="player-gold"
              >gold:{player.gold}</p>

              <p
              className="player-health"
              >health: {player.health}</p>

              <p
              className="player-mana"
              >mana: {player.mana}</p>

              <p
              className="player-damage"
              >damage: {player.damage}</p>
                    <p
              className="player-speed"
              >speed: {player.speed}</p>

              <p
              className="player-strength"
              >strength: {player.strength}</p>

              <p
              className="player-intellect"
              >intellect: {player.intellect}</p>

              <p
              className="player-dexterity"
              >dexterity: {player.dexterity}</p>
                    <p
              className="player-vitality"
              >vitality: {player.vitality}</p>




              </NavLink>



            </div>
          ))}

          </div>



        </div>

    </div>
  );
}

export default PlayerCard;
