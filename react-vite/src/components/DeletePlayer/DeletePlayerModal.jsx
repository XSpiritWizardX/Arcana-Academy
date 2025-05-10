


import * as playerActions from '../../redux/player';
import { useDispatch } from 'react-redux';
import { useModal } from '../../context/Modal';
import './DeletePlayerModal.css';
import { useNavigate } from 'react-router-dom';

// import { useParams } from 'react-router-dom';


function DeletePlayerModal({playerId}) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  // const playerId = useParams()
  const handleSubmit = async () => {
    // console.log("Player ID before deleting:", playerId);
    if (!playerId) {
      alert("Error: No player ID provided!");  // Debugging check
      return;
    }

    try {
      dispatch(playerActions.deletePlayer(playerId));
      alert("Player deleted successfully!");
      navigate(`/players`);

      closeModal();
    } catch (error) {
      alert(error.message);
    }
  };



  return (

    <div className='delete-confirm'>
      <h1>Confirm Delete</h1>

      <p
      className='confirm-delete-text'
      >
      Are you sure you want to remove this player?
      {/* {`${playerId}`} */}
      </p>
      <form
      className='delete-player-form'
      onSubmit={handleSubmit}>




        <button type="submit"
          onClick={handleSubmit}
          className='delete-player-button'
        >
          Yes (Delete Player)
          </button>


          <button type="submit"
          onClick={closeModal}
          className='keep-player-button'
        >
          No (Keep Player)
          </button>


      </form>
    </div>


  );
}






export default DeletePlayerModal;
