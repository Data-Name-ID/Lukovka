import classNames from 'classnames';
import React from 'react';
import styles from '../Icon/Icon.module.scss';

interface PreviosIconProps {
  disabled?: boolean;
}

const PreviosIcon: React.FC<PreviosIconProps> = ({ disabled = false }) => {
  return (
    <svg
      width="38"
      height="42"
      viewBox="0 0 38 42"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={classNames(disabled && styles.icon__disabled, styles.icon)}
    >
      <path
        d="M23.12 31.5599L14.4267 22.8666C13.4 21.8399 13.4 20.1599 14.4267 19.1333L23.12 10.4399"
        stroke="#151411"
        strokeWidth="1.5"
        strokeMiterlimit="10"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export default PreviosIcon;
