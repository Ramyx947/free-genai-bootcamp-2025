
export type SortField = 'name' | 'wordCount';
export type SortOrder = 'asc' | 'desc';

export interface Word {
  romanian: string;
  english: string;
}

export interface WordGroup {
  id: number;
  name: string;
  wordCount: number;
  description: string;
  words?: Word[]; // Now using Word interface instead of string[]
}
