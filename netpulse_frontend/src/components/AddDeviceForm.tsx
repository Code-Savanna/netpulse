import React, { useState } from 'react';
import { authService } from '../services/authService';

interface AddDeviceFormProps {
    onDeviceAdded: (device: NewDevice) => void;
}

interface DeviceFormData {
    name: string;
    ip_address: string;
    device_type: string;
    location: string;
}

interface NewDevice {
    id: string;
    name: string;
    ip_address: string;
    device_type: string;
    location: string;
    status: string;
}

interface DeviceType {
    value: string;
    label: string;
    icon: string;
}

const AddDeviceForm: React.FC<AddDeviceFormProps> = ({ onDeviceAdded }) => {
    const [formData, setFormData] = useState<DeviceFormData>({
        name: '',
        ip_address: '',
        device_type: 'router',
        location: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            const token = authService.getToken();
            const response = await fetch('http://localhost:8000/api/v1/devices/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Authentication failed. Please log in again.');
                }
                throw new Error('Failed to add device');
            }

            const newDevice: NewDevice = await response.json();
            onDeviceAdded(newDevice);
            setFormData({
                name: '',
                ip_address: '',
                device_type: 'router',
                location: ''
            });
            setSuccess(true);
            setTimeout(() => setSuccess(false), 3000);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const deviceTypes = [
        { value: 'router', label: 'Router', icon: '🌐' },
        { value: 'switch', label: 'Switch', icon: '🔌' },
        { value: 'server', label: 'Server', icon: '💻' },
        { value: 'firewall', label: 'Firewall', icon: '🛡️' },
        { value: 'access_point', label: 'Access Point', icon: '📡' }
    ];

    return (
        <div className="bg-white shadow-lg rounded-xl border border-gray-200">
            <div className="p-6 border-b border-gray-200 bg-gray-50">
                <h3 className="text-2xl font-bold text-gray-800">Add New Device</h3>
                <p className="text-gray-600 mt-1">Fill out the form to add a new device to the network.</p>
            </div>

            <div className="p-6">
                {/* Success Message */}
                {success && (
                    <div className="mb-4 p-4 bg-green-100 border border-green-200 rounded-lg">
                        <div className="flex items-center">
                            <svg className="w-5 h-5 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span className="text-green-800 font-medium">Device added successfully!</span>
                        </div>
                    </div>
                )}

                {/* Error Message */}
                {error && (
                    <div className="mb-4 p-4 bg-red-100 border border-red-200 rounded-lg">
                        <div className="flex items-center">
                            <svg className="w-5 h-5 text-red-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                            <span className="text-red-800 font-medium">{error}</span>
                        </div>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">Device Name</label>
                        <input
                            type="text"
                            name="name"
                            id="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="e.g., Core Router 1"
                        />
                    </div>

                    <div>
                        <label htmlFor="ip_address" className="block text-sm font-medium text-gray-700 mb-1">IP Address</label>
                        <input
                            type="text"
                            name="ip_address"
                            id="ip_address"
                            value={formData.ip_address}
                            onChange={handleChange}
                            required
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="e.g., 192.168.1.1"
                        />
                    </div>

                    <div>
                        <label htmlFor="device_type" className="block text-sm font-medium text-gray-700 mb-1">Device Type</label>
                        <select
                            name="device_type"
                            id="device_type"
                            value={formData.device_type}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            {deviceTypes.map(type => (
                                <option key={type.value} value={type.value}>{type.label}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                        <input
                            type="text"
                            name="location"
                            id="location"
                            value={formData.location}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="e.g., Data Center A"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex justify-center items-center px-4 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300 transition-all"
                    >
                        {loading ? (
                            <>
                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Adding...
                            </>
                        ) : (
                            'Add Device'
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AddDeviceForm;
