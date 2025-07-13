import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';

interface User {
    id: string;
    email: string;
    full_name: string;
    is_active: boolean;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    const isAuthenticated = !!user && authService.isAuthenticated();

    useEffect(() => {
        // Check if user is already logged in on app startup
        const checkAuth = async () => {
            const token = authService.getToken();
            if (token && authService.isAuthenticated()) {
                try {
                    const userData = await authService.getCurrentUser(token);
                    setUser(userData);
                } catch (error) {
                    // Token is invalid, remove it
                    authService.removeToken();
                }
            }
            setLoading(false);
        };

        checkAuth();
    }, []);

    const login = async (email: string, password: string) => {
        try {
            const loginResponse = await authService.login(email, password);
            authService.setToken(loginResponse.access_token);
            
            const userData = await authService.getCurrentUser(loginResponse.access_token);
            setUser(userData);
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        authService.removeToken();
        setUser(null);
    };

    const value: AuthContextType = {
        user,
        isAuthenticated,
        loading,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
