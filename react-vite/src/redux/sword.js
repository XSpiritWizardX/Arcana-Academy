import { csrfFetch } from "./csrf";

const CREATE_SWORD = 'sword/createSword';
const SET_ONE_SWORD = 'sword/oneSword';
const REMOVE_SWORD = 'sword/removeSword';
const GET_SWORDS = 'sword/getSwords';
const GET_ALL_SWORDS = 'sword/getAllSwords';
const UPDATE_SWORD = 'sword/updateSword';





// action creators
const addSword = (sword) => ({
  type: CREATE_SWORD,
  payload: sword
});

const setOneSword = (sword) => ({
    type: SET_ONE_SWORD,
    payload: sword,
  });

const removeSwordId = (swordId) => ({
  type: REMOVE_SWORD,
  swordId
});

const getSwords = (swords) => ({
  type: GET_SWORDS,
  payload: swords
});

const getAllSwords = (swords) => ({
  type: GET_ALL_SWORDS,
  payload: swords
});

const updateSwordAction = (sword) => ({
  type: UPDATE_SWORD,
  payload: sword
});

// Thunk action creators
export const fetchSwords = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/swords/', {
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getSwords(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching swords:', error);
    throw error;
  }
};



export const fetchAllSwords = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/swords/all', {

    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getAllSwords(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching all swords:', error);
    throw error;
  }
};





export const fetchOneSword = (swordId) => async (dispatch) => {
  try {
    const response = await fetch(`/api/swords/${swordId}`, {

    });
    console.log('fetchOneSword response:', response)
    console.log("sword id:")

    if (response.ok) {
      const sword = await response.json();
      console.log(sword)
      dispatch(setOneSword(sword));
      return sword;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch sword');
    }
  } catch (error) {
    console.error('Error fetching sword', {error});
    throw error;
  }
};


export const createSword = (swordData) => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/swords/', {
      method: 'POST',
      body: swordData,
    });

    const data = await response.json();

    dispatch(addSword(data));
    // after creating a sword, fetch all swords to update the state
    dispatch(fetchSwords());
    return data;
  } catch (error) {
    console.error('Error creating sword:', error);
    if (error.json) {
      const errorData = await error.json();
      throw new Error(errorData.error || errorData.message || 'Failed to create sword');
    }
    throw error;
  }
};


export const deleteSword = (swordId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/swords/${swordId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete sword');  // Prevents misleading success alerts
    }

    dispatch(removeSwordId(swordId)); // Update Redux state
    return 'Sword deleted successfully'; // Ensure frontend knows it worked
  } catch (error) {
    console.error('Delete Error:', error); // Log error to console
    throw error; // Ensures the frontend properly handles the failure
  }
};



export const updateSword = (swordId, swordData) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/swords/${swordId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(swordData),
    });

    if (response.ok) {
      const updatedSword = await response.json();
      dispatch(updateSwordAction(updatedSword));
      return updatedSword;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update sword');
    }
  } catch (error) {
    console.error('Error updating sword:', error);
    throw error;
  }
};


const initialState = { swords: null, currentSword: null };

function swordReducer(state = initialState, action) {
  switch (action.type) {
    case CREATE_SWORD:
      return { ...state, currentSword: action.payload };

    case SET_ONE_SWORD:
      return { ...state, currentSword: action.payload };

    case REMOVE_SWORD:
      return {
        ...state,
        swords: state.swords.filter(sword => sword.id !== action.swordId)
      };

    case GET_SWORDS:
    case GET_ALL_SWORDS:
      return { ...state, swords: action.payload.swords };

    case UPDATE_SWORD:
      return { ...state, currentSword: action.payload };

    default:
      return state;
  }
}




export default swordReducer;
