


import * as swordActions from '../../redux/sword';
import { useDispatch } from 'react-redux';
import { useModal } from '../../context/Modal';
import './DeleteSwordModal.css';
import { useNavigate } from 'react-router-dom';

// import { useParams } from 'react-router-dom';


function DeleteSwordModal({swordId}) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  // const swordId = useParams()
  const handleSubmit = async () => {
    console.log("Sword ID before deleting:", swordId);
    if (!swordId) {
      alert("Error: No Sword ID provided!");  // Debugging check
      return;
    }

    try {
      dispatch(swordActions.deleteSword(swordId));
      alert("Sword deleted successfully!");
      navigate(`/swords`);

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
      Are you sure you want to remove this sword? {`${swordId}`}
      </p>
      <form
      className='delete-sword-form'
      onSubmit={handleSubmit}>




        <button type="submit"
          onClick={handleSubmit}
          className='delete-sword-button'
        >
          Yes (Delete Sword)
          </button>


          <button type="submit"
          onClick={closeModal}
          className='keep-sword-button'
        >
          No (Keep Sword)
          </button>


      </form>
    </div>


  );
}






export default DeleteSwordModal;
