// Action Types
const LOAD_SYMBOLS = 'symbols/LOAD_SYMBOLS';
const LOAD_SYMBOL = 'symbols/LOAD_SYMBOL';
const UPDATE_SYMBOL_PRICE = 'symbols/UPDATE_SYMBOL_PRICE';

// Action Creators
const loadSymbols = (symbols) => ({
    type: LOAD_SYMBOLS,
    symbols
});

const loadSymbol = (symbol) => ({
    type: LOAD_SYMBOL,
    symbol
});

const updateSymbolPrice = (symbol) => ({
    type: UPDATE_SYMBOL_PRICE,
    symbol
});

// Thunk Actions
export const fetchSymbols = () => async (dispatch) => {
    const response = await fetch('/api/symbols');
    if (response.ok) {
        const data = await response.json();
        dispatch(loadSymbols(data.symbols));
        return data.symbols;
    }
};

export const fetchSymbol = (symbol) => async (dispatch) => {
    const response = await fetch(`/api/symbols/${symbol}`);
    if (response.ok) {
        const data = await response.json();
        dispatch(loadSymbol(data));
        return data;
    }
};

export const fetchSymbolPrices = (symbol) => async (dispatch) => {
    const response = await fetch(`/api/symbols/${symbol}/prices`);
    if (response.ok) {
        const data = await response.json();
        return data.prices;
    }
};

// Reducer
const initialState = {
    allSymbols: {},
    currentSymbol: null
};

const symbolsReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOAD_SYMBOLS:
            const allSymbols = {};
            action.symbols.forEach(symbol => {
                allSymbols[symbol.symbol] = symbol;
            });
            return {
                ...state,
                allSymbols
            };
        case LOAD_SYMBOL:
            return {
                ...state,
                currentSymbol: action.symbol,
                allSymbols: {
                    ...state.allSymbols,
                    [action.symbol.symbol]: action.symbol
                }
            };
        case UPDATE_SYMBOL_PRICE:
            return {
                ...state,
                allSymbols: {
                    ...state.allSymbols,
                    [action.symbol.symbol]: action.symbol
                }
            };
        default:
            return state;
    }
};

export default symbolsReducer; 