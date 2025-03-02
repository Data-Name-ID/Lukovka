import { apiRoutes } from 'config/apiRoutes';
import instance from './api.config';

export interface RegisterPayload {
  email: string;
  password: string;
}

export interface RegisterResponse {
  type: string;
  access_token: string;
  refresh_token: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  type: string;
  access_token: string;
  refresh_token: string;
}

export interface CurrentUserResponse {
  id: number;
  email: string;
  is_admin: boolean;
}

export default class AuthService {
  static async register(payload: RegisterPayload): Promise<RegisterResponse> {
    const { data } = await instance.post<RegisterResponse>(apiRoutes.register, payload);
    return data;
  }

  static async login(payload: LoginPayload): Promise<LoginResponse> {
    const { data } = await instance.post<LoginResponse>(apiRoutes.login, payload);
    return data;
  }

  static async getCurrentUser(): Promise<CurrentUserResponse> {
    const { data } = await instance.get<CurrentUserResponse>(apiRoutes.curentUser);
    return data;
  }
}
