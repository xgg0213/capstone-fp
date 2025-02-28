import { csrfFetch } from './csrf';

// Action Types
const LOAD_WATCHLISTS = 'watchlists/LOAD_WATCHLISTS';
const ADD_WATCHLIST = 'watchlists/ADD_WATCHLIST';
const REMOVE_WATCHLIST = 'watchlists/REMOVE_WATCHLIST';

// Action Creators
const loadWatchlists = (watchlists) => ({
  type: LOAD_WATCHLISTS,
  payload: watchlists
});

const addWatchlist = (watchlist) => ({
  type: ADD_WATCHLIST,
  payload: watchlist
});

const removeWatchlist = (watchlistId) => ({
  type: REMOVE_WATCHLIST,
  payload: watchlistId
});

// Thunks
export const getWatchlists = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/watchlist/');
    if (response.ok) {
      const data = await response.json();
      dispatch(loadWatchlists(data.watchlists));
      return data.watchlists;
    }
  } catch (error) {
    console.error('Error fetching watchlists:', error);
  }
};

export const createWatchlist = (name) => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/watchlist/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name })
    });
    if (response.ok) {
      const watchlist = await response.json();
      dispatch(addWatchlist(watchlist));
      return watchlist;
    }
  } catch (error) {
    console.error('Error creating watchlist:', error);
  }
};

// Reducer
const initialState = {
  watchlists: []
};

const watchlistReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOAD_WATCHLISTS:
      return {
        ...state,
        watchlists: action.payload
      };
    case ADD_WATCHLIST:
      return {
        ...state,
        watchlists: [...state.watchlists, action.payload]
      };
    case REMOVE_WATCHLIST:
      return {
        ...state,
        watchlists: state.watchlists.filter(list => list.id !== action.payload)
      };
    default:
      return state;
  }
};

export default watchlistReducer; 