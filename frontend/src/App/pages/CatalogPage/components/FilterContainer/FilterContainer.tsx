import React, { useState, useCallback, useEffect } from 'react';
import Button from 'components/Button';
import FuelTypesFilter from '../FuelTypesFilter';
import RegionsFilter from '../RegionsFilter';

const FilterContainer: React.FC = () => {
  const [selectedRegion, setSelectedRegion] = useState<string>('');
  const [selectedFuel, setSelectedFuel] = useState<string>('');

  // Функция, которая извлекает параметры из URL
  const getQueryParams = () => {
    const queryParams = new URLSearchParams(window.location.search);
    return {
      region: queryParams.get('region') || '',
      fuel: queryParams.get('fuel') || '',
    };
  };

  useEffect(() => {
    const { region, fuel } = getQueryParams();
    setSelectedRegion(region);
    setSelectedFuel(fuel);
  }, []);

  const handleRegionSelect = useCallback((region: string) => {
    setSelectedRegion(region);
  }, []);

  const handleFuelSelect = useCallback((fuel: string) => {
    setSelectedFuel(fuel);
  }, []);

  const handleApplyFilters = () => {
    const path = window.location.pathname;
    const searchParams = new URLSearchParams(window.location.search);

    if (selectedRegion) {
      searchParams.set('region', selectedRegion);
    } else {
      searchParams.delete('region');
    }

    if (selectedFuel) {
      searchParams.set('fuel', selectedFuel);
    } else {
      searchParams.delete('fuel');
    }

    const newUrl = `${path}?${searchParams.toString()}`;
    window.history.pushState({}, '', newUrl);
    window.location.reload();
  };

  return (
    <div className="d-flex w-100 justify-content-between align-items-end gap-3">
      <RegionsFilter onRegionSelect={handleRegionSelect} selectedRegion={selectedRegion} />
      <FuelTypesFilter onFuelSelect={handleFuelSelect} />
      <Button onClick={handleApplyFilters}>Применить</Button>
    </div>
  );
};

export default FilterContainer;
