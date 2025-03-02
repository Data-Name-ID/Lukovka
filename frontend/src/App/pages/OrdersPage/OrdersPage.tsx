import React, { useEffect, useState } from 'react';
import Loader from 'components/Loader';
import { apiRoutes } from 'config/apiRoutes';

interface Order {
  id: number;
  status: string;
  created_datetime: string;
  updated_datetime: string;
  volume: number;
  delivery_type: string;
  depot: string;
  fuel: string;
  region: string;
}

const OrdersPage = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrders = async () => {
      setIsLoading(true);
      setError(null);

      const accessToken = localStorage.getItem('access_token') || '';

      try {
        const response = await fetch(apiRoutes.orders, {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Ошибка при загрузке заказов');
        }

        const data = await response.json();
        setOrders(data.orders);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Неизвестная ошибка');
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div className="container">
      <h1>Заказы</h1>

      {isLoading && <Loader />}
      {error && <p className="text-danger">{error}</p>}

      {!isLoading && !error && orders.length === 0 && <p>У вас нет заказов.</p>}

      {!isLoading && !error && orders.length > 0 && (
        <table className="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Топливо</th>
              <th>Нефтебаза</th>
              <th>Регион</th>
              <th>Объём</th>
              <th>Доставка</th>
              <th>Дата создания</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order, index) => (
              <tr key={order.id}>
                <th>{index + 1}</th>
                <td>{order.fuel}</td>
                <td>{order.depot}</td>
                <td>{order.region}</td>
                <td>{order.volume} тонн</td>
                <td>{order.delivery_type}</td>
                <td>{new Date(order.created_datetime).toLocaleString()}</td>
                <td
                  className={
                    order.status === 'Отмена' ? 'text-danger' : order.status === 'Доставлен' ? 'text-success' : ''
                  }
                >
                  {order.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default OrdersPage;
