import React, { useState, useEffect, useCallback } from 'react';
import useWebSocket from '../hooks/useWebSocket';
import { authService } from '../services/authService';

interface Device {
    id: string;
    name: string;
    ip_address: string;
    mac_address: string;
    device_type: string;
    status: 'online' | 'offline' | 'unknown';
    last_seen: string;
}

interface DeviceListProps {
    refreshKey: number;
}

const DeviceList: React.FC<DeviceListProps> = ({ refreshKey }) => {
    const [devices, setDevices] = useState<Device[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');

    const handleWebSocketMessage = useCallback((message: { type: string; data: any }) => {
        if (message.type === 'device_update') {
            const updatedDevices: Device[] = Array.isArray(message.data) ? message.data : [message.data];
            setDevices(prevDevices => {
                const newDevicesMap = new Map(prevDevices.map(d => [d.id, d]));
                updatedDevices.forEach(updatedDevice => {
                    newDevicesMap.set(updatedDevice.id, updatedDevice);
                });
                return Array.from(newDevicesMap.values());
            });
        }
    }, []);

    const { isConnected } = useWebSocket('ws://localhost:8000/ws', handleWebSocketMessage);

    const fetchDevices = useCallback(async () => {
        try {
            const token = authService.getToken();
            const response = await fetch('http://localhost:8000/api/v1/devices/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Authentication failed. Please log in again.');
                }
                throw new Error('Failed to fetch devices');
            }
            const data = await response.json();
            setDevices(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchDevices();
    }, [refreshKey, fetchDevices]);

    const handleDelete = async (deviceId: string) => {
        if (window.confirm('Are you sure you want to delete this device?')) {
            try {
                const token = authService.getToken();
                const response = await fetch(`http://localhost:8000/api/v1/devices/${deviceId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Authentication failed. Please log in again.');
                    }
                    const errorData = await response.json().catch(() => ({ detail: 'Failed to delete device' }));
                    throw new Error(errorData.detail || 'Failed to delete device');
                }
                // Optimistic UI update: remove the device from the list immediately
                setDevices(prevDevices => prevDevices.filter(d => d.id !== deviceId));
            } catch (err) {
                if (err instanceof Error) {
                    alert(`Error: ${err.message}`);
                } else {
                    alert('An unknown error occurred while deleting the device.');
                }
            }
        }
    };

    const getStatusColor = (status: 'online' | 'offline' | 'unknown') => {
        switch (status) {
            case 'online':
                return 'text-green-600 bg-green-100';
            case 'offline':
                return 'text-red-600 bg-red-100';
            default:
                return 'text-gray-600 bg-gray-100';
        }
    };

    const getDeviceIcon = (type: string) => {
        switch (type) {
            case 'router':
                return '🌐';
            case 'switch':
                return '🔌';
            case 'server':
                return '💻';
            case 'firewall':
                return '🛡️';
            case 'access_point':
                return '📡';
            default:
                return '📱';
        }
    };

    const filteredDevices = devices.filter(device =>
        device.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        device.ip_address.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <span className="ml-3 text-gray-600">Loading devices...</span>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <div className="text-red-600 text-lg font-semibold mb-2">Error Loading Devices</div>
                <div className="text-red-500">{error}</div>
                <button
                    onClick={fetchDevices}
                    className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                    Try Again
                </button>
            </div>
        );
    }

    return (
        <div className="bg-white shadow-lg rounded-xl overflow-hidden">
            {/* Header */}
            <div className="p-6 bg-gray-50 border-b border-gray-200">
                <div className="flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800">Network Devices</h2>
                        <p className="text-gray-600 mt-1">A list of all devices in your network.</p>
                    </div>
                    <div className="flex items-center space-x-4">
                        <div className="flex items-center" title={`WebSocket Status: ${isConnected ? 'Connected' : 'Disconnected'}`}>
                            <span className={`w-3 h-3 rounded-full mr-2 transition-colors ${isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></span>
                            <span className="text-sm text-gray-500">{isConnected ? 'Live' : 'Connecting...'}</span>
                        </div>
                        <button
                            onClick={fetchDevices}
                            className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-100 rounded-lg hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all"
                        >
                            Refresh
                        </button>
                    </div>
                </div>
                <div className="mt-4">
                    <input
                        type="text"
                        placeholder="Search by name or IP..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
            </div>

            {/* Table */}
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Device</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP Address</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Seen</th>
                            <th scope="col" className="relative px-6 py-3">
                                <span className="sr-only">Actions</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {filteredDevices.map((device) => (
                            <tr key={device.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <div className="text-2xl mr-4">{getDeviceIcon(device.device_type)}</div>
                                        <div>
                                            <div className="text-sm font-medium text-gray-900">{device.name}</div>
                                            <div className="text-sm text-gray-500 capitalize">{device.device_type.replace('_', ' ')}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm text-gray-900">{device.ip_address}</div>
                                    <div className="text-sm text-gray-500">{device.mac_address}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(device.status)}`}>
                                        {device.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {device.last_seen ? new Date(device.last_seen).toLocaleString() : 'N/A'}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button onClick={() => alert('Edit not implemented yet!')} className="text-blue-600 hover:text-blue-900">Edit</button>
                                    <button onClick={() => handleDelete(device.id)} className="text-red-600 hover:text-red-900 ml-4">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Empty State */}
            {filteredDevices.length === 0 && (
                <div className="text-center py-12">
                    <h3 className="text-lg font-medium text-gray-900">No Devices Found</h3>
                    <p className="mt-1 text-sm text-gray-500">
                        {searchTerm ? 'Try adjusting your search.' : 'Add a new device to get started.'}
                    </p>
                </div>
            )}
        </div>
    );
};

export default DeviceList;
