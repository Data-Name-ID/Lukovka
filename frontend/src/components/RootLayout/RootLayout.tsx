import React from 'react';
import Header from 'components/Header';

export type RootLayoutProps = {
  children?: React.ReactNode;
};

const RootLayout: React.FC<RootLayoutProps> = ({ children }) => {
  return (
    <div>
      <Header />
      {children}
    </div>
  );
};

export default RootLayout;
