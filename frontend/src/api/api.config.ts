import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://where-pizza.ru/api',
});

// Перехватчик запросов
instance.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('access_token');
  if (accessToken && config.headers) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

export default instance;
