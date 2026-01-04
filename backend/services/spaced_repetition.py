from datetime import datetime, timedelta
from models.schemas import UserProgress, MasteryLevel

class SpacedRepetitionService:
    """
    Implements a spaced repetition algorithm (similar to SM-2/Anki)
    for optimal learning scheduling.
    """
    
    @staticmethod
    def calculate_next_review(progress: UserProgress, correct: bool) -> UserProgress:
        """
        Calculate the next review date based on performance.
        
        Args:
            progress: Current user progress
            correct: Whether the answer was correct
            
        Returns:
            Updated UserProgress with new scheduling parameters
        """
        if correct:
            progress.correct_count += 1
            
            # Update ease factor (quality 4 for correct)
            progress.ease_factor = max(1.3, progress.ease_factor + 0.1)
            
            # Calculate new interval
            if progress.interval == 0:
                progress.interval = 1
            elif progress.interval == 1:
                progress.interval = 6
            else:
                progress.interval = int(progress.interval * progress.ease_factor)
            
            # Update mastery level based on performance
            if progress.interval >= 21 and progress.correct_count >= 5:
                progress.mastery_level = MasteryLevel.MASTERED
            elif progress.interval >= 6:
                progress.mastery_level = MasteryLevel.FAMILIAR
            elif progress.correct_count >= 1:
                progress.mastery_level = MasteryLevel.LEARNING
                
        else:
            progress.incorrect_count += 1
            
            # Reduce ease factor for incorrect answers
            progress.ease_factor = max(1.3, progress.ease_factor - 0.2)
            
            # Reset interval for incorrect answers
            progress.interval = 1
            
            # Update mastery level
            if progress.mastery_level == MasteryLevel.MASTERED:
                progress.mastery_level = MasteryLevel.FAMILIAR
            elif progress.mastery_level == MasteryLevel.FAMILIAR:
                progress.mastery_level = MasteryLevel.LEARNING
            else:
                progress.mastery_level = MasteryLevel.NEW
        
        # Set next review date
        progress.last_reviewed = datetime.now()
        progress.next_review = datetime.now() + timedelta(days=progress.interval)
        
        return progress
    
    @staticmethod
    def get_items_due_for_review(user_progress_list: list[UserProgress]) -> list[UserProgress]:
        """
        Get items that are due for review.
        
        Args:
            user_progress_list: List of user progress items
            
        Returns:
            List of items due for review, sorted by priority
        """
        now = datetime.now()
        due_items = [p for p in user_progress_list if p.next_review <= now]
        
        # Sort by next_review (oldest first) and mastery level (new items first)
        mastery_priority = {
            MasteryLevel.NEW: 0,
            MasteryLevel.LEARNING: 1,
            MasteryLevel.FAMILIAR: 2,
            MasteryLevel.MASTERED: 3
        }
        
        due_items.sort(key=lambda x: (x.next_review, mastery_priority[x.mastery_level]))
        
        return due_items
    
    @staticmethod
    def calculate_retention_rate(progress: UserProgress) -> float:
        """
        Calculate retention rate for an item.
        
        Args:
            progress: User progress item
            
        Returns:
            Retention rate as a percentage (0-100)
        """
        total = progress.correct_count + progress.incorrect_count
        if total == 0:
            return 0.0
        
        return (progress.correct_count / total) * 100
