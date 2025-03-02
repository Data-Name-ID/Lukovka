import { apiRoutes } from 'config/apiRoutes';

export interface LotDetail {
  price: number;
  current_volume: number;
  status: string;
  id: number;
  depot: string;
  fuel: string;
  region: string;
  date: string;
}

export async function fetchLotDetailFromApi(id: number): Promise<LotDetail> {
  const accessToken = localStorage.getItem('access_token');

  if (!accessToken) {
    throw new Error('Отсутствует access_token');
  }

  const response = await fetch(apiRoutes.productById(String(id)), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Ошибка при получении данных для лота с id ${id}, статус: ${response.status}, сообщение: ${errorText}`,
    );
  }

  return await response.json();
}
