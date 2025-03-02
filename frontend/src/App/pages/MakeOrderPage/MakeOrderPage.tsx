import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Button from 'components/Button';
import Loader from 'components/Loader';
import Text from 'components/Text';
import { apiRoutes } from 'config/apiRoutes';
import DetailStore from '../DetailPage/stores/DetailStore';

const MakeOrderPage = () => {
  const { id } = useParams<{ id: string }>();
  const [orderAmount, setOrderAmount] = useState<number>(0);
  const [deliveryType, setDeliveryType] = useState<string>('Доставка');
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (id) {
      DetailStore.fetchLotDetail(Number(id));
    }
  }, [id]);

  if (DetailStore.isLoading) {
    return (
      <div className="container">
        <Loader />
      </div>
    );
  }

  if (!DetailStore.lot) {
    return (
      <div className="container">
        <Text view="title">Ошибка: данные не найдены</Text>
      </div>
    );
  }

  const { depot, fuel, region, price, current_volume, id: lotId } = DetailStore.lot;

  const handleOrder = async () => {
    if (orderAmount <= 0 || orderAmount > current_volume) {
      setMessage('❌ Укажите корректное количество тонн.');
      return;
    }

    setLoading(true);
    setMessage(null);

    const accessToken = localStorage.getItem('access_token') || '';
    const orderData = {
      volume: orderAmount,
      delivery_type: deliveryType,
      lot_id: lotId,
    };

    console.log('Отправляем данные:', orderData);

    try {
      const response = await fetch(apiRoutes.orders, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(orderData),
      });

      const result = await response.json();
      console.log('Ответ сервера:', result);

      if (response.ok) {
        setMessage('✅ Заказ успешно оформлен!');
      } else {
        setMessage(`❌ Ошибка: ${result.detail || 'Неизвестная ошибка'}`);
      }
    } catch (error) {
      console.error('Ошибка при отправке запроса:', error);
      setMessage('❌ Ошибка при оформлении заказа.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="pt-4">Формирование заказа</h1>
      <table className="table">
        <tbody>
          <tr>
            <td>Номер лота</td>
            <td>{lotId}</td>
          </tr>
          <tr>
            <td>Вид топлива</td>
            <td>{fuel}</td>
          </tr>
          <tr>
            <td>Название нефтебазы</td>
            <td>{depot}</td>
          </tr>
          <tr>
            <td>Регион нефтебазы</td>
            <td>{region}</td>
          </tr>
          <tr>
            <td>Остаток топлива на нефтебазе</td>
            <td>{current_volume} тонн</td>
          </tr>
          <tr>
            <td>Цена за 1 тонну</td>
            <td>{price} ₽</td>
          </tr>
          <tr>
            <td>Количество тонн для заказа</td>
            <td>
              <input
                className="form-control"
                type="number"
                value={orderAmount}
                onChange={(e) => setOrderAmount(Number(e.target.value))}
                placeholder="Введите количество тонн"
              />
            </td>
          </tr>
          <tr>
            <td>Способ доставки</td>
            <td>
              <select className="form-control" value={deliveryType} onChange={(e) => setDeliveryType(e.target.value)}>
                <option value="Доставка">Доставка</option>
                <option value="Самовывоз">Самовывоз</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
      {message && <p>{message}</p>}
      <Button onClick={handleOrder} disabled={loading}>
        {loading ? 'Оформление...' : 'Оформить заказ'}
      </Button>
    </div>
  );
};

export default MakeOrderPage;
