
export interface WordItem {
  word: string;
  translation: string;
  pronunciation?: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface GameSession {
  id: string;
  groupName: string;
  startTime: Date;
  correctAnswers: number;
  wrongAnswers: number;
  score: number;
  totalTimePlayed: number;
  status: 'in-progress' | 'completed';
  trophy?: 'silver' | 'gold';
  isFavorite: boolean;
}

export type GameState = 'ready' | 'playing' | 'finished';

export interface GameData {
  currentWord: WordItem | null;
  remainingWords: WordItem[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  score: number;
  correctAnswers: number;
  wrongAnswers: number;
  startTime: Date | null;
}
