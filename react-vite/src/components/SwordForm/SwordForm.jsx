import { useDispatch, useSelector } from 'react-redux';
import * as swordActions from '../../redux/sword';
import { useModal } from '../../context/Modal';
import './SwordForm.css';
import { useState } from 'react';


function SwordForm() {
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
      const swordData = {
        user_id: sessionUser.id,
        url: url,
        name: name,
        description: description,
        damage:damage,
        cost: cost,
        mana_cost: manaCost,
        element: element
      };

      await dispatch(swordActions.createSword(swordData));
      alert("Sword created successfully!");
      closeModal();
    } catch (error) {
      alert(error.message || "Failed to create sword");
    }
  };

  return (
    <div className='create-confirm'>
      <h1
      className='create-sword-title'
      >Confirm New Sword</h1>


      <form
      onSubmit={handleSubmit}
      className='create-sword-form'
      >


        <label
        className='create-sword-labels'
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
        className='create-sword-labels'
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




        <div
        className='select-el-container'
        >
          <label htmlFor="element">Element</label>
          <br />
          <select
            id="element-select"
            name="element"
            value={element}
            onChange={(e) => setElement(e.target.value)}          >

            <option
            className='beautiful-dropdown'
            value="">----Choose Element----</option>
            <option
            className='beautiful-dropdown-fire'
            value="Fire">Fire</option>
            <option
            className='beautiful-dropdown-water'
            value="Water">Water</option>
            <option
            className='beautiful-dropdown-earth'
            value="Earth">Earth</option>
            <option
            className='beautiful-dropdown-ice'
            value="Ice">Ice</option>
            <option
            className='beautiful-dropdown-wind'
            value="Wind">Wind</option>
            <option
            className='beautiful-dropdown-light'
            value="Light">Light</option>
            <option
            className='beautiful-dropdown-dark'
            value="Dark">Dark</option>
            <option
            className='beautiful-dropdown-arcane'
            value="Arcane">Arcane</option>
            <option
            className='beautiful-dropdown-nature'
            value="Nature">Nature</option>
            <option
            className='beautiful-dropdown-gravity'
            value="Gravity">Gravity</option>
            <option
            className='beautiful-dropdown-support'
            value="Support">Support</option>
            <option
            className='beautiful-dropdown-time'
            value="Time">Time</option>
            <option
            className='beautiful-dropdown-electricity'
            value="Electricty">Electricty</option>
            <option
            className='beautiful-dropdown-psychic'
            value="Psychic">Psychic</option>
            <option
            className='beautiful-dropdown-ancient'
            value="Ancient">Ancient</option>
            <option
            className='beautiful-dropdown-life'
            value="Life">Life</option>
            <option
            className='beautiful-dropdown-death'
            value="Death">Death</option>
            <option
            className='beautiful-dropdown-non'
            value="No Element">No Element</option>
          </select>
        </div>





        <label
        className='create-sword-labels'
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
        className='create-sword-labels'
        >
        Gold Cost
        <input
        className='inputs'
        placeholder='1234.56'
        type="decimal"
        value={cost}
        onChange={(e) => setCost(e.target.value)}
        required
        />
        </label>


        <label
        className='create-sword-labels'
        >
        Mana Cost
        <input
        className='inputs'
        placeholder='1234.56'
        type="decimal"
        value={manaCost}
        onChange={(e) => setManaCost(e.target.value)}
        required
        />
        </label>

        <label
        className='create-sword-labels'
        >
        Damage
        <input
        className='inputs'
        placeholder='1234.56'
        type="decimal"
        value={damage}
        onChange={(e) => setDamage(e.target.value)}
        required
        />
        </label>




      <p className='confirm-create-text'>
        Are you sure you want to create this sword?
      </p>

        <div className="button-container">
          <button
            type="submit"
            className='create-sword-button'
          >
            Yes (Create Sword)
          </button>

          <button
            // use "type=submit" to type="button" so it doesn't submit the form
            type="button"
            onClick={closeModal}
            className='keep-sword-button'
          >
            No (Return)
          </button>
        </div>
      </form>
    </div>
  );
}


export default SwordForm;
