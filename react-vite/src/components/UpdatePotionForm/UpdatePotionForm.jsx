import { useDispatch, useSelector } from 'react-redux';
import * as potionActions from '../../redux/potion';
import { useModal } from '../../context/Modal';
import './UpdatePotionForm.css';
import { useState } from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchOnePotion } from '../../redux/potion';


function UpdatePotionForm() {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const sessionUser = useSelector(state => state.session.user);
  const potion = useSelector(state => state.potion.currentPotion || []);
  const navigate = useNavigate();

  const [url, setUrl] = useState(potion.url)
  const [name, setName] = useState(potion.name)
  const [description, setDescription]= useState(potion.description)
  const [regeneration, setRegeneration] = useState(potion.regeneration)
  const [cost, setCost] = useState(potion.cost)
  const [type, setType] = useState(potion.mtype)
  const [element, setElement] = useState(potion.element)


  const handleSubmit = async (e) => {
    e.preventDefault();    // prevent default form submission

    try {
      const potionData = {
        id: potion.id,
        user_id: sessionUser.id,
        url,
        name,
        description,
        regeneration,
        cost,
        type,
        element
      };

      dispatch(potionActions.updatePotion(potion.id, potionData));
      alert("Potion updated successfully!");
      closeModal();
      navigate(`/potions/${potion.id}`)
    } catch (error) {
      alert(error.message || "Failed to update potion");
    }
  };


  useEffect(() => {
    // console.log("potion id:",potion.id)
    dispatch(fetchOnePotion(potion.id));

  }, [dispatch, potion.id]);


  return (
    <div className='create-confirm'>
      <h1
      className='create-potion-title'
      >Update Your Potion</h1>


      <form
      onSubmit={handleSubmit}
      className='create-potion-form'
      >


        <label
        className='create-potion-labels'
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
        className='create-potion-labels'
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
        className='create-potion-labels'
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
        className='create-potion-labels'
        >
        Regeneration
        <input
        className='inputs'
        placeholder='Regeneration'
        type="decimal"
        value={regeneration}
        onChange={(e) => setRegeneration(e.target.value)}
        required
        />
        </label>

        <label
        className='create-potion-labels'
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


        <div
        className='select-type-container'
        >
          <label htmlFor="type">Type</label>
          <br />
          <select
            id="type-select"
            name="type"
            value={type}
            onChange={(e) => setType(e.target.value)}          >

            <option
            className='beautiful-dropdown'
            value="">----Choose Type----</option>
            <option
            className='beautiful-dropdown-health'
            value="health">Health</option>
            <option
            className='beautiful-dropdown-mana'
            value="mana">Mana</option>


          </select>
        </div>


      <p className='confirm-create-text'>
        Are you sure you want to update this potion?
      </p>

        <div className="button-container">
          <button
            type="submit"
            className='create-potion-button'
          >
            Yes (Update Potion)
             {/* {`${potion.id}`} */}
          </button>

          <button
            // use "type=submit" to type="button" so it doesn't submit the form
            type="button"
            onClick={closeModal}
            className='keep-potion-button'
          >
            No (Return)
          </button>
        </div>
      </form>
    </div>
  );
}


export default UpdatePotionForm;
