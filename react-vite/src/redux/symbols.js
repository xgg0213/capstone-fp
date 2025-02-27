// Constants
const LOAD_SYMBOLS = 'symbols/LOAD_SYMBOLS';
const LOAD_SYMBOL = 'symbols/LOAD_SYMBOL';
const UPDATE_SYMBOL_PRICE = 'symbols/UPDATE_SYMBOL_PRICE';

// Action Creators
const loadSymbols = (symbols) => ({
    type: LOAD_SYMBOLS,
    payload: symbols
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
export const fetchSymbols = () => async (dispatch) => {
    try {
        const response = await fetch('/api/symbols');
        if (response.ok) {
            const data = await response.json();
            dispatch(loadSymbols(data.symbols));
            return data.symbols;
        }
    } catch (error) {
        console.error('Error fetching symbols:', error);
        return null;
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

// Initial State
const initialState = {
    allSymbols: {},
    currentSymbol: null,
    isLoading: false,
    error: null
};

// Reducer
const symbolsReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOAD_SYMBOLS: {
            const allSymbols = {};
            action.payload.forEach(symbol => {
                allSymbols[symbol.symbol] = symbol;
            });
            return {
                ...state,
                allSymbols,
                isLoading: false,
                error: null
            };
        }
        case LOAD_SYMBOL:
            return {
                ...state,
                currentSymbol: action.payload,
                allSymbols: {
                    ...state.allSymbols,
                    [action.payload.symbol]: action.payload
                },
                isLoading: false,
                error: null
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
        default:
            return state;
    }
};

export default symbolsReducer; 