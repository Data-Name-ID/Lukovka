import classNames from 'classnames';
import { observer } from 'mobx-react-lite';
import React, { useEffect, useState } from 'react';
import Form from 'react-bootstrap/Form';
import { Link, useNavigate } from 'react-router-dom';
import Button from 'components/Button';
import { routerUrls } from 'config/routerUrls';
import AuthStore from 'stores/AuthStore';
import styles from './LoginPage.module.scss';

const LoginPage = observer(() => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (AuthStore.isAuth) {
      navigate('/lots');
    }
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // 1. Базовая проверка на пустые поля
    if (!email.trim() || !password.trim()) {
      setError('Пожалуйста, введите email и пароль');
      return;
    }

    try {
      // 2. Отправляем запрос на логин
      await AuthStore.login({ email, password });

      // 3. Если авторизация прошла успешно, AuthStore.isAuth станет true
      if (AuthStore.isAuth) {
        navigate('/lots');
      } else {
        // На случай, если AuthStore не установил isAuth = true
        setError('Неверный email или пароль');
      }
    } catch (err) {
      // 4. Если произошла ошибка (сервер вернул 400/401), показываем сообщение
      console.error('Login error:', err);
      setError('Неверный email или пароль');
    }
  };

  return (
    <div className={classNames('container', styles.block)}>
      <div className={styles.login_form}>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control
              type="email"
              placeholder="Введите email"
              value={email}
              onChange={(e) => {
                setError('');
                setEmail(e.target.value);
              }}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Пароль</Form.Label>
            <Form.Control
              type="password"
              placeholder="Введите пароль"
              value={password}
              onChange={(e) => {
                setError('');
                setPassword(e.target.value);
              }}
            />
          </Form.Group>

          {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}

          <Button type="submit">{AuthStore.isLoading ? 'Loading...' : 'Submit'}</Button>
          <Link to={routerUrls.register.mask}>
            <p className={styles.login__register}>Зарегистрироваться</p>
          </Link>
        </Form>
      </div>
    </div>
  );
});

export default LoginPage;
