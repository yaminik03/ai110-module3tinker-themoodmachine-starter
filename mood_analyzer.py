# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

import re

class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        cleaned = text.lower().strip()
      
        cleaned = re.sub(r"[^\w\s🥲😂😭💀:()]", "", cleaned)
        tokens = cleaned.split()

        #print("TOKENS:", tokens)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
      tokens = self.preprocess(text)
      score = 0

      i = 0
      while i < len(tokens):
        word = tokens[i]

        # Handle negation (look at next word)
        if word == "not" and i + 1 < len(tokens):
            next_word = tokens[i + 1]

            if next_word in self.positive_words:
                score -= 1  # "not happy" → negative
                i += 2
                continue
            elif next_word in self.negative_words:
                score += 1  # "not bad" → positive
                i += 2
                continue

        # Normal scoring
        if word in self.positive_words:
            score += 1
        elif word in self.negative_words:
            score -= 1

        i += 1
        
      return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        score = self.score_text(text)

        if score > 0:
          return "positive"
        elif score < 0:
            return "negative"
        elif score == 0:
          return "neutral"
        else:
          return "mixed"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
if __name__ == "__main__":
    analyzer = MoodAnalyzer()

    print(analyzer.predict_label("I love this"))              # positive
    print(analyzer.predict_label("I hate this"))              # negative
    print(analyzer.predict_label("I am not happy"))           # negative
    print(analyzer.predict_label("This is not bad"))          # positive
    print(analyzer.predict_label("Feeling tired but hopeful"))# mixed or neutral (depends on your logic)
    print(analyzer.predict_label("This is fine"))             # neutral

    # -------------------------------
    # Breaker sentences (new test set)
    # -------------------------------

    BREAKER_SENTENCES = [
        "I love getting stuck in traffic",
        "This concert was sick 🔥",
        "I’m fine 🙂",
        "I’m exhausted but proud of myself",
        "That movie was wicked good",
        "I literally hate waiting in lines 😩",
        "Lowkey nervous but also excited",
        "This pizza is fire 🔥",
        "I can’t believe I lost again 💀",
        "Feeling meh about everything today",
    ]

    # Test breaker sentences
    print("\n=== Breaker Sentences ===")
    for sentence in BREAKER_SENTENCES:
        label = analyzer.predict_label(sentence)
        print(f'"{sentence}" -> predicted={label}')
