import React from 'react';

import { createRoot } from 'react-dom/client';
import './index.scss';
import { BrowserRouter } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App';
import './config/configureMobX';

createRoot(document.getElementById('root')!).render(
  <BrowserRouter basename="/">
    <App />
  </BrowserRouter>,
);
