import classNames from 'classnames';
import { observer } from 'mobx-react-lite';
import React from 'react';
import Button from 'components/Button';
import Text from 'components/Text';
import { GetFuelTypeImage } from 'utils/GetFuelTypeImage';
import styles from './Card.module.scss';

export type CardProps = {
  /** Дополнительный classname */
  className?: string;
  /** URL изображения */
  typeFuel: string;
  /** Заголовок карточки */
  nameBase: React.ReactNode;
  /** Описание карточки */
  nameRegion: React.ReactNode;
  curentValue: React.ReactNode;
  /** Содержимое карточки (футер/боковая часть), может быть пустым */
  contentSlot: React.ReactNode;
  /** Клик на карточку */
  onClick?: React.MouseEventHandler;
  /** Слот для действия */
  actionSlot?: React.ReactNode;
};

const Card: React.FC<CardProps> = observer(
  ({ className = '', typeFuel, nameBase, nameRegion, curentValue, contentSlot, onClick, actionSlot }) => {
    return (
      <div className={classNames(className, styles.card)} onClick={onClick}>
        <img src={GetFuelTypeImage(typeFuel)} alt="Card" className={styles.card__image} />
        <div className={styles.card__content}>
          <Text view="p-20" weight="normal" maxLines={2} className={styles.card__title}>
            Название нефтебазы: {nameBase}
          </Text>
          <Text view="p-16" weight={'normal'} maxLines={3} color="secondary" className={styles.card__subtitle}>
            Регион: {nameRegion}
          </Text>
          <Text view="p-16" weight={'normal'} maxLines={3} color="secondary" className={styles.card__subtitle}>
            В наличии: {curentValue} тонн
          </Text>
          <div className={styles.card__footer}>
            {contentSlot && (
              <Text view="p-18" weight="bold">
                {contentSlot}
              </Text>
            )}
            {actionSlot && <Button>{actionSlot}</Button>}
          </div>
        </div>
      </div>
    );
  },
);

export default Card;
