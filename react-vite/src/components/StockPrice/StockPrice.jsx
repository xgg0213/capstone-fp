import { useState, useEffect } from 'react';
import { stockWebSocket } from '../../services/websocket';

export default function StockPrice({ symbol }) {
    const [priceData, setPriceData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Get initial price
        fetch(`/api/stocks/prices?symbols=${symbol}`)
            .then(res => res.json())
            .then(data => {
                if (data[symbol]) {
                    setPriceData(data[symbol]);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching price:', err);
                setLoading(false);
            });

        // Subscribe to real-time updates
        const handleUpdate = (data) => {
            setPriceData(data);
        };

        stockWebSocket.subscribe(symbol, handleUpdate);

        // Cleanup subscription
        return () => {
            stockWebSocket.unsubscribe(symbol, handleUpdate);
        };
    }, [symbol]);

    if (loading) return <div>Loading...</div>;
    if (!priceData) return <div>No data available</div>;

    const { price, change, change_percent } = priceData;
    const isPositive = change >= 0;

    return (
        <div className="stock-price">
            <div className="symbol">{symbol}</div>
            <div className="price">${price.toFixed(2)}</div>
            <div className={`change ${isPositive ? 'positive' : 'negative'}`}>
                {isPositive ? '+' : ''}{change.toFixed(2)} 
                ({change_percent.toFixed(2)}%)
            </div>
            {priceData.bid && (
                <div className="bid-ask">
                    <div>Bid: ${priceData.bid.toFixed(2)} × {priceData.bid_size}</div>
                    <div>Ask: ${priceData.ask.toFixed(2)} × {priceData.ask_size}</div>
                </div>
            )}
        </div>
    );
} 