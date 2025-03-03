import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchSymbol, fetchSymbolPrices } from '../../redux/symbols';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import './SymbolDetails.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SymbolDetails = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { symbol } = useParams();
    const [priceHistory, setPriceHistory] = useState([]);
    const [showOrderForm, setShowOrderForm] = useState(false);
    const [shares, setShares] = useState('');
    const [errors, setErrors] = useState([]);
    const [isInWatchlist, setIsInWatchlist] = useState(false);
    
    const symbolData = useSelector(state => 
        state.symbols.allSymbols[symbol?.toUpperCase()]
    );
    const user = useSelector(state => state.session.user);

    useEffect(() => {
        if (symbol) {
            dispatch(fetchSymbol(symbol))
                .then(data => {
                    if (!data) {
                        navigate('/dashboard');
                    }
                })
                .catch(() => navigate('/dashboard'));

            dispatch(fetchSymbolPrices(symbol))
                .then(prices => setPriceHistory(prices));

            // Check if symbol is in watchlist
            fetch(`/api/watchlist/${symbol}/check`)
                .then(async response => {
                    if (!response.ok) {
                        const error = await response.text();
                        throw new Error(error);
                    }
                    return response.json();
                })
                .then(data => {
                    setIsInWatchlist(data.isWatched);
                })
                .catch(error => {
                    console.error('Error checking watchlist status:', error);
                    setIsInWatchlist(false);
                });
        }
    }, [dispatch, symbol, navigate]);

    if (!symbolData) return <div>Loading...</div>;

    // Prepare chart data with reversed dates
    const chartData = {
        labels: priceHistory.map(price => new Date(price.date).toLocaleDateString()).reverse(),
        datasets: [
            {
                label: 'Price',
                data: priceHistory.map(price => price.close).reverse(),
                fill: true,
                borderColor: '#00C805',
                backgroundColor: 'rgba(0, 200, 5, 0.1)',
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#00C805',
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        elements: {  
        line: {
            borderWidth: 1  // This makes the line thinner (default is usually 3)
        }
        },
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    size: 12,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 12
                },
                padding: 12,
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        return `$${context.parsed.y.toFixed(2)}`;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    font: {
                        size: 12
                    },
                    maxRotation: 0,
                    color: '#666',
                    maxTicksLimit: 6 // Limit number of x-axis labels
                }
            },
            y: {
                display: false, // Hide y-axis labels
                grid: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    font: {
                        size: 12
                    },
                    color: '#666',
                    callback: value => `$${value}`
                }
            }
        },
        interaction: {
            mode: 'index',
            intersect: false
        },
        hover: {
            mode: 'index',
            intersect: false
        }
    };

    const handleAddToWatchlist = async () => {
        try {
            const response = await fetch('/api/watchlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbol: symbol.toUpperCase() })
            });

            if (response.ok) {
                setIsInWatchlist(true);
            }
        } catch (error) {
            console.error('Error adding to watchlist:', error);
        }
    };

    const handlePlaceOrder = () => {
        setShowOrderForm(true);
    };

    const handleSubmitOrder = async (e) => {
        e.preventDefault();
        setErrors([]);

        const orderData = {
            symbol: symbol.toUpperCase(),
            shares: Number(shares),
            price: symbolData.current_price
        };

        try {
            const response = await fetch('/api/orders', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderData)
            });

            if (response.ok) {
                setShowOrderForm(false);
                setShares('');
                navigate('/portfolio');
            } else {
                const data = await response.json();
                if (data.errors) setErrors(data.errors);
            }
        } catch (error) {
            setErrors(['An error occurred while placing the order.']);
        }
    };

    const orderTotal = shares ? (shares * symbolData?.current_price).toFixed(2) : '0.00';

    return (
        <div className="symbol-details">
            <div className="symbol-header">
                <div className="symbol-info">
                    <h2>{symbolData.company_name} ({symbolData.symbol})</h2>
                    <div className="current-price-details">
                        ${symbolData.current_price}
                        <span className={`price-change-details ${symbolData.price_change_pct >= 0 ? 'positive' : 'negative'}`}>
                            {symbolData.price_change_pct}%
                        </span>
                    </div>
                </div>
                <div className="action-buttons">
                    {!isInWatchlist && (
                        <button 
                            className="watchlist-button"
                            onClick={handleAddToWatchlist}
                        >
                            Add to Watchlist
                        </button>
                    )}
                    <button 
                        className="order-button"
                        onClick={handlePlaceOrder}
                    >
                        Place Order
                    </button>
                </div>
            </div>
            
            {/* <div className="price-stats">
                <div>Daily High: ${symbolData.daily_high}</div>
                <div>Daily Low: ${symbolData.daily_low}</div>
                <div>Volume: {symbolData.daily_volume?.toLocaleString()}</div>
            </div> */}

            <div className="price-chart">
                <Line data={chartData} options={chartOptions} />
            </div>

            {showOrderForm && (
                <div className="order-form-overlay">
                    <div className="order-form">
                        <h3>Place Order for {symbol}</h3>
                        <form onSubmit={handleSubmitOrder}>
                            {errors.length > 0 && (
                                <div className="errors">
                                    {errors.map((error, idx) => (
                                        <div key={idx} className="error">{error}</div>
                                    ))}
                                </div>
                            )}
                            <div className="form-group">
                                <label>Current Price:</label>
                                <div>${symbolData.current_price}</div>
                            </div>
                            <div className="form-group">
                                <label>Available Balance:</label>
                                <div>${user.balance.toFixed(2)}</div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="shares">Number of Shares:</label>
                                <input
                                    type="number"
                                    id="shares"
                                    value={shares}
                                    onChange={(e) => setShares(e.target.value)}
                                    min="1"
                                    step="1"
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Estimated Total:</label>
                                <div>${orderTotal}</div>
                            </div>
                            <div className="form-actions">
                                <button type="button" onClick={() => setShowOrderForm(false)}>
                                    Cancel
                                </button>
                                <button type="submit" className="submit-order">
                                    Confirm Order
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SymbolDetails; 