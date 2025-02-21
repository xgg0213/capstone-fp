import { useState, useEffect } from 'react';
import { stockWebSocket } from '../services/websocket';

export default function TestConnection() {
    const [status, setStatus] = useState({
        jwt: 'Checking...',
        alpaca: 'Checking...',
        websocket: 'Checking...'
    });

    useEffect(() => {
        // Test JWT
        fetch('/api/auth/test-token', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(res => res.ok ? 
            setStatus(s => ({...s, jwt: '✅ JWT Working'})) : 
            setStatus(s => ({...s, jwt: '❌ JWT Failed'}))
        );

        // Test Alpaca
        fetch('/api/stocks/prices?symbols=AAPL')
        .then(res => res.json())
        .then(data => {
            if (data.AAPL) {
                setStatus(s => ({...s, alpaca: '✅ Alpaca Connected'}));
            } else {
                setStatus(s => ({...s, alpaca: '❌ Alpaca Failed'}));
            }
        });

        // Test WebSocket
        const handleUpdate = (data) => {
            setStatus(s => ({...s, websocket: '✅ WebSocket Receiving Data'}));
        };

        stockWebSocket.subscribe('AAPL', handleUpdate);

        return () => {
            stockWebSocket.unsubscribe('AAPL', handleUpdate);
        };
    }, []);

    return (
        <div className="test-connection">
            <h2>Connection Status</h2>
            <div>JWT Status: {status.jwt}</div>
            <div>Alpaca Status: {status.alpaca}</div>
            <div>WebSocket Status: {status.websocket}</div>
        </div>
    );
} 