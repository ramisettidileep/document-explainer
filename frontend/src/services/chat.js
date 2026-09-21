import { request } from './api';

export const chatService = {
  ask: (id, question) =>
    request(`/documents/${id}/chat`, {
      method: 'POST',
      body: JSON.stringify({ question })
    })
};