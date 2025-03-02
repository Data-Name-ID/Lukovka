import { observer } from 'mobx-react-lite';
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'components/Button';
import Input from 'components/Input';
import styles from './Search.module.scss';

const Search = observer(() => {
  // Инициализация состояния `depot` из строки запроса (если параметр есть)
  const [depot, setDepot] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Извлекаем параметр `depot` из строки запроса, если он есть
    const searchParams = new URLSearchParams(window.location.search);
    const depotValue = searchParams.get('depot') || '';
    setDepot(depotValue); // Устанавливаем его в состояние
  }, []);

  // Функция для обработки изменения в поле ввода
  const handleSearchChange = useCallback((value: string) => {
    setDepot(value); // Обновляем состояние depot
  }, []);

  // Функция для обработки поиска
  // Функция для обработки поиска
  const handleSearch = () => {
    const path = window.location.pathname;
    // Создаем новый URLSearchParams без предыдущих параметров
    const searchParams = new URLSearchParams();

    // Добавляем или обновляем параметр "depot"
    if (depot) {
      searchParams.set('depot', depot);
    }

    // Формируем новый URL с обновленными параметрами
    const newUrl = `${path}?${searchParams.toString()}`;
    window.history.pushState({}, '', newUrl); // Обновляем URL в адресной строке
    window.location.reload(); // Перезагружаем страницу
  };

  return (
    <div className={styles.search}>
      <div className={styles.search__input}>
        <Input
          value={depot} // Значение из состояния
          onChange={handleSearchChange} // Обработчик изменения
          placeholder="Название товара" // Текст подсказки
        />
      </div>
      <Button onClick={handleSearch}>Найти</Button> {/* Обработка нажатия на кнопку */}
    </div>
  );
});

export default Search;
