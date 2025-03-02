import React, { useEffect, useState, FC } from 'react';
import { apiRoutes } from 'config/apiRoutes';
import AuthStore from 'stores/AuthStore';

interface FuelType {
  id: number;
  name: string;
}

interface FuelTypesFilterProps {
  // Callback для передачи выбранного типа топлива (как строка)
  onFuelSelect: (fuel: string) => void;
}

const FuelTypesFilter: FC<FuelTypesFilterProps> = ({ onFuelSelect }) => {
  const [fuelTypes, setFuelTypes] = useState<FuelType[]>([]);
  const [selectedFuel, setSelectedFuel] = useState<string>('');

  useEffect(() => {
    // Извлекаем параметр fuel из строки запроса
    const queryParams = new URLSearchParams(window.location.search);
    const fuelFromUrl = queryParams.get('fuel');
    if (fuelFromUrl) {
      setSelectedFuel(fuelFromUrl);
      onFuelSelect(fuelFromUrl); // Устанавливаем фильтр при загрузке страницы
    }

    // Запрашиваем типы топлива
    const fetchFuelTypes = async () => {
      try {
        const accessToken = localStorage.getItem('access_token') || 'your_access_token_here';
        const response = await fetch(apiRoutes.fuelsTypes, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        // Если сервер вернул 401, вызываем logout и редиректим на /login
        if (!response.ok) {
          if (response.status === 401) {
            AuthStore.logout();
            window.location.href = '/login';
            return;
          }
          throw new Error('Ошибка при получении типов топлива');
        }

        const data: FuelType[] = await response.json();
        setFuelTypes(data);
      } catch (error) {
        console.error('Ошибка загрузки типов топлива:', error);
      }
    };

    fetchFuelTypes();
  }, [onFuelSelect]);

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    setSelectedFuel(value);
    onFuelSelect(value);
  };

  return (
    <div className="mb-3 w-100">
      <label htmlFor="fuelSelect" className="form-label">
        Тип топлива
      </label>
      <select id="fuelSelect" className="form-select" value={selectedFuel} onChange={handleChange}>
        <option value="">Выберите тип топлива</option>
        {fuelTypes.map((fuel) => (
          <option key={fuel.id} value={fuel.name}>
            {fuel.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FuelTypesFilter;
