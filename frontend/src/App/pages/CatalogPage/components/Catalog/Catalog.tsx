import { observer } from 'mobx-react-lite';
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import Card from 'components/Card';
import Loader from 'components/Loader';
import Text from 'components/Text';
import { routerUrls } from 'config/routerUrls';
import CatalogStore from '../../stores/CatalogStore';
import styles from './Catalog.module.scss';

const Catalog = observer(() => {
  const { lots, isLoading, page, pageCount } = CatalogStore;

  // Первоначальная загрузка данных
  useEffect(() => {
    CatalogStore.fetchLots();
  }, []);

  // Эффект для бесконечного скролла
  useEffect(() => {
    const handleScroll = () => {
      // Если прокрутили почти до конца (с запасом 500px),
      // нет активной загрузки и есть еще страницы для загрузки – загружаем следующую страницу
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 && !isLoading && page < pageCount) {
        CatalogStore.setPage(page + 1);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isLoading, page, pageCount]);

  // Если нет товаров и не идет загрузка, выводим сообщение
  if (lots.length === 0 && !isLoading) {
    return <p>Товары не найдены по заданным фильтрам.</p>;
  }

  return (
    <div>
      <div className={styles.catalog}>
        {lots.map((lot) => (
          <div key={lot.id}>
            <Link to={routerUrls.lotDetail.create(lot.id)}>
              <Card
                typeFuel={lot.fuel}
                nameBase={lot.depot}
                nameRegion={lot.region}
                curentValue={lot.current_volume}
                contentSlot={`${lot.price} ₽`}
                actionSlot="Подробнее"
              />
            </Link>
          </div>
        ))}
      </div>
      {/* Если идет загрузка, показываем Loader внизу */}
      {isLoading && <Loader />}
    </div>
  );
});

export default Catalog;
