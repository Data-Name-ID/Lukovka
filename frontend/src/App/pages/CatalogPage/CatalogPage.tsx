import React, { useCallback } from 'react';
import Catalog from './components/Catalog';
import FilterContainer from './components/FilterContainer';
import Search from './components/Search';
import Title from './components/Title';

const CatalogPage = () => {
  return (
    <div className="container">
      <Title />
      <Search />
      <FilterContainer />
      <Catalog />
    </div>
  );
};

export default CatalogPage;
