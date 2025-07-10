import React, { useState, useEffect } from 'react';

const DeviceList = () => {
    const [devices, setDevices] = useState([]);

    useEffect(() => {
        fetch('/api/v1/devices/')
            .then(response => response.json())
            .then(data => setDevices(data));
    }, []);

    return (
        <div>
            <h2>Devices</h2>
            <ul>
                {devices.map((device, index) => (
                    <li key={index}>{device.device_name}</li>
                ))}
            </ul>
        </div>
    );
};

export default DeviceList;
