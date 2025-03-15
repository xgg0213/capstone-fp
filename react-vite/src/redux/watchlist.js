import { csrfFetch } from './csrf';

// Action Types
const LOAD_WATCHLISTS = 'watchlists/LOAD_WATCHLISTS';
const ADD_WATCHLIST = 'watchlists/ADD_WATCHLIST';
const REMOVE_WATCHLIST = 'watchlists/REMOVE_WATCHLIST';
const REMOVE_SYMBOL = 'watchlists/REMOVE_SYMBOL';
const ADD_SYMBOL = 'watchlists/ADD_SYMBOL';
const SET_WATCHED_SYMBOLS = 'watchlists/SET_WATCHED_SYMBOLS';
const SET_ERROR = 'watchlists/SET_ERROR';
const UPDATE_WATCHLIST = 'watchlists/UPDATE_WATCHLIST';

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

const removeSymbol = (watchlistId, symbol) => ({
  type: REMOVE_SYMBOL,
  payload: { watchlistId, symbol }
});

const addSymbol = (symbol) => ({
  type: ADD_SYMBOL,
  payload: symbol
});

const setWatchedSymbols = (symbols) => ({
  type: SET_WATCHED_SYMBOLS,
  payload: symbols
});

const setError = (error) => ({
  type: SET_ERROR,
  payload: error
});

const updateWatchlist = (watchlist) => ({
  type: UPDATE_WATCHLIST,
  payload: watchlist
});

// Thunks
export const getWatchlists = () => async (dispatch) => {
  try {
    const response = await csrfFetch('/api/watchlist/');
    if (response.ok) {
      const data = await response.json();
      dispatch(loadWatchlists(data.watchlists));
      
      // Extract all watched symbols from watchlists
      const watchedSymbols = new Set();
      data.watchlists.forEach(watchlist => {
        watchlist.symbols.forEach(symbol => {
          watchedSymbols.add(symbol.symbol);
        });
      });
      dispatch(setWatchedSymbols(Array.from(watchedSymbols)));
      
      return data.watchlists;
    }
  } catch (error) {
    console.error('Error fetching watchlists:', error);
    dispatch(setError(error.toString()));
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
    dispatch(setError(error.toString()));
  }
};

export const addSymbolToWatchlist = (watchlistId, symbol) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/watchlist/${watchlistId}/symbols`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ symbol: symbol.toUpperCase() })
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(addSymbol(symbol.toUpperCase()));
      await dispatch(getWatchlists()); // Refresh watchlists to get updated data
      return { success: true, data };
    } else {
      const errorData = await response.json();
      dispatch(setError(errorData.errors || 'Failed to add to watchlist'));
      return { success: false, errors: errorData.errors };
    }
  } catch (error) {
    console.error('Error adding symbol to watchlist:', error);
    dispatch(setError(error.toString()));
    return { success: false, errors: [error.toString()] };
  }
};

export const checkSymbolInWatchlist = (symbol) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/watchlist/${symbol}/check`);
    if (response.ok) {
      const data = await response.json();
      return data.isWatched;
    }
    return false;
  } catch (error) {
    console.error('Error checking if symbol is in watchlist:', error);
    return false;
  }
};

export const removeSymbolFromWatchlist = (watchlistId, symbol) => async (dispatch) => {
  // try {
    const response = await csrfFetch(`/api/watchlist/${watchlistId}/symbols/${symbol}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      // Dispatch action to update state
      dispatch(removeSymbol(watchlistId, symbol));
      // Return success
      return true;
    } else {
      const errorData = await response.json();
      console.error('Error removing symbol:', errorData.error);
      dispatch(setError(errorData.error));
      return false;
    }
  // } 
};

export const updateWatchlistName = (watchlistId, name) => async (dispatch) => {
  // try {
    const response = await csrfFetch(`/api/watchlist/${watchlistId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name })
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(updateWatchlist(data));
      return { success: true };
    } else {
      const errorData = await response.json();
      dispatch(setError(errorData.errors || 'Failed to update watchlist name'));
      return errorData;
    }
  // } 
  // catch (error) {
  //   console.error('Error updating watchlist name:', error);
  //   dispatch(setError(error.toString()));
  //   return { success: false, errors: [error.toString()] };
  // }
};

export const deleteWatchlist = (watchlistId) => async (dispatch) => {
  try {
    const response = await csrfFetch(`/api/watchlist/${watchlistId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      dispatch(removeWatchlist(watchlistId));
      return { success: true };
    } else {
      const errorData = await response.json();
      dispatch(setError(errorData.errors || 'Failed to delete watchlist'));
      return { success: false, errors: errorData.errors };
    }
  } catch (error) {
    console.error('Error deleting watchlist:', error);
    dispatch(setError(error.toString()));
    return { success: false, errors: [error.toString()] };
  }
};

// Reducer
const initialState = {
  watchlists: [],
  watchedSymbols: [],
  error: null
};

const watchlistReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOAD_WATCHLISTS:
      return {
        ...state,
        watchlists: action.payload,
        error: null
      };
    case ADD_WATCHLIST:
      return {
        ...state,
        watchlists: [...state.watchlists, action.payload],
        error: null
      };
    case REMOVE_WATCHLIST:
      return {
        ...state,
        watchlists: state.watchlists.filter(list => list.id !== action.payload),
        error: null
      };
    case REMOVE_SYMBOL:
      // This is handled by the getWatchlists refresh, but we could optimize it here
      return {
        ...state,
        error: null
      };
    case ADD_SYMBOL:
      return {
        ...state,
        watchedSymbols: [...state.watchedSymbols, action.payload],
        error: null
      };
    case SET_WATCHED_SYMBOLS:
      return {
        ...state,
        watchedSymbols: action.payload,
        error: null
      };
    case SET_ERROR:
      return {
        ...state,
        error: action.payload
      };
    case UPDATE_WATCHLIST:
      return {
        ...state,
        watchlists: state.watchlists.map(list =>
          list.id === action.payload.id ? action.payload : list
        ),
        error: null
      };
    default:
      return state;
  }
};

export default watchlistReducer; 