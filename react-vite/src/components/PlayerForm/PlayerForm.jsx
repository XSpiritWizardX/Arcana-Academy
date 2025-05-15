import { useDispatch, useSelector } from 'react-redux';
import * as playerActions from '../../redux/player';
import { useModal } from '../../context/Modal';
import './PlayerForm.css';
import { useState } from 'react';


function PlayerForm() {
  const dispatch = useDispatch();
  const { closeModal } = useModal();
  const sessionUser = useSelector(state => state.session.user);
  console.log(`Trying to get user ID: ${ sessionUser }`)
  const [name, setName] = useState()
  const [url, setUrl] = useState()
  const [magic_class, setMagicClass]= useState()
  const [element, setElement] = useState()
  const [level, setLevel] = useState()
  const [xp, setXp] = useState()
  const [gold, setGold] = useState()
  const [health, setHealth] = useState()
  const [mana, setMana] = useState()
  const [damage, setDamage] = useState()
  const [speed, setSpeed] = useState()
  const [strength, setStrength] = useState()
  const [intellect, setIntellect] = useState()
  const [dexterity, setDexterity] = useState()
  const [vitality, setVitality] = useState()

  const handleSubmit = async (e) => {
    e.preventDefault();    // prevent default form submission

    try {
      const playerData = {
        user_id: sessionUser.id,
        url,
        magic_class,
        name,
        element,
        level,
        xp,
        gold,
        health,
        mana,
        damage,
        speed,
        strength,
        intellect,
        dexterity,
        vitality
      };

      await dispatch(playerActions.createPlayer(playerData));
      alert("Player created successfully!");
      closeModal();
    } catch (error) {
      alert(error.message || "Failed to create player");
    }
  };

  return (
    <div className='create-confirm'>
      <h1
      className='create-player-title'
      >Confirm New Player</h1>


<form
      onSubmit={handleSubmit}
      className='create-player-form'
      >


        <label
        className='create-player-labels'
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
        className='create-player-labels'
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
        className='select-magic-class-container'
        >
          <label htmlFor="type">Magic Class</label>
          <br />
          <select
            id="magic-class-select"
            name="magic-class"
            value={magic_class}
            onChange={(e) => setMagicClass(e.target.value)}          >

            <option
            className='beautiful-dropdown'
            value="">----Choose Magic Class----</option>
            <option
            className='beautiful-dropdown-intellect'
            value="Wizard">Wizard</option>
            <option
            className='beautiful-dropdown-intellect'
            value="Witch">Witch</option>
            <option
            className='beautiful-dropdown-strength'
            value="Warrior">Warrior</option>
            <option
            className='beautiful-dropdown-strength'
            value="Sheild Maiden">Shield Maiden</option>
             <option
            className='beautiful-dropdown-vitality'
            value="Paladin">Paladin</option>
             <option
            className='beautiful-dropdown-vitality'
            value="Priestess">Priestess</option>
             <option
            className='beautiful-dropdown-dexterity'
            value="Archer">Archer</option>
             <option
            className='beautiful-dropdown-dexterity'
            value="Dwarf">Dwarf</option>
             <option
            className='beautiful-dropdown-speed'
            value="Thief"> Thief</option>
             <option
            className='beautiful-dropdown-speed'
            value="from-another-world"> Other Worlder</option>
             <option
            className='beautiful-dropdown-speed'
            value="Farmer"> Farmer</option>


          </select>
        </div>


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
        className='create-player-labels'
        >
        Level
        <input
        className='inputs'
        placeholder='level'
        type="decimal"
        value={level}
        onChange={(e) => setLevel(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Xp
        <input
        className='inputs'
        placeholder='xp'
        type="decimal"
        value={xp}
        onChange={(e) => setXp(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Gold
        <input
        className='inputs'
        placeholder='gold'
        type="decimal"
        value={gold}
        onChange={(e) => setGold(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Health
        <input
        className='inputs'
        placeholder='health'
        type="decimal"
        value={health}
        onChange={(e) => setHealth(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Mana
        <input
        className='inputs'
        placeholder='mana'
        type="decimal"
        value={mana}
        onChange={(e) => setMana(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Damage
        <input
        className='inputs'
        placeholder='damage'
        type="decimal"
        value={damage}
        onChange={(e) => setDamage(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Speed
        <input
        className='inputs'
        placeholder='speed'
        type="decimal"
        value={speed}
        onChange={(e) => setSpeed(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Strength
        <input
        className='inputs'
        placeholder='strength'
        type="decimal"
        value={strength}
        onChange={(e) => setStrength(e.target.value)}
        required
        />
        </label>


        <label
        className='create-player-labels'
        >
        Intellect
        <input
        className='inputs'
        placeholder='intellect'
        type="decimal"
        value={intellect}
        onChange={(e) => setIntellect(e.target.value)}
        required
        />
        </label>



        <label
        className='create-player-labels'
        >
        Dexterity
        <input
        className='inputs'
        placeholder='dexterity'
        type="decimal"
        value={dexterity}
        onChange={(e) => setDexterity(e.target.value)}
        required
        />
        </label>



        <label
        className='create-player-labels'
        >
        Vitality
        <input
        className='inputs'
        placeholder='vitality'
        type="decimal"
        value={vitality}
        onChange={(e) => setVitality(e.target.value)}
        required
        />
        </label>





      <p className='confirm-create-text'>
        Are you sure you want to create this Player?
      </p>

        <div className="button-container">
          <button
            type="submit"
            className='create-potion-button'
          >
            Yes (Create Player)
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


export default PlayerForm;
