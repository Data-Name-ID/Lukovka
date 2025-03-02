import classNames from 'classnames';
import React from 'react';
import styles from '../Icon/Icon.module.scss';

interface NextIconProps {
  disabled?: boolean;
}

const NextIcon: React.FC<NextIconProps> = ({ disabled = false }) => {
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
        d="M14.88 31.5599L23.5733 22.8666C24.6 21.8399 24.6 20.1599 23.5733 19.1333L14.88 10.4399"
        stroke="#151411"
        strokeWidth="1.5"
        strokeMiterlimit="10"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

export default NextIcon;
