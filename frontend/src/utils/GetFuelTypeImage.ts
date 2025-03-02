import banner_92 from '../assets/92.png';
import banner_92_ecto from '../assets/92_экто.png';
import banner_95 from '../assets/95.png';
import banner_95_ecto from '../assets/95_экто.png';
import banner_dt from '../assets/дт.png';

export function GetFuelTypeImage(str: string): string {
  const fuelImages: Record<string, string> = {
    'АИ-92': banner_92,
    'АИ-95': banner_95,
    'АИ-92 Экто': banner_92_ecto,
    'АИ-95 Экто': banner_95_ecto,
    ДТ: banner_dt,
  };

  return fuelImages[str] || 'https://my.mhaus.org/global_graphics/default-store-350x350.jpg';
}
