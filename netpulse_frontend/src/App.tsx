import React, { useState } from 'react';
import './App.css';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginPage from './pages/LoginPage';
import DeviceList from './components/DeviceList';
import AddDeviceForm from './components/AddDeviceForm';

const Dashboard: React.FC = () => {
  const [refreshKey, setRefreshKey] = useState(0);
  const { user, logout } = useAuth();

  const handleDeviceAdded = () => {
    // Trigger a refresh of the device list
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
        <div className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-2">NetPulse</h1>
              <p className="text-blue-100 text-lg">Network Operations Center Monitoring</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-blue-200">Welcome, {user?.full_name || user?.email}</p>
              <div className="flex items-center justify-end mt-1 space-x-4">
                <div className="flex items-center">
                  <span className="w-3 h-3 bg-green-400 rounded-full mr-2"></span>
                  <span>All systems operational</span>
                </div>
                <button
                  onClick={logout}
                  className="px-3 py-1 text-sm bg-blue-700 hover:bg-blue-800 rounded-lg transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Device List */}
          <div className="lg:col-span-2">
            <DeviceList key={refreshKey} refreshKey={refreshKey} />
          </div>

          {/* Add Device Form */}
          <div>
            <AddDeviceForm onDeviceAdded={handleDeviceAdded} />
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white mt-12 py-6 border-t">
        <div className="container mx-auto text-center text-gray-500">
          <p>&copy; 2025 NetPulse. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

const AppContent: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return isAuthenticated ? <Dashboard /> : <LoginPage />;
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
