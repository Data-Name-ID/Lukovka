import classNames from 'classnames';
import React, { useCallback, useState } from 'react';
import { Link } from 'react-router-dom';
import Navigation from 'components/Nav';
import Panel from 'components/Panel';
import { routerUrls } from 'config/routerUrls';
import logo from '../../assets/logo.png';
import styles from './Header.module.scss';

const Header = () => {
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleMenu = useCallback(() => {
    setMenuOpen((isMenuOpen) => !isMenuOpen);
  }, [setMenuOpen]);

  return (
    <header className={styles.header}>
      <div className="container">
        <div className={styles.panel}>
          <button className={styles.burger} onClick={toggleMenu} aria-label="Toggle menu">
            <span className={styles.burger__line}></span>
            <span className={styles.burger__line}></span>
            <span className={styles.burger__line}></span>
          </button>
        </div>
        <div className={classNames(styles.menu, { [styles.menu_open]: isMenuOpen })}>
          <div className={styles.header__inner}>
            <Link to={routerUrls.lots.mask}>
              <img className={styles.logo} src={logo} alt="Logo" />
            </Link>
            <Navigation />
            <Panel />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
