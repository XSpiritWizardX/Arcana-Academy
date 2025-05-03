import { csrfFetch } from "./csrf";

const CREATE_SPELL = 'spell/createSpell';
const SET_ONE_SPELL = 'spell/oneSpell';
const REMOVE_SPELL = 'spell/removeSpell';
const GET_SPELLS = 'spell/getSpells';
const GET_ALL_SPELLS = 'spell/getAllSpells';
const UPDATE_SPELL = 'spell/updateSpell';





// action creators
const addSpell = (spell) => ({
  type: CREATE_SPELL,
  payload: spell
});

// change this to updateSpell
const setOneSpell = (spell) => ({
    type: SET_ONE_SPELL,
    payload: spell,
  });

const removeSpellId = (spellId) => ({
  type: REMOVE_SPELL,
  spellId
});

const getSpells = (spells) => ({
  type: GET_SPELLS,
  payload: spells
});

const getAllSpells = (spells) => ({
  type: GET_ALL_SPELLS,
  payload: spells
});

const updateSpellAction = (spell) => ({
  type: UPDATE_SPELL,
  payload: spell
});

// Thunk action creators
export const fetchSpells = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/spells/', {
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getSpells(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching spells:', error);
    throw error;
  }
};



export const fetchAllSpells = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/spells/all', {

    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getAllSpells(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching all spells:', error);
    throw error;
  }
};





export const fetchOneSpell = (spellId) => async (dispatch) => {
  try {
    const response = await fetch(`/api/spells/${spellId}`, {

    });
    console.log('fetchOneSpell response:', response)
    console.log("spell id:")

    if (response.ok) {
      const spell = await response.json();
      console.log(spell)
      dispatch(setOneSpell(spell));
      return spell;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch spell');
    }
  } catch (error) {
    console.error('Error fetching spell', error);
    throw error;
  }
};


export const createSpell = (spellData) => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/spells/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(spellData),
      credentials: 'include'   // send auth. cookies in request
    });

    if (response.ok) {
      const data = await response.json();

      dispatch(addSpell(data));
      // after creating a portfolio, fetch all spells to update the state
      dispatch(fetchSpells());
      return data;
    } else {
      // handle non-OK responses
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to create spell');
    }
  } catch (error) {
    console.error('Error creating spell:', error);
    throw error;
  }
};


export const deleteSpell = (spellId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/spells/${spellId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete spell');  // Prevents misleading success alerts
    }

    dispatch(removeSpellId(spellId)); // Update Redux state
    return 'Spell deleted successfully'; // Ensure frontend knows it worked
  } catch (error) {
    console.error('Delete Error:', error); // Log error to console
    throw error; // Ensures the frontend properly handles the failure
  }
};


// export const updateSpell = (spellId, spellData) => async (dispatch) => {
//   try {
//     const response = await csrfFetch(`/api/spells/${spellId}`, {
//       method: 'PUT',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(spellData),
//       credentials: 'include'
//     });

//     if (response.ok) {
//       const data = await response.json();
//       dispatch(updateSpellAction(data));
//       // after updating, fetch all spells to update the state
//       dispatch(fetchSpells());
//       return data;
//     } else {
//       const errorData = await response.json();
//       throw new Error(errorData.message || 'Failed to update spell');
//     }
//   } catch (error) {
//     console.error('Error updating spell:', error);
//     throw error;
//   }
// };
export const updateSpell = (spellId, spellData) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/spells/${spellId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(spellData),
    });

    if (response.ok) {
      const updatedSpell = await response.json();
      dispatch(updateSpellAction(updatedSpell));
      return updatedSpell;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update spell');
    }
  } catch (error) {
    console.error('Error updating spell:', error);
    throw error;
  }
};


const initialState = { spell: null, currentSpell: null };


// Reducer
function spellReducer(state = initialState, action) {
  switch (action.type) {

    case CREATE_SPELL:
        return { ...state, spell: action.payload };

    case SET_ONE_SPELL:
        return { currentSpell: action.payload };

    // updated to handle deletion of single spell or entry in port array:
    case REMOVE_SPELL: {
      const newState = { ...state };
      if (newState.spell && newState.spell.spells) {
        // if we have a spells array, filter out the deleted one
        newState.spell.spells = newState.spell.spells.filter(
          spell => spell.id !== action.spellId
        );
      } else {
        // if we're dealing with a single spell and it matches the ID, set to null
        if (newState.spell && newState.spell.id === action.spellId) {
          newState.spell = null;
        }
      }
      return newState;
    }

    case GET_SPELLS:
      return { ...state, spell: action.payload };

    case GET_ALL_SPELLS:
      return { ...state, spell: action.payload };

    case UPDATE_SPELL:
      return { currentSpell: action.payload };

    default:
        return state;
  }
}



export default spellReducer;
