"""
Seed data script to populate Firestore with sample radicals and characters.
Run this script once to initialize your database with learning content.
"""

from services.firebase_service import initialize_firebase
from datetime import datetime

def seed_radicals():
    """Add sample radicals to Firestore"""
    db = initialize_firebase()
    
    sample_radicals = [
        {"character": "人", "meaning": "person", "stroke_count": 2, "frequency": 95, "examples": ["他", "你", "們"]},
        {"character": "口", "meaning": "mouth", "stroke_count": 3, "frequency": 90, "examples": ["吃", "叫", "問"]},
        {"character": "手", "meaning": "hand", "stroke_count": 4, "frequency": 88, "examples": ["打", "找", "拿"]},
        {"character": "心", "meaning": "heart", "stroke_count": 4, "frequency": 85, "examples": ["想", "思", "愛"]},
        {"character": "水", "meaning": "water", "stroke_count": 4, "frequency": 87, "examples": ["河", "海", "湖"]},
        {"character": "木", "meaning": "tree/wood", "stroke_count": 4, "frequency": 84, "examples": ["林", "森", "樹"]},
        {"character": "火", "meaning": "fire", "stroke_count": 4, "frequency": 80, "examples": ["炎", "燒", "熱"]},
        {"character": "土", "meaning": "earth/soil", "stroke_count": 3, "frequency": 82, "examples": ["地", "場", "城"]},
        {"character": "日", "meaning": "sun/day", "stroke_count": 4, "frequency": 92, "examples": ["明", "時", "晚"]},
        {"character": "月", "meaning": "moon/month", "stroke_count": 4, "frequency": 86, "examples": ["明", "期", "朋"]},
        {"character": "言", "meaning": "speech/words", "stroke_count": 7, "frequency": 83, "examples": ["話", "說", "語"]},
        {"character": "糸", "meaning": "thread/silk", "stroke_count": 6, "frequency": 75, "examples": ["紅", "緣", "線"]},
        {"character": "女", "meaning": "woman", "stroke_count": 3, "frequency": 81, "examples": ["她", "好", "媽"]},
        {"character": "子", "meaning": "child", "stroke_count": 3, "frequency": 79, "examples": ["學", "字", "孩"]},
        {"character": "一", "meaning": "one", "stroke_count": 1, "frequency": 100, "examples": ["二", "三", "天"]},
        {"character": "二", "meaning": "two", "stroke_count": 2, "frequency": 98, "examples": ["三", "王", "元"]},
        {"character": "竹", "meaning": "bamboo", "stroke_count": 6, "frequency": 70, "examples": ["筆", "笑", "等"]},
        {"character": "雨", "meaning": "rain", "stroke_count": 8, "frequency": 72, "examples": ["雪", "雲", "電"]},
        {"character": "金", "meaning": "metal/gold", "stroke_count": 8, "frequency": 76, "examples": ["銀", "錢", "鐵"]},
        {"character": "門", "meaning": "gate/door", "stroke_count": 8, "frequency": 74, "examples": ["開", "閉", "間"]},
    ]
    
    radicals_ref = db.collection('radicals')
    
    print("Seeding radicals...")
    for radical in sample_radicals:
        doc_ref = radicals_ref.add(radical)
        print(f"Added radical: {radical['character']} - {radical['meaning']} (ID: {doc_ref[1].id})")
    
    print(f"\n✓ Added {len(sample_radicals)} radicals to Firestore")

def seed_characters():
    """Add sample characters to Firestore"""
    db = initialize_firebase()
    
    # Get radical IDs (you'll need to adjust these based on your actual radical IDs)
    radicals_ref = db.collection('radicals')
    radical_map = {}
    for doc in radicals_ref.stream():
        data = doc.to_dict()
        radical_map[data['character']] = doc.id
    
    sample_characters = [
        {
            "hanzi": "好",
            "pinyin": "hǎo",
            "meaning": "good, well",
            "hsk_level": 1,
            "frequency": 95,
            "radicals": []  # Will be populated with actual IDs
        },
        {
            "hanzi": "你",
            "pinyin": "nǐ",
            "meaning": "you",
            "hsk_level": 1,
            "frequency": 100,
            "radicals": []
        },
        {
            "hanzi": "我",
            "pinyin": "wǒ",
            "meaning": "I, me",
            "hsk_level": 1,
            "frequency": 98,
            "radicals": []
        },
        {
            "hanzi": "他",
            "pinyin": "tā",
            "meaning": "he, him",
            "hsk_level": 1,
            "frequency": 97,
            "radicals": []
        },
        {
            "hanzi": "們",
            "pinyin": "men",
            "meaning": "plural marker",
            "hsk_level": 1,
            "frequency": 92,
            "radicals": []
        },
        {
            "hanzi": "說",
            "pinyin": "shuō",
            "meaning": "to say, to speak",
            "hsk_level": 1,
            "frequency": 90,
            "radicals": []
        },
        {
            "hanzi": "學",
            "pinyin": "xué",
            "meaning": "to learn, to study",
            "hsk_level": 1,
            "frequency": 89,
            "radicals": []
        },
        {
            "hanzi": "中",
            "pinyin": "zhōng",
            "meaning": "middle, center, China",
            "hsk_level": 1,
            "frequency": 96,
            "radicals": []
        },
        {
            "hanzi": "國",
            "pinyin": "guó",
            "meaning": "country, nation",
            "hsk_level": 1,
            "frequency": 94,
            "radicals": []
        },
        {
            "hanzi": "人",
            "pinyin": "rén",
            "meaning": "person, people",
            "hsk_level": 1,
            "frequency": 99,
            "radicals": []
        },
    ]
    
    characters_ref = db.collection('characters')
    
    print("\nSeeding characters...")
    for character in sample_characters:
        doc_ref = characters_ref.add(character)
        print(f"Added character: {character['hanzi']} ({character['pinyin']}) - {character['meaning']} (ID: {doc_ref[1].id})")
    
    print(f"\n✓ Added {len(sample_characters)} characters to Firestore")

def main():
    print("=" * 60)
    print("Happy Hanzy - Database Seeding Script")
    print("=" * 60)
    print("\nThis script will populate your Firestore database with sample")
    print("radicals and characters for testing and initial content.\n")
    
    try:
        seed_radicals()
        seed_characters()
        
        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        print("\nYou can now start the application and begin learning!")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        print("\nMake sure:")
        print("1. Your .env file is configured with Firebase credentials")
        print("2. You have proper permissions to write to Firestore")
        print("3. Your Firebase project is set up correctly")

if __name__ == "__main__":
    main()
