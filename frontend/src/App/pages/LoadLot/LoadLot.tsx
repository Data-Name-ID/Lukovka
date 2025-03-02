import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'components/Button';
import { apiRoutes } from 'config/apiRoutes';
import AuthStore from 'stores/AuthStore';

const LoadLot = () => {
  // Состояние для хранения выбранного файла
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!AuthStore.user?.is_admin) {
      navigate('/lots');
    }
  }, [navigate]);

  // Обработчик изменения файла
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  // Обработчик отправки файла на сервер
  const handleUpload = async () => {
    if (!file) {
      setError('Пожалуйста, выберите файл для загрузки');
      return;
    }

    const formData = new FormData();
    // Изменяем имя поля на 'csv_file', как ожидает сервер
    formData.append('csv_file', file);

    setIsUploading(true);
    setError(null);
    setSuccessMessage(null);

    // Получаем токен доступа (можно изменить логику получения)
    const accessToken = localStorage.getItem('access_token') || 'your_access_token_here';

    try {
      const response = await fetch(apiRoutes.LoadLod, {
        method: 'POST',
        body: formData,
        headers: {
          // Передаем токен в заголовке Authorization
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        console.error('Ошибка от сервера:', errorResponse);
        throw new Error('Ошибка при загрузке файла');
      }

      const data = await response.json();
      setSuccessMessage('Файл успешно загружен');
      console.log('Ответ от сервера:', data);
    } catch (err) {
      setError('Произошла ошибка при загрузке файла');
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="pt-4">Загрузить лот</h1>
      <div className="mb-3">
        <label htmlFor="formFile" className="form-label">
          Выберите файл для загрузки
        </label>
        <input className="form-control" type="file" id="formFile" onChange={handleFileChange} />
      </div>

      {/* Показываем ошибку или успешное сообщение */}
      {error && <div className="alert alert-danger">{error}</div>}
      {successMessage && <div className="alert alert-success">{successMessage}</div>}

      {/* Кнопка загрузки */}
      <Button onClick={handleUpload} disabled={isUploading}>
        {isUploading ? 'Загружается...' : 'Подтвердить'}
      </Button>
    </div>
  );
};

export default LoadLot;
