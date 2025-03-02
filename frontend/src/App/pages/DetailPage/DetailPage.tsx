import { observer } from 'mobx-react-lite';
import React, { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Loader from 'components/Loader';
import Text from 'components/Text';
import { GetFuelTypeImage } from 'utils/GetFuelTypeImage';
import ItemInfo from './components/ItemInfo';
import DetailStore from './stores/DetailStore';
import styles from './DetailPage.module.scss';

const DetailPage = observer(() => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();

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

  return (
    <div>
      <div className="container">
        <button className={styles.nav_detail} onClick={() => navigate(-1)}>
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M20.1201 26.56L11.4268 17.8667C10.4001 16.84 10.4001 15.16 11.4268 14.1333L20.1201 5.44"
              stroke="black"
              strokeWidth="1.5"
              strokeMiterlimit="10"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <Text className={styles.nav_detail__text} view="p-20">
            Назад
          </Text>
        </button>
        <div className={styles.item}>
          <div className={styles.item__images}>
            <img src={GetFuelTypeImage(fuel)} alt={fuel} />
          </div>
          <ItemInfo
            number={`Номер лота: ${lotId}`}
            price={price}
            id={lotId}
            nameBase={`Название нефтебазы: ${depot}`}
            nameRegion={`Регион: ${region}`}
            curentValue={`Остаток топлива: ${current_volume}`}
          />
        </div>
      </div>
    </div>
  );
});

export default DetailPage;
