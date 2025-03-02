import React from 'react';
import Text from 'components/Text';
import styles from './Title.module.scss';

const Title = () => {
  return (
    <div className={styles.title}>
      <Text view="title" weight="bold">
        Луковка
      </Text>
      <Text className={styles.sub} view="p-20" color="secondary" maxLines={2}>
        Остатки топлива — ваша выгода с Лукойл!
      </Text>
    </div>
  );
};

export default Title;
