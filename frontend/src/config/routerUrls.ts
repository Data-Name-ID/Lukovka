export const routerUrls = {
  root: '/',
  lots: {
    mask: '/lots',
    create: () => '/lots',
  },
  lotDetail: {
    mask: '/lots/:id',
    create: (id: number) => `/lots/${id}`,
  },
  login: {
    mask: '/login',
    create: () => `/login`,
  },
  profile: {
    mask: '/profile',
    create: () => `/profile`,
  },
  register: {
    mask: '/register',
    create: () => `/register`,
  },
};
