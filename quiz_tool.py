import os
import json
from typing import List, Dict, Union
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS, SIMILARITY_THRESHOLD
from utils import read_pdf, read_txt, scrape_webpage, extract_questions, calculate_similarity

client = OpenAI(api_key=OPENAI_API_KEY)

class QuizTool:
    def __init__(self):
        self.lesson_content = ""
        self.questions = []
        self.answers = []

    def load_lesson(self, source: Union[str, bytes]) -> None:
        """Load lesson material from file or direct text"""
        if isinstance(source, bytes):
            # Handle file upload
            with open("temp_upload", "wb") as f:
                f.write(source)
            source = "temp_upload"

        if os.path.exists(source):
            if source.endswith('.pdf'):
                self.lesson_content = read_pdf(source)
            elif source.endswith('.txt'):
                self.lesson_content = read_txt(source)
        else:
            # Treat as direct text input or URL
            if source.startswith('http'):
                self.lesson_content = scrape_webpage(source)
            else:
                self.lesson_content = source

    def extract_quiz_questions(self, quiz_source: str) -> List[str]:
        """Extract questions from quiz text or file"""
        self.questions = extract_questions(quiz_source)
        return self.questions

    def generate_answers(self, question_type: str = "multiple_choice", options: List[str] = None) -> List[Dict]:
        """Generate answers for loaded questions"""
        if not self.questions or not self.lesson_content:
            raise ValueError("No questions or lesson content loaded")

        self.answers = []
        for question in self.questions:
            if question_type == "multiple_choice" and options:
                answer = self._find_best_match(question, options)
            else:
                answer = self._generate_short_answer(question)
            self.answers.append(answer)
        return self.answers

    def _find_best_match(self, question: str, options: List[str]) -> Dict:
        """Find best matching option for multiple choice questions"""
        best_match = {"option": "", "confidence": 0, "source": ""}
        for option in options:
            similarity = calculate_similarity(question + " " + option, self.lesson_content)
            if similarity > best_match["confidence"]:
                best_match = {
                    "option": option,
                    "confidence": similarity,
                    "source": self._find_source_reference(question)
                }
        return best_match

    def _generate_short_answer(self, question: str) -> Dict:
        """Generate short answer using OpenAI API"""
        prompt = f"Based on the following lesson content:\n{self.lesson_content}\n\nAnswer this question: {question}"
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=OPENAI_MAX_TOKENS
        )
        
        return {
            "answer": response.choices[0].message.content,
            "confidence": 1.0,  # LLM answers assumed to be high confidence
            "source": self._find_source_reference(question)
        }

    def _find_source_reference(self, question: str) -> str:
        """Find relevant section in lesson material"""
        # Simple implementation - can be enhanced
        sentences = self.lesson_content.split('.')
        for i, sentence in enumerate(sentences):
            if calculate_similarity(question, sentence) > SIMILARITY_THRESHOLD:
                return f"Section {i+1}"
        return "General reference"

    def save_results(self, output_file: str = "quiz_results.json") -> None:
        """Save questions and answers to JSON file"""
        results = {
            "questions": self.questions,
            "answers": self.answers,
            "lesson_source": self.lesson_content[:100] + "..." if self.lesson_content else ""
        }
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    print("Quiz Tool module loaded. Import and use the QuizTool class.")