interface LoginResponse {
    access_token: string;
    token_type: string;
}

interface User {
    id: string;
    email: string;
    full_name: string;
    is_active: boolean;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const authService = {
    async login(email: string, password: string): Promise<LoginResponse> {
        const formData = new FormData();
        formData.append('username', email); // FastAPI OAuth2PasswordRequestForm expects 'username'
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
            throw new Error(errorData.detail || 'Login failed');
        }

        return response.json();
    },

    async getCurrentUser(token: string): Promise<User> {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to get user information');
        }

        return response.json();
    },

    setToken(token: string): void {
        localStorage.setItem('access_token', token);
    },

    getToken(): string | null {
        return localStorage.getItem('access_token');
    },

    removeToken(): void {
        localStorage.removeItem('access_token');
    },

    isAuthenticated(): boolean {
        const token = this.getToken();
        if (!token) return false;

        try {
            // Simple token expiration check
            const payload = JSON.parse(atob(token.split('.')[1]));
            const currentTime = Date.now() / 1000;
            return payload.exp > currentTime;
        } catch {
            return false;
        }
    }
};
