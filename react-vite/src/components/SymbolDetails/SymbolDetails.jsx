import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchSymbol, fetchSymbolPrices } from '../../redux/symbols';
import { Line } from 'react-chartjs-2';
import OpenModalButton from '../OpenModalButton';
import PlaceOrderModal from '../Modals/PlaceOrderModal';
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
import { csrfFetch } from '../../redux/csrf';

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
            const response = await csrfFetch('/api/watchlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbol: symbol.toUpperCase() })
            });

            if (response.ok) {
                setIsInWatchlist(true);
                // Show success message
                alert(`${symbol.toUpperCase()} added to watchlist successfully!`);
            } else {
                const data = await response.json();
                console.error('Error adding to watchlist:', data.errors || 'Unknown error');
                alert(`Failed to add to watchlist: ${data.errors ? data.errors.join(', ') : 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error adding to watchlist:', error);
            alert('Failed to add to watchlist. Please try again.');
        }
    };

    return (
        <div className="symbol-details">
            <div className="symbol-header">
                <div className="symbol-info-details">
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
                    <OpenModalButton
                        buttonText="Place Order"
                        className="order-button"
                        modalComponent={
                            <PlaceOrderModal
                                symbol={symbol}
                                currentPrice={symbolData.current_price}
                                initialOrderType="buy"
                            />
                        }
                    />
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
        </div>
    );
};

export default SymbolDetails; 