import React from 'react';
import { Routes, Route, Link, Navigate } from 'react-router-dom';
import RootLayout from 'components/RootLayout';
import { routerUrls } from 'config/routerUrls';
import LoginPage from './pages/Auth/LoginPage';
import PrivateRoute from './pages/Auth/PrivateRoute';
import ProfilePage from './pages/Auth/ProfilePage';
import RegisterPage from './pages/Auth/RegisterPage';
import CatalogPage from './pages/CatalogPage';
import DetailPage from './pages/DetailPage';
import LoadLot from './pages/LoadLot';
import MakeOrderPage from './pages/MakeOrderPage';
import OrdersPage from './pages/OrdersPage';

function App() {
  return (
    <div>
      <RootLayout>
        <Routes>
          <Route path="/" element={<Navigate to="/lots" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route element={<PrivateRoute />}>
            <Route path={routerUrls.lots.mask} element={<CatalogPage />} />
            <Route path={routerUrls.lotDetail.mask} element={<DetailPage />} />
            <Route path="/orders" element={<OrdersPage />} />
            <Route path="/make_order/:id" element={<MakeOrderPage />} />
            <Route path="/load_lot" element={<LoadLot />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>

          <Route path="*" element={<div>Not Found</div>} />
        </Routes>
      </RootLayout>
    </div>
  );
}

export default App;
