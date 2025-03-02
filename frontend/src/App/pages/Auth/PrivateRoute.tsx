import { observer } from 'mobx-react-lite';
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import AuthStore from 'stores/AuthStore';

const PrivateRoute = observer(() => {
  if (!AuthStore.isAuth) {
    return <Navigate to="/login" />;
  }
  return <Outlet />;
});

export default PrivateRoute;
