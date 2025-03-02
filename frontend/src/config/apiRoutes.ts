const API_BASE = 'http://localhost:8000/api';
const createApiRoute = (route: string) => `${API_BASE}${route}`;

export const apiRoutes = {
  products: createApiRoute('/lots'),
  productById: (id: string | undefined) => createApiRoute(`/lots/${id}`),
  fuelsTypes: createApiRoute('/fuels/types'),
  regions: createApiRoute('/depots/regions'),
  LoadLod: createApiRoute('/lots/upload'),
  login: createApiRoute('/auth/signin'),
  register: createApiRoute('/auth/signup'),
  curentUser: createApiRoute('/auth/current'),
};
