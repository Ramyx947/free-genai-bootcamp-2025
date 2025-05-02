export interface Dialogue {
  dialog: string[];
  question: string;
  options: Record<string, string>;
  correct_answer: string;
  audio_path?: string;
}

export interface AudioResponse {
  audio_url: string;
  duration: number;
}

export interface DialogueResponse {
  dialogues: Record<string, Dialogue>;
} 