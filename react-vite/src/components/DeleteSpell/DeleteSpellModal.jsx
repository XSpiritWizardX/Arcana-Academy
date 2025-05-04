


import * as spellActions from '../../redux/spell';
import { useDispatch } from 'react-redux';
import { useModal } from '../../context/Modal';
import './DeleteSpellModal.css';
import { useNavigate } from 'react-router-dom';

// import { useParams } from 'react-router-dom';


function DeleteSpellModal({spellId}) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  // const spellId = useParams()
  const handleSubmit = async () => {
    console.log("Spell ID before deleting:", spellId);
    if (!spellId) {
      alert("Error: No Spell ID provided!");  // Debugging check
      return;
    }

    try {
      dispatch(spellActions.deleteSpell(spellId));
      alert("Spell deleted successfully!");
      navigate(`/spells`);

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
      Are you sure you want to remove this spell? {`${spellId}`}
      </p>
      <form
      className='delete-spell-form'
      onSubmit={handleSubmit}>




        <button type="submit"
          onClick={handleSubmit}
          className='delete-spell-button'
        >
          Yes (Delete Spell)
          </button>


          <button type="submit"
          onClick={closeModal}
          className='keep-spell-button'
        >
          No (Keep Spell)
          </button>


      </form>
    </div>


  );
}






export default DeleteSpellModal;
