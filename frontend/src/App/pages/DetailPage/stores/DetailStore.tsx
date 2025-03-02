import { makeAutoObservable } from 'mobx';
import { LotDetail, fetchLotDetailFromApi } from 'api/getDetailLot';

class DetailStore {
  lot: LotDetail | null = null;
  isLoading: boolean = false;

  constructor() {
    makeAutoObservable(this);
  }

  async fetchLotDetail(id: number) {
    this.isLoading = true;
    try {
      this.lot = await fetchLotDetailFromApi(id);
    } catch (error) {
      console.error('Ошибка при получении деталей лота:', error);
      this.lot = null;
    } finally {
      this.isLoading = false;
    }
  }
}

export default new DetailStore();
