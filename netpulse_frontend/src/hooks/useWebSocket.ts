import { useEffect, useRef, useState } from 'react';

interface WebSocketMessage {
    type: string;
    data: any;
}

type MessageHandler = (message: WebSocketMessage) => void;

const useWebSocket = (url: string, onMessage: MessageHandler) => {
    const [isConnected, setIsConnected] = useState(false);
    const socket = useRef<WebSocket | null>(null);

    useEffect(() => {
        const connect = () => {
            socket.current = new WebSocket(url);

            socket.current.onopen = () => {
                console.log('WebSocket connected');
                setIsConnected(true);
            };

            socket.current.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    onMessage(message);
                } catch (error) {
                    console.error('Failed to parse WebSocket message:', error);
                }
            };

            socket.current.onclose = () => {
                console.log('WebSocket disconnected. Attempting to reconnect...');
                setIsConnected(false);
                // Simple exponential backoff reconnect strategy
                setTimeout(connect, 3000);
            };

            socket.current.onerror = (error) => {
                console.error('WebSocket error:', error);
                socket.current?.close();
            };
        };

        connect();

        return () => {
            socket.current?.close();
        };
    }, [url, onMessage]);

    return { isConnected };
};

export default useWebSocket;
