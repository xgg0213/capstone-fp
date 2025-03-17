import { csrfFetch } from './csrf';

// Constants
const LOAD_SYMBOLS = 'symbols/LOAD';
const LOAD_SYMBOL = 'symbols/LOAD_SYMBOL';
const UPDATE_SYMBOL_PRICE = 'symbols/UPDATE_SYMBOL_PRICE';
export const SET_ALL_SYMBOLS = 'symbols/SET_ALL_SYMBOLS';
export const FETCH_ALL_SYMBOLS_ERROR = 'symbols/FETCH_ALL_SYMBOLS_ERROR';

// Action Creators
const loadSymbols = (symbols) => ({
    type: LOAD_SYMBOLS,
    symbols
});

const loadSymbol = (symbol) => ({
    type: LOAD_SYMBOL,
    payload: symbol
});

const updateSymbolPrice = (symbol) => ({
    type: UPDATE_SYMBOL_PRICE,
    payload: symbol
});

// Thunks
export const fetchSymbols = () => async dispatch => {
    try {
        const response = await csrfFetch('/api/symbols/');
        if (response.ok) {
            const data = await response.json();
            dispatch(loadSymbols(data.symbols));
            return data.symbols;
        }
    } catch (error) {
        console.error('Error fetching symbols:', error);
        throw error;
    }
};

export const fetchSymbol = (symbol) => async (dispatch) => {
    try {
        console.log("Fetching symbol:", symbol);  // Debug log
        const response = await fetch(`/api/symbols/${symbol}`);
        console.log("Response status:", response.status);  // Debug log
        
        if (response.ok) {
            const data = await response.json();
            console.log("Symbol data received:", data);  // Debug log
            dispatch(loadSymbol(data));
            return data;
        } else {
            const error = await response.json();
            console.error("Error response:", error);  // Debug log
            return null;
        }
    } catch (error) {
        console.error('Error fetching symbol:', error);
        return null;
    }
};

export const fetchSymbolPrices = (symbol) => async () => {
    try {
        const response = await fetch(`/api/symbols/${symbol}/prices`);
        if (response.ok) {
            const data = await response.json();
            return data.prices;
        }
    } catch (error) {
        console.error('Error fetching symbol prices:', error);
        return null;
    }
};

export const updateSymbolPrices = (symbols = []) => async (dispatch) => {
    try {
        const response = await fetch('/api/symbols/update-prices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbols })
        });
        if (response.ok) {
            const data = await response.json();
            data.symbols.forEach(symbol => {
                dispatch(updateSymbolPrice(symbol));
            });
            return data.symbols;
        }
    } catch (error) {
        console.error('Error updating symbol prices:', error);
        return null;
    }
};

export const fetchAllSymbols = () => async (dispatch) => {
    try {
        const response = await fetch('/api/symbols');
        
        if (!response.ok) {
            const errorData = await response.json();
            dispatch({
                type: FETCH_ALL_SYMBOLS_ERROR,
                payload: errorData.error || 'Failed to fetch symbols'
            });
            return false;
        }
        
        const data = await response.json();
        
        // // Convert array to object indexed by symbol
        // const symbolsObject = {};
        // data.symbols.forEach(symbol => {
        //     symbolsObject[symbol.symbol] = symbol;
        // });
        
        dispatch({
            type: SET_ALL_SYMBOLS,
            payload: data.symbols
            // payload: symbolsObject
        });
        
        return true;
    } catch (error) {
        console.error('Error fetching symbols:', error);
        dispatch({
            type: FETCH_ALL_SYMBOLS_ERROR,
            payload: error.message
        });
        return false;
    }
};

// Initial State
const initialState = {
    symbol: null,
    symbolPrices: [],
    symbolError: null,
    isLoading: false,
    allSymbols: [],
    allSymbolsError: null
};

// Reducer
const symbolsReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOAD_SYMBOLS:
            return { ...state, symbols: action.symbols };
        case LOAD_SYMBOL:
            return {
                ...state,
                symbol: action.payload,
                isLoading: false,
                symbolError: null
            };
        case UPDATE_SYMBOL_PRICE:
            return {
                ...state,
                allSymbols: {
                    ...state.allSymbols,
                    [action.payload.symbol]: {
                        ...state.allSymbols[action.payload.symbol],
                        ...action.payload
                    }
                }
            };
        case SET_ALL_SYMBOLS:
            return {
                ...state,
                allSymbols: action.payload,
                allSymbolsError: null
            };
        case FETCH_ALL_SYMBOLS_ERROR:
            return {
                ...state,
                allSymbolsError: action.payload
            };
        default:
            return state;
    }
};

export default symbolsReducer; 