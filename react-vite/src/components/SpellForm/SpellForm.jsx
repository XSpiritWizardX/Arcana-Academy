import { useDispatch, useSelector } from 'react-redux';
import * as spellActions from '../../redux/spell';
import { useModal } from '../../context/Modal';
import './SpellForm.css';
import { useState } from 'react';


function SpellForm() {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const sessionUser = useSelector(state => state.session.user);
  console.log(`Trying to get user ID: ${ sessionUser }`)
  const [url, setUrl] = useState("")
  const [name, setName] = useState("")
  const [description, setDescription]= useState("")
  const [damage, setDamage] = useState("")
  const [cost, setCost] = useState("")
  const [manaCost, setManaCost] = useState("")
  const [element, setElement] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault();    // prevent default form submission

    try {
      // Default portfolio data plus user_id from sessionUser
      const spellData = {
        user_id: sessionUser.id,
        url: url,
        name: name,
        description: description,
        damage:damage,
        cost: cost,
        mana_cost: manaCost,
        element: element
      };

      await dispatch(spellActions.createSpell(spellData));
      alert("Spell created successfully!");
      closeModal();
    } catch (error) {
      alert(error.message || "Failed to create spell");
    }
  };

  return (
    <div className='create-confirm'>
      <h1
      className='create-spell-title'
      >Confirm New Spell</h1>


      <form
      onSubmit={handleSubmit}
      className='create-spell-form'
      >


        <label
        className='create-spell-labels'
        >
        Name
        <input
        className='inputs'
        placeholder='Name'
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
        />
        </label>



        <label
        className='create-spell-labels'
        >
        Image Url
        <input
        className='inputs'
        placeholder='URL'
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        required
        />
        </label>





        {/* <select
          value={element}
          onChange={(e) => setElement(e.target.value)}
          className='element-select'
          required

        >
            ELEMENT
          <option value="">-- Select an element --</option>

            <option>
                "Fire"
            </option>

        </select> */}
        <label
        className='create-spell-labels'
        >
        Element
        <input
        className='inputs'
        placeholder='Element'
        type="text"
        value={element}
        onChange={(e) => setElement(e.target.value)}
        required
        />
        </label>

        <label
        className='create-spell-labels'
        >
        Description
        <input
        className='inputs'
        placeholder='up to 256 characters'
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
        />
        </label>

        <label
        className='create-spell-labels'
        >
        Damage
        <input
        className='inputs'
        placeholder='Damage'
        type="decimal"
        value={damage}
        onChange={(e) => setDamage(e.target.value)}
        required
        />
        </label>

        <label
        className='create-spell-labels'
        >
        Cost
        <input
        className='inputs'
        placeholder='Cost'
        type="decimal"
        value={cost}
        onChange={(e) => setCost(e.target.value)}
        required
        />
        </label>

        <label
        className='create-spell-labels'
        >
        Mana Cost
        <input
        className='inputs'
        placeholder='Mana Cost'
        type="decimal"
        value={manaCost}
        onChange={(e) => setManaCost(e.target.value)}
        required
        />
        </label>


      <p className='confirm-create-text'>
        Are you sure you want to create this spell?
      </p>

        <div className="button-container">
          <button
            type="submit"
            className='create-spell-button'
          >
            Yes (Create Spell)
          </button>

          <button
            // use "type=submit" to type="button" so it doesn't submit the form
            type="button"
            onClick={closeModal}
            className='keep-spell-button'
          >
            No (Return)
          </button>
        </div>
      </form>
    </div>
  );
}


export default SpellForm;
