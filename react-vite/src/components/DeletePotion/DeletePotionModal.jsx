


import * as potionActions from '../../redux/potion';
import { useDispatch } from 'react-redux';
import { useModal } from '../../context/Modal';
import './DeletePotionModal.css';
import { useNavigate } from 'react-router-dom';

// import { useParams } from 'react-router-dom';


function DeletePotionModal({potionId}) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  // const potionId = useParams()
  const handleSubmit = async () => {
    console.log("Potion ID before deleting:", potionId);
    if (!potionId) {
      alert("Error: No potion ID provided!");  // Debugging check
      return;
    }

    try {
      dispatch(potionActions.deletePotion(potionId));
      alert("Potion deleted successfully!");
      navigate(`/potions`);

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
      Are you sure you want to remove this potion? {`${potionId}`}
      </p>
      <form
      className='delete-potion-form'
      onSubmit={handleSubmit}>




        <button type="submit"
          onClick={handleSubmit}
          className='delete-potion-button'
        >
          Yes (Delete Potion)
          </button>


          <button type="submit"
          onClick={closeModal}
          className='keep-potion-button'
        >
          No (Keep Potion)
          </button>


      </form>
    </div>


  );
}






export default DeletePotionModal;
