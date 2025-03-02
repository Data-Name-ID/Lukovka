import classNames from 'classnames';
import React from 'react';
import { Link, useMatch } from 'react-router-dom';
import { routerUrls } from 'config/routerUrls';
import styles from './Nav.module.scss';

const Navigation = () => {
  return (
    <nav>
      <ul className={styles.navigation}>
        <li
          className={classNames(styles.navigation__item, {
            [styles.active]: useMatch(routerUrls.lots.mask),
          })}
        >
          <Link to={routerUrls.lots.mask}>Лоты</Link>
        </li>
      </ul>
    </nav>
  );
};
export default Navigation;
