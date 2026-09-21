import { request } from './api';

export const documentsService = {
  create: (text, fileName) =>
    request('/documents', {
      method: 'POST',
      body: JSON.stringify({ text, file_name: fileName })
    }),
  get: (id) => request(`/documents/${id}`),
  list: () => request('/documents'),
  delete: (id) => request(`/documents/${id}`, { method: 'DELETE' })
};