import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchOnePlayer } from "../../redux/player";
import OpenModalButton from "../OpenModalButton/OpenModalButton";
import UpdatePlayerForm from "../UpdatePlayerForm/UpdatePlayerForm"
import DeletePlayerModal from "../DeletePlayer/DeletePlayerModal";
import { useParams } from "react-router-dom";
import './PlayerShow.css'


function PlayerShow() {
  const dispatch = useDispatch();
  const currentPlayer = useSelector(state => state.player.currentPlayer || [])
const playerUserId = currentPlayer.user_id
  const user = useSelector(state => state.session.user);
  const [isLoading, setIsLoading] = useState(true);
    const {playerId} = useParams()
    console.log("currentPlayerId:", playerId)
  useEffect(() => {

      setIsLoading(true);
      dispatch(fetchOnePlayer(playerId))
        .then(() => setIsLoading(false))
        .catch(() => setIsLoading(false));

  }, [dispatch, playerId]);

  if (isLoading) {
    return <div className="player-container">Loading player...</div>;
  }



  return (
    <div className="player-show-container">

      <h1
      className="player-list-title"
      >PLAYER DETAILS</h1>
    { playerUserId === user?.id ? (

          <div
          className="potion-show-card"
          >
          <h2
              className="player-name"
              >{currentPlayer.name}</h2>

              <img className="player-image" src={currentPlayer.url} alt={currentPlayer.name} />



              <p
              className="player-magic_class"
              >{currentPlayer.magic_class}</p>

              <p
              className="player-element"
              >element: {currentPlayer.element}</p>

              <p
              className="player-level"
              >level: {currentPlayer.level}</p>

              <p
              className="player-xp"
              >xp: {currentPlayer.xp}</p>

              <p
              className="player-gold"
              >gold:{currentPlayer.gold}</p>

              <p
              className="player-health"
              >health: {currentPlayer.health}</p>

              <p
              className="player-mana"
              >mana: {currentPlayer.mana}</p>

              <p
              className="player-damage"
              >damage: {currentPlayer.damage}</p>
                    <p
              className="player-speed"
              >speed: {currentPlayer.speed}</p>

              <p
              className="player-strength"
              >strength: {currentPlayer.strength}</p>

              <p
              className="player-intellect"
              >intellect: {currentPlayer.intellect}</p>

              <p
              className="player-dexterity"
              >dexterity: {currentPlayer.dexterity}</p>
                    <p
              className="player-vitality"
              >vitality: {currentPlayer.vitality}</p>




<div
                className="player-modal-buttons"
                >
                <OpenModalButton
                className="update-player-button"
                buttonText="UPDATE"

                modalComponent={<UpdatePlayerForm playerId={currentPlayer.id}/>}
              />
              <OpenModalButton
                className="delete-player-button"
                buttonText="DELETE"

                modalComponent={<DeletePlayerModal playerId={currentPlayer.id}/>}
              />
                </div>



          </div>
    ):(
      <div
      className="potion-show-card"
      >
      <h2
              className="player-name"
              >{currentPlayer.name}</h2>

              <img className="player-image" src={currentPlayer.url} alt={currentPlayer.name} />



              <p
              className="player-magic_class"
              >{currentPlayer.magic_class}</p>

              <p
              className="player-element"
              >element: {currentPlayer.element}</p>

              <p
              className="player-level"
              >level: {currentPlayer.level}</p>

              <p
              className="player-xp"
              >xp: {currentPlayer.xp}</p>

              <p
              className="player-gold"
              >gold:{currentPlayer.gold}</p>

              <p
              className="player-health"
              >health: {currentPlayer.health}</p>

              <p
              className="player-mana"
              >mana: {currentPlayer.mana}</p>

              <p
              className="player-damage"
              >damage: {currentPlayer.damage}</p>
                    <p
              className="player-speed"
              >speed: {currentPlayer.speed}</p>

              <p
              className="player-strength"
              >strength: {currentPlayer.strength}</p>

              <p
              className="player-intellect"
              >intellect: {currentPlayer.intellect}</p>

              <p
              className="player-dexterity"
              >dexterity: {currentPlayer.dexterity}</p>
                    <p
              className="player-vitality"
              >vitality: {currentPlayer.vitality}</p>



      </div>
    )}








    </div>



  );
}

export default PlayerShow;
