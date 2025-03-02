import classNames from 'classnames';
import { observer } from 'mobx-react-lite';
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Button from 'components/Button';
import Text from 'components/Text';
import { routerUrls } from 'config/routerUrls';
import styles from './ItemInfo.module.scss';

export type ItemInfoProps = {
  number: string;
  price: number;
  id: number;
  nameBase: React.ReactNode;
  nameRegion: React.ReactNode;
  curentValue: React.ReactNode;
};

const ItemInfo: React.FC<ItemInfoProps> = observer(({ number, price, id, nameBase, nameRegion, curentValue }) => {
  const [isInCart, setIsInCart] = useState(false);

  const handleAddToCart = () => {
    setIsInCart(true);
  };

  return (
    <div>
      <Text view="title" weight="bold">
        {number}
      </Text>
      <Text className={styles.item__description} view="p-20" color="secondary">
        {nameBase}
      </Text>
      <Text className={styles.item__description} view="p-20" color="secondary">
        {nameRegion}
      </Text>
      <Text className={styles.item__description} view="p-20" color="secondary">
        {curentValue}
      </Text>
      <Text className={styles.item__price} view="title" weight="bold">
        {price + ' ₽'}
      </Text>
      <div className={styles.buttons}>
        <Link to={`/make_order/${id}`}>
          <Button>Купить сейчас</Button>
        </Link>
      </div>
    </div>
  );
});

export default ItemInfo;
