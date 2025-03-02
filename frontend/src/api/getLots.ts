import { apiRoutes } from 'config/apiRoutes';

export interface Lot {
  price: number;
  current_volume: number;
  status: string;
  id: number;
  depot: string;
  fuel: string;
  region: string;
}

export interface LotsResponse {
  page_count: number;
  lots: Lot[];
}

interface FetchLotsParams {
  page: number;
  offset: number;
  fuel?: string;
  depot?: string;
  region?: string;
}

export async function fetchLotsFromApi({ page, offset, fuel, depot, region }: FetchLotsParams): Promise<LotsResponse> {
  const accessToken = localStorage.getItem('access_token');
  // Создаем объект URL с добавленными query параметрами
  const url = new URL(apiRoutes.products);
  url.searchParams.append('page', page.toString());
  url.searchParams.append('offset', offset.toString());

  if (fuel) url.searchParams.append('fuel', fuel);
  if (depot) url.searchParams.append('depot', depot);
  if (region) url.searchParams.append('region', region);

  // Выполняем запрос
  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  });
  if (!response.ok) {
    throw new Error('Ошибка при получении данных');
  }
  const data = await response.json();
  return data;
}
