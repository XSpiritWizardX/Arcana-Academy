import { csrfFetch } from "./csrf";

const CREATE_POTION = 'potion/createPotion';
const SET_ONE_POTION = 'potion/onePotion';
const REMOVE_POTION = 'potion/removePotion';
const GET_POTIONS = 'potion/getPotions';
const GET_ALL_POTIONS = 'potion/getAllPotions';
const UPDATE_POTION = 'potion/updatePotion';





// action creators
const addPotion = (potion) => ({
  type: CREATE_POTION,
  payload: potion
});

const setOnePotion = (potion) => ({
    type: SET_ONE_POTION,
    payload: potion,
  });

const removePotionId = (potionId) => ({
  type: REMOVE_POTION,
  potionId
});

const getPotions = (potions) => ({
  type: GET_POTIONS,
  payload: potions
});

const getAllPotions = (potions) => ({
  type: GET_ALL_POTIONS,
  payload: potions
});

const updatePotionAction = (potion) => ({
  type: UPDATE_POTION,
  payload: potion
});

// Thunk action creators
export const fetchPotions = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/potions/', {
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getPotions(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching potions:', error);
    throw error;
  }
};



export const fetchAllPotions = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/potions/all', {

    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getAllPotions(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching all potions:', error);
    throw error;
  }
};





export const fetchOnePotion = (potionId) => async (dispatch) => {
  try {
    const response = await fetch(`/api/potions/${potionId}`, {

    });
    console.log('fetchOnePotion response:', response)
    console.log("potion id:")

    if (response.ok) {
      const potion = await response.json();
      console.log(potion)
      dispatch(setOnePotion(potion));
      return potion;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch potion');
    }
  } catch (error) {
    console.error('Error fetching potion', {error});
    throw error;
  }
};


export const createPotion = (potionData) => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/potions/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(potionData),
      credentials: 'include'   // send auth. cookies in request
    });

    if (response.ok) {
      const data = await response.json();

      dispatch(addPotion(data));
      // after creating a potion, fetch all potions to update the state
      dispatch(fetchPotions());
      return data;
    } else {
      // handle non-OK responses
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to create potion');
    }
  } catch (error) {
    console.error('Error creating potion:', error);
    throw error;
  }
};


export const deletePotion = (potionId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/potions/${potionId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete potion');  // Prevents misleading success alerts
    }

    dispatch(removePotionId(potionId)); // Update Redux state
    return 'Potion deleted successfully'; // Ensure frontend knows it worked
  } catch (error) {
    console.error('Delete Error:', error); // Log error to console
    throw error; // Ensures the frontend properly handles the failure
  }
};



export const updatePotion = (potionId, potionData) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/potions/${potionId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(potionData),
    });

    if (response.ok) {
      const updatedPotion = await response.json();
      dispatch(updatePotionAction(updatedPotion));
      return updatedPotion;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update potion');
    }
  } catch (error) {
    console.error('Error updating potion:', error);
    throw error;
  }
};


const initialState = { potions: null, currentPotion: null };

function potionReducer(state = initialState, action) {
  switch (action.type) {
    case CREATE_POTION:
      return { ...state, currentPotion: action.payload };

    case SET_ONE_POTION:
      return { ...state, currentPotion: action.payload };

    case REMOVE_POTION:
      return {
        ...state,
        potions: state.potions.filter(potion => potion.id !== action.potionId)
      };

    case GET_POTIONS:
    case GET_ALL_POTIONS:
      return { ...state, potions: action.payload.potions };

    case UPDATE_POTION:
      return { ...state, currentPotion: action.payload };

    default:
      return state;
  }
}




export default potionReducer;
