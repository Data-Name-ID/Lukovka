import React, { useEffect, useState, FC } from 'react';
import { apiRoutes } from 'config/apiRoutes';

interface Region {
  id: number;
  region: string;
}

interface RegionsFilterProps {
  onRegionSelect: (region: string) => void;
  selectedRegion: string;
}

const RegionsFilter: FC<RegionsFilterProps> = ({ onRegionSelect, selectedRegion }) => {
  const [regions, setRegions] = useState<Region[]>([]);

  useEffect(() => {
    const fetchRegions = async () => {
      try {
        const accessToken = localStorage.getItem('access_token') || 'your_access_token_here';
        const response = await fetch(apiRoutes.regions, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (!response.ok) {
          throw new Error('Ошибка при получении регионов');
        }
        const data: Region[] = await response.json();
        setRegions(data);
      } catch (error) {
        console.error('Ошибка загрузки регионов:', error);
      }
    };

    fetchRegions();
  }, []);

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    onRegionSelect(value);
  };

  return (
    <div className="mb-3 w-100">
      <label htmlFor="regionSelect" className="form-label">
        Регион
      </label>
      <select id="regionSelect" className="form-select" value={selectedRegion} onChange={handleChange}>
        <option value="">Выберите регион</option>
        {regions.map((region) => (
          <option key={region.id} value={region.region}>
            {region.region}
          </option>
        ))}
      </select>
    </div>
  );
};

export default RegionsFilter;
