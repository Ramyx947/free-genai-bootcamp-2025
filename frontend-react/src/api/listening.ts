import { fetchWithTimeout } from './index';
import type { DialogueResponse, AudioResponse } from '@/types/listening';

export const getDialogues = async (): Promise<DialogueResponse> => {
  return await fetchWithTimeout('/api/dialogues');
};

export const getAudio = async (topicId: string): Promise<AudioResponse> => {
  return await fetchWithTimeout(`/api/audio/${topicId}`);
};

const API_TIMEOUT = 600000; // 10 minutes

export const checkAPIHealth = async () => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    const response = await fetch('http://localhost:8000/health', {
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    return response.ok;
  } catch {
    return false;
  }
};