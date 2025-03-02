const API_BASE = 'https://where-pizza.ru/api';
const createApiRoute = (route: string) => `${API_BASE}${route}`;

export const apiRoutes = {
  products: createApiRoute('/lots'),
  productById: (id: string | undefined) => createApiRoute(`/lots/${id}`),
  orders: createApiRoute('/orders'),
  fuelsTypes: createApiRoute('/fuels/types'),
  regions: createApiRoute('/depots/regions'),
  LoadLod: createApiRoute('/lots/upload'),
  login: createApiRoute('/auth/signin'),
  register: createApiRoute('/auth/signup'),
  curentUser: createApiRoute('/auth/current'),
};
