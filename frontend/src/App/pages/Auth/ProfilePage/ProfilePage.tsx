import { observer } from 'mobx-react-lite';
import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthStore from 'stores/AuthStore';

const ProfilePage = observer(() => {
  useEffect(() => {
    AuthStore.getCurrentUser();
  }, []);

  const handleLogout = () => {
    AuthStore.logout();
  };

  return (
    <div>
      <div className="container mt-3">
        <div className="card flex-md-row mb-4 box-shadow h-md-250">
          <div className="card-body d-flex flex-column align-items-start">
            <div className="p-1">
              <h3>Иванов Иван Иванович</h3>
              <p className="card-text text-muted">Информация о профиле:</p>
            </div>
            <table className="table">
              <tbody>
                <tr>
                  <td>Дата регистрации</td>
                  <td>10.10.2015</td>
                </tr>
                <tr>
                  <td>Статус профиля</td>
                  <td>Активен</td>
                </tr>
                <tr>
                  <td>Email</td>
                  <td>{AuthStore.user?.email}</td>
                </tr>
                <tr>
                  <td>Адрес</td>
                  <td>Москва</td>
                </tr>
              </tbody>
            </table>
            <div className="d-flex gap-2">
              <Link to="/orders">
                <button className="btn btn-primary">Мои заказы</button>
              </Link>
              <button className="btn btn-outline-success" type="button" onClick={handleLogout}>
                Выход
              </button>
              {AuthStore.user?.is_admin && (
                <Link to="/load_lot">
                  <button className="btn btn-primary">Загрузить лот</button>
                </Link>
              )}
            </div>
          </div>
          <img
            className="card-img-right flex-auto d-none d-md-block"
            src="https://placehold.co/200x250"
            alt="Profile"
            style={{ width: '200px', height: '250px' }}
          />
        </div>
      </div>
    </div>
  );
});

export default ProfilePage;
