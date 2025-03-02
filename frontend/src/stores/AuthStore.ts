import { makeAutoObservable } from 'mobx';
import AuthService, { RegisterPayload, LoginPayload } from 'api/AuthService';

export interface User {
  id: number;
  email: string;
  is_admin: boolean;
}

class AuthStore {
  user: User | null = null;
  isAuth = false;
  isLoading = false;

  constructor() {
    makeAutoObservable(this);
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuth = true;
    }
  }

  async register(payload: RegisterPayload) {
    this.isLoading = true;
    try {
      // Создаём пользователя
      await AuthService.register(payload);

      // После успешной регистрации сразу логиним
      await this.login({ email: payload.email, password: payload.password });
    } catch (err) {
      console.error('Registration error:', err);
    } finally {
      this.isLoading = false;
    }
  }

  async login(payload: LoginPayload) {
    this.isLoading = true;
    try {
      const { access_token } = await AuthService.login(payload);

      // Сохраняем токены
      localStorage.setItem('access_token', access_token);
      this.isAuth = true;
    } catch (err) {
      console.error('Login error:', err);
    } finally {
      this.isLoading = false;
    }
  }

  logout() {
    localStorage.removeItem('access_token');
    this.isAuth = false;
  }

  async getCurrentUser() {
    this.isLoading = true;
    try {
      const data = await AuthService.getCurrentUser();
      this.user = {
        id: data.id,
        email: data.email,
        is_admin: data.is_admin,
      };
    } catch (err) {
      console.error('Get user error:', err);
    } finally {
      this.isLoading = false;
    }
  }
}

export default new AuthStore();
