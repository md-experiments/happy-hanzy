// Type definitions for Firestore data models

export interface Radical {
  id: string;
  character: string;
  meaning: string;
  stroke_count: number;
  frequency: number;
  examples?: string[];
}

export interface Character {
  id: string;
  hanzi: string;
  pinyin: string;
  meaning: string;
  hsk_level: number;
  frequency: number;
  radicals?: string[];
}

export interface UserProgress {
  id?: string;
  user_id: string;
  item_id: string;
  item_type: 'radical' | 'character';
  mastery_level: 'new' | 'learning' | 'familiar' | 'mastered';
  last_reviewed: Date | any;
  next_review: Date | any;
  correct_count: number;
  incorrect_count: number;
  ease_factor: number;
  interval: number;
}

export interface QuizAttempt {
  id?: string;
  user_id: string;
  question_id: string;
  question_type: string;
  answer: string;
  correct: boolean;
  timestamp: Date | any;
}

export interface ProgressStats {
  total_learned: number;
  radicals_mastered: number;
  characters_mastered: number;
  accuracy_rate: number;
  streak_days: number;
  total_reviews: number;
}

export interface Mistake {
  question_id: string;
  question_type: string;
  count: number;
}
