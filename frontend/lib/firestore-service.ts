import { db } from './firebase';
import { collection, getDocs, getDoc, doc, query, where, orderBy, limit, addDoc, updateDoc } from 'firebase/firestore';
import { Radical, Character, UserProgress, ProgressStats, Mistake } from './types';

// Radical Operations
export const getRadicals = async (limitCount: number = 50): Promise<Radical[]> => {
  try {
    const radicalsRef = collection(db, 'radicals');
    const q = query(radicalsRef, orderBy('frequency', 'desc'), limit(limitCount));
    const querySnapshot = await getDocs(q);
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Error fetching radicals:', error);
    return [];
  }
};

export const getRadicalById = async (radicalId: string) => {
  try {
    const radicalRef = doc(db, 'radicals', radicalId);
    const radicalSnap = await getDoc(radicalRef);
    
    if (radicalSnap.exists()) {
      return {
        id: radicalSnap.id,
        ...radicalSnap.data()
      };
    }
    return null;
  } catch (error) {
    console.error('Error fetching radical:', error);
    return null;
  }
};

// Character Operations
export const getCharacters = async (limitCount: number = 50, hskLevel?: number) => {
  try {
    const charactersRef = collection(db, 'characters');
    let q = query(charactersRef, orderBy('frequency', 'desc'), limit(limitCount));
    
    if (hskLevel) {
      q = query(charactersRef, where('hsk_level', '==', hskLevel), orderBy('frequency', 'desc'), limit(limitCount));
    }
    
    const querySnapshot = await getDocs(q);
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Error fetching characters:', error);
    return [];
  }
};

export const getCharacterById = async (characterId: string) => {
  try {
    const characterRef = doc(db, 'characters', characterId);
    const characterSnap = await getDoc(characterRef);
    
    if (characterSnap.exists()) {
      return {
        id: characterSnap.id,
        ...characterSnap.data()
      };
    }
    return null;
  } catch (error) {
    console.error('Error fetching character:', error);
    return null;
  }
};

export const getCharacterRadicals = async (characterId: string) => {
  try {
    const character = await getCharacterById(characterId);
    if (!character || !character.radicals) {
      return [];
    }
    
    const radicalPromises = character.radicals.map((radicalId: string) => getRadicalById(radicalId));
    const radicals = await Promise.all(radicalPromises);
    
    return radicals.filter(r => r !== null);
  } catch (error) {
    console.error('Error fetching character radicals:', error);
    return [];
  }
};

// User Progress Operations
export const getUserProgress = async (userId: string) => {
  try {
    const progressRef = collection(db, 'user_progress');
    const q = query(progressRef, where('user_id', '==', userId));
    const querySnapshot = await getDocs(q);
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Error fetching user progress:', error);
    return [];
  }
};

export const getDueItems = async (userId: string) => {
  try {
    const progressRef = collection(db, 'user_progress');
    const q = query(progressRef, where('user_id', '==', userId));
    const querySnapshot = await getDocs(q);
    
    const now = new Date();
    const dueItems = querySnapshot.docs
      .map(doc => ({
        id: doc.id,
        ...doc.data()
      }))
      .filter((item: any) => {
        const nextReview = item.next_review?.toDate ? item.next_review.toDate() : new Date(item.next_review);
        return nextReview <= now;
      });
    
    return dueItems;
  } catch (error) {
    console.error('Error fetching due items:', error);
    return [];
  }
};

export const recordReview = async (userId: string, itemId: string, itemType: string, correct: boolean) => {
  try {
    const progressRef = collection(db, 'user_progress');
    const q = query(progressRef, where('user_id', '==', userId), where('item_id', '==', itemId));
    const querySnapshot = await getDocs(q);
    
    if (!querySnapshot.empty) {
      // Update existing progress
      const docRef = querySnapshot.docs[0].ref;
      const data = querySnapshot.docs[0].data();
      
      const correctCount = (data.correct_count || 0) + (correct ? 1 : 0);
      const incorrectCount = (data.incorrect_count || 0) + (correct ? 0 : 1);
      
      await updateDoc(docRef, {
        correct_count: correctCount,
        incorrect_count: incorrectCount,
        last_reviewed: new Date(),
        // Simple spaced repetition: increase interval if correct
        interval: correct ? Math.max(1, (data.interval || 0) * 2) : 1,
      });
    } else {
      // Create new progress record
      await addDoc(progressRef, {
        user_id: userId,
        item_id: itemId,
        item_type: itemType,
        mastery_level: 'new',
        last_reviewed: new Date(),
        next_review: new Date(Date.now() + 24 * 60 * 60 * 1000), // 1 day
        correct_count: correct ? 1 : 0,
        incorrect_count: correct ? 0 : 1,
        ease_factor: 2.5,
        interval: 1,
      });
    }
    
    return { success: true };
  } catch (error) {
    console.error('Error recording review:', error);
    return { success: false, error };
  }
};

export const getProgressStats = async (userId: string) => {
  try {
    const progressRef = collection(db, 'user_progress');
    const q = query(progressRef, where('user_id', '==', userId));
    const querySnapshot = await getDocs(q);
    
    let totalLearned = 0;
    let radicalsMastered = 0;
    let charactersMastered = 0;
    let totalCorrect = 0;
    let totalAttempts = 0;
    
    querySnapshot.docs.forEach(doc => {
      const data = doc.data();
      totalLearned++;
      
      if (data.mastery_level === 'mastered') {
        if (data.item_type === 'radical') {
          radicalsMastered++;
        } else if (data.item_type === 'character') {
          charactersMastered++;
        }
      }
      
      totalCorrect += data.correct_count || 0;
      totalAttempts += (data.correct_count || 0) + (data.incorrect_count || 0);
    });
    
    const accuracyRate = totalAttempts > 0 ? (totalCorrect / totalAttempts) * 100 : 0;
    
    return {
      total_learned: totalLearned,
      radicals_mastered: radicalsMastered,
      characters_mastered: charactersMastered,
      accuracy_rate: accuracyRate,
      streak_days: 0, // TODO: Calculate streak
      total_reviews: totalAttempts,
    };
  } catch (error) {
    console.error('Error fetching progress stats:', error);
    return {
      total_learned: 0,
      radicals_mastered: 0,
      characters_mastered: 0,
      accuracy_rate: 0,
      streak_days: 0,
      total_reviews: 0,
    };
  }
};

// Quiz Operations
export const submitQuizAnswer = async (userId: string, questionId: string, questionType: string, answer: string, correct: boolean) => {
  try {
    const attemptsRef = collection(db, 'quiz_attempts');
    await addDoc(attemptsRef, {
      user_id: userId,
      question_id: questionId,
      question_type: questionType,
      answer,
      correct,
      timestamp: new Date(),
    });
    
    return { success: true };
  } catch (error) {
    console.error('Error submitting quiz answer:', error);
    return { success: false, error };
  }
};

export const getQuizHistory = async (userId: string, limitCount: number = 50) => {
  try {
    const attemptsRef = collection(db, 'quiz_attempts');
    const q = query(attemptsRef, where('user_id', '==', userId), orderBy('timestamp', 'desc'), limit(limitCount));
    const querySnapshot = await getDocs(q);
    
    return querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Error fetching quiz history:', error);
    return [];
  }
};

export const getMistakes = async (userId: string) => {
  try {
    const attemptsRef = collection(db, 'quiz_attempts');
    const q = query(attemptsRef, where('user_id', '==', userId), where('correct', '==', false));
    const querySnapshot = await getDocs(q);
    
    const mistakes: { [key: string]: { question_id: string; question_type: string; count: number } } = {};
    
    querySnapshot.docs.forEach(doc => {
      const data = doc.data();
      const questionId = data.question_id;
      
      if (mistakes[questionId]) {
        mistakes[questionId].count++;
      } else {
        mistakes[questionId] = {
          question_id: questionId,
          question_type: data.question_type,
          count: 1,
        };
      }
    });
    
    return Object.values(mistakes).sort((a, b) => b.count - a.count).slice(0, 20);
  } catch (error) {
    console.error('Error fetching mistakes:', error);
    return [];
  }
};
