import { csrfFetch } from "./csrf";

const CREATE_PLAYER = 'player/createPlayer';
const SET_ONE_PLAYER = 'player/onePlayer';
const REMOVE_PLAYER = 'player/removePlayer';
const GET_PLAYERS = 'player/getPlayers';
const GET_ALL_PLAYERS = 'player/getAllPlayers';
const UPDATE_PLAYER = 'player/updatePlayer';





// action creators
const addPlayer = (player) => ({
  type: CREATE_PLAYER,
  payload: player
});

const setOnePlayer = (player) => ({
    type: SET_ONE_PLAYER,
    payload: player,
  });

const removePlayerId = (playerId) => ({
  type: REMOVE_PLAYER,
  playerId
});

const getPlayers = (players) => ({
  type: GET_PLAYERS,
  payload: players
});

const getAllPlayers = (players) => ({
  type: GET_ALL_PLAYERS,
  payload: players
});

const updatePlayerAction = (player) => ({
  type: UPDATE_PLAYER,
  payload: player
});

// Thunk action creators
export const fetchPlayers = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/players/', {
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getPlayers(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching players:', error);
    throw error;
  }
};



export const fetchAllPlayers = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/players/all', {

    });

    if (response.ok) {
      const data = await response.json();
      dispatch(getAllPlayers(data));
      return data;
    }
  } catch (error) {
    console.error('Error fetching all players:', error);
    throw error;
  }
};





export const fetchOnePlayer = (playerId) => async (dispatch) => {
  try {
    const response = await fetch(`/api/players/${playerId}`, {

    });
    console.log('fetchOnePlayer response:', response)
    console.log("player id:")

    if (response.ok) {
      const player = await response.json();
      console.log(player)
      dispatch(setOnePlayer(player));
      return player;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch player');
    }
  } catch (error) {
    console.error('Error fetching player', {error});
    throw error;
  }
};


export const createPlayer = (playerData) => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/players/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(playerData),
      credentials: 'include'   // send auth. cookies in request
    });

    if (response.ok) {
      const data = await response.json();

      dispatch(addPlayer(data));
      // after creating a player, fetch all players to update the state
      dispatch(fetchPlayers());
      return data;
    } else {
      // handle non-OK responses
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to create player');
    }
  } catch (error) {
    console.error('Error creating player:', error);
    throw error;
  }
};


export const deletePlayer = (playerId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/players/${playerId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete player');  // Prevents misleading success alerts
    }

    dispatch(removePlayerId(playerId)); // Update Redux state
    return 'Player deleted successfully'; // Ensure frontend knows it worked
  } catch (error) {
    console.error('Delete Error:', error); // Log error to console
    throw error; // Ensures the frontend properly handles the failure
  }
};



export const updatePlayer = (playerId, playerData) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/players/${playerId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(playerData),
    });

    if (response.ok) {
      const updatedPlayer = await response.json();
      dispatch(updatePlayerAction(updatedPlayer));
      return updatedPlayer;
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to update player');
    }
  } catch (error) {
    console.error('Error updating player:', error);
    throw error;
  }
};


const initialState = { players: null, currentPlayer: null };

function playerReducer(state = initialState, action) {
  switch (action.type) {
    case CREATE_PLAYER:
      return { ...state, currentPlayer: action.payload };

    case SET_ONE_PLAYER:
      return { ...state, currentPlayer: action.payload };

    case REMOVE_PLAYER:
      return {
        ...state,
        players: state.players.filter(player => player.id !== action.playerId)
      };

    case GET_PLAYERS:
    case GET_ALL_PLAYERS:
      return { ...state, players: action.payload.players };

    case UPDATE_PLAYER:
      return { ...state, currentPlayer: action.payload };

    default:
      return state;
  }
}




export default playerReducer;
