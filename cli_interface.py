import os
import sys
from quiz_tool import QuizTool
from automation import QuizAutomator
from config import OPENAI_API_KEY

def main():
    print("\n=== Perfect Score Quiz Tool ===")
    print("1. Process Quiz from Files")
    print("2. Process Quiz from Text/URL")
    print("3. Auto-Submit Quiz (requires login)")
    print("4. Exit")
    
    choice = input("\nSelect an option (1-4): ")
    
    quiz_tool = QuizTool()
    automator = None
    
    try:
        if choice == "1":
            file_path = input("Enter path to lesson material (PDF/TXT): ")
            quiz_source = input("Enter path to quiz questions file: ")
            
            quiz_tool.load_lesson(file_path)
            with open(quiz_source, 'r') as f:
                quiz_text = f.read()
            questions = quiz_tool.extract_quiz_questions(quiz_text)
            
        elif choice == "2":
            lesson_source = input("Enter lesson text or URL: ")
            quiz_text = input("Enter quiz questions text: ")
            
            quiz_tool.load_lesson(lesson_source)
            questions = quiz_tool.extract_quiz_questions(quiz_text)
            
        elif choice == "3":
            if not OPENAI_API_KEY:
                print("Error: OpenAI API key not configured in config.py")
                return
                
            username = input("Enter your e-learning username: ")
            password = input("Enter your password: ")
            quiz_url = input("Enter quiz URL: ")
            
            automator = QuizAutomator(username, password)
            automator.initialize_driver()
            
            if not automator.login():
                print("Login failed. Please check credentials.")
                return
                
            # Process quiz directly from the page
            # This would need to be implemented based on the specific website structure
            print("Auto-submit feature would be implemented here")
            return
            
        elif choice == "4":
            print("Exiting...")
            return
            
        else:
            print("Invalid choice")
            return
            
        # Process questions
        print("\nFound questions:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")
            
        question_type = input("\nQuestion type (multiple_choice/short_answer): ")
        options = None
        
        if question_type == "multiple_choice":
            options = input("Enter options (comma separated): ").split(',')
            
        answers = quiz_tool.generate_answers(question_type, options)
        
        print("\nGenerated Answers:")
        for i, (q, a) in enumerate(zip(questions, answers), 1):
            print(f"\nQuestion {i}: {q}")
            print(f"Answer: {a['answer'] if 'answer' in a else a['option']}")
            print(f"Confidence: {a['confidence']:.2f}")
            print(f"Source: {a['source']}")
            
        save = input("\nSave results to file? (y/n): ")
        if save.lower() == 'y':
            quiz_tool.save_results()
            print("Results saved to quiz_results.json")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if automator:
            automator.close()

if __name__ == "__main__":
    main()