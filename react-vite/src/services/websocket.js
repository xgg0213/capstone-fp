class StockWebSocket {
    constructor() {
        this.socket = null;
        this.subscriptions = new Map();
        this.connected = false;
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        this.socket = new WebSocket(`${protocol}//${host}/ws`);

        this.socket.onopen = () => {
            this.connected = true;
            // Resubscribe to all symbols
            this.subscriptions.forEach((handlers, symbol) => {
                this.sendSubscription(symbol);
            });
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'price_update') {
                const handlers = this.subscriptions.get(data.symbol) || [];
                handlers.forEach(handler => handler(data));
            }
        };

        this.socket.onclose = () => {
            this.connected = false;
            // Reconnect after a delay
            setTimeout(() => this.connect(), 5000);
        };
    }

    subscribe(symbol, handler) {
        if (!this.subscriptions.has(symbol)) {
            this.subscriptions.set(symbol, new Set());
            if (this.connected) {
                this.sendSubscription(symbol);
            }
        }
        this.subscriptions.get(symbol).add(handler);
    }

    unsubscribe(symbol, handler) {
        const handlers = this.subscriptions.get(symbol);
        if (handlers) {
            handlers.delete(handler);
            if (handlers.size === 0) {
                this.subscriptions.delete(symbol);
                if (this.connected) {
                    this.socket.send(JSON.stringify({
                        type: 'unsubscribe',
                        symbols: [symbol]
                    }));
                }
            }
        }
    }

    sendSubscription(symbol) {
        this.socket.send(JSON.stringify({
            type: 'subscribe',
            symbols: [symbol]
        }));
    }
}

export const stockWebSocket = new StockWebSocket(); 