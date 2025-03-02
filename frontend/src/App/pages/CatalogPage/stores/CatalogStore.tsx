import { makeAutoObservable } from 'mobx';
import { Lot, LotsResponse, fetchLotsFromApi } from 'api/getLots';

// Для извлечения параметров из строки запроса
function getQueryParams() {
  const urlParams = new URLSearchParams(window.location.search);
  return {
    page: parseInt(urlParams.get('page') || '1', 10),
    offset: parseInt(urlParams.get('offset') || '9', 10),
    fuel: urlParams.get('fuel') || '',
    depot: urlParams.get('depot') || '',
    region: urlParams.get('region') || '',
  };
}

class CatalogStore {
  lots: Lot[] = [];
  pageCount: number = 0;
  isLoading: boolean = false;
  page: number = 1;
  offset: number = 9;
  fuel: string = '';
  depot: string = '';
  region: string = '';

  constructor() {
    makeAutoObservable(this);
    const queryParams = getQueryParams();
    this.page = queryParams.page;
    this.offset = queryParams.offset;
    this.fuel = queryParams.fuel;
    this.depot = queryParams.depot;
    this.region = queryParams.region;
  }

  async fetchLots() {
    this.isLoading = true;
    try {
      const data: LotsResponse = await fetchLotsFromApi({
        page: this.page,
        offset: this.offset,
        fuel: this.fuel,
        depot: this.depot,
        region: this.region,
      });
      if (this.page === 1) {
        this.lots = data.lots;
      } else {
        // При подгрузке следующих страниц дописываем новые лоты
        this.lots = [...this.lots, ...data.lots];
      }
      this.pageCount = data.page_count;
    } catch (error) {
      console.error('Ошибка при получении лотов:', error);
    } finally {
      this.isLoading = false;
    }
  }

  setPage(page: number) {
    this.page = page;
    this.updateUrlParams();
    this.fetchLots();
  }

  setOffset(offset: number) {
    this.offset = offset;
    this.updateUrlParams();
    this.fetchLots();
  }

  setFuel(fuel: string) {
    this.fuel = fuel;
    this.updateUrlParams();
    this.fetchLots();
  }

  setDepot(depot: string) {
    this.depot = depot;
    this.updateUrlParams();
    this.fetchLots();
  }

  setRegion(region: string) {
    this.region = region;
    this.updateUrlParams();
    this.fetchLots();
  }

  // Функция для обновления URL с новыми параметрами
  private updateUrlParams() {
    const url = new URL(window.location.href);
    const searchParams = new URLSearchParams();

    if (this.page) searchParams.set('page', this.page.toString());
    if (this.offset) searchParams.set('offset', this.offset.toString());
    if (this.fuel) searchParams.set('fuel', this.fuel);
    if (this.depot) searchParams.set('depot', this.depot);
    if (this.region) searchParams.set('region', this.region);

    url.search = searchParams.toString();
    window.history.pushState({}, '', url.toString());
  }

  get confirmedLots(): Lot[] {
    return this.lots.filter((lot) => lot.status === 'Подтверждён');
  }
}

export default new CatalogStore();
