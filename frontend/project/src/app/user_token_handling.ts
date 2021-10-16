import projectConfig from '../assets/conf.json';

export class UserTokenHandling {
    static isUserTokenSet(): boolean {
        return localStorage.getItem('userToken') !== null;
    }

    static getUserToken(): string | null {
        if (!UserTokenHandling.isUserTokenSet()) {
            UserTokenHandling.setGuestToken();
        }
        else {
            UserTokenHandling.validateToken();
        }
        return localStorage.getItem('userToken');
    }

    static getUserId(): string | null {
        return localStorage.getItem('userId');
    }

    static validateToken(): void {
        const data = { token: localStorage.getItem('userToken') };
        fetch((projectConfig.api_url + 'validate_token'), {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-type': 'application/json' }
        }).then(response => response.json())
            .then(response => {
                if (response.status === 'error_token_expired' && UserTokenHandling.isUserTokenSet()) {
                    UserTokenHandling.logOut();
                }
                else if(response.status === 'error_token_expired') {
                    UserTokenHandling.setGuestToken();
                }
            });
    }
    static setGuestToken(): void {
        const data = { timestamp: Date.now().toString() };
        fetch((projectConfig.api_url + 'generate_guest_token'), {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-type': 'application/json' }
        })
            .then(response => response.json())
            .then(json => {
                localStorage.setItem('userToken', json.token);
                location.reload();
            });
    }

    static setUserToken(value: string): void {
        localStorage.setItem('userToken', value);
    }

    static setUserToId(value: string): void {
        localStorage.setItem('userId', value);
    }

    static isUserLoggedIn(): boolean {
        return localStorage.getItem('userId') !== null;
    }
    static logOut(): void {
        localStorage.removeItem('userId');
        localStorage.removeItem('userToken');
    }
}
