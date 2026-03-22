# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.
I explored both models and compared them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  
Example: “I used the rule based model only” or “I compared both models.”

I compared both the rule-based and ML models.

**Intended purpose:**  
What is this model trying to do?  
Example: classify short text messages as moods like positive, negative, neutral, or mixed.

Classify short text messages or social media posts as moods: positive, negative, neutral, or mixed.

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  
For the ML version, describe how training works at a high level (no math needed).

Rule-based: Assigns +1 for positive words, -1 for negative words, and handles negation phrases like "not happy" -> negative. The final numeric score is mapped to a label.
ML: Uses a bag-of-words representation (CountVectorizer) and trains a logistic regression classifier on labeled examples (SAMPLE_POSTS and TRUE_LABELS). Predicts labels based on learned word patterns.

## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.

Started with 6 starter posts.
Expanded to 16 posts with additional examples including mixed emotions, slang, emojis, and negation

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.

Labels were chosen based on the overall sentiment of each post.
Hard-to-label posts include:
    "Feeling tired but kind of hopeful" -> mixed
    "Lowkey stressed about finals but I think I got this" -> mixed
    "LOL that was so funny 😂" -> positive
These posts were deliberately chosen to test subtle, ambiguous, or slang-heavy language.

**Important characteristics of your dataset:**  
Examples you might include:  

- Contains slang or emojis  
- Includes sarcasm  
- Some posts express mixed feelings  
- Contains short or ambiguous messages

Contains slang: "lowkey", "no cap", "LOL"
Emojis: "🙂", "💀", "😂", "😅"
Sarcasm: "I love getting stuck in traffic"
Mixed emotions: "Feeling lowkey happy but also stressed 😅"
Short or ambiguous messages

**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

Small and imbalanced (more positive than mixed or neutral examples)
Limited slang, cultural references, or emojis
Does not cover long posts or complex sentence structures

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

- How positive and negative words affect score  
- Negation rules you added  
- Weighted words  
- Emoji handling  
- Threshold decisions for labels

Positive words -> +1, negative words -> -1
Negation handling: "not happy" -> negative, "not bad" -> positive
Thresholds: score >0 -> positive, score <0 -> negative, score =0 -> neutral
No special weighting for slang or emojis beyond word lists

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

Predictable and interpretable
Works reasonably well for clear positive/negative sentences with words in the lists

**Weaknesses of this approach:**  
Where does it fail?  
Examples: sarcasm, subtlety, mixed moods, unfamiliar slang.

Fails on sarcasm: "I love getting stuck in traffic" -> predicted positive instead of negative
Mixed emotions often misclassified: "Feeling tired but kind of hopeful" -> neutral
Slang and emojis not in word lists ignored: "LOL that was so funny 😂" -> neutral

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

Bag-of-words (CountVectorizer) encoding words in each post

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

Trained on SAMPLE_POSTS and TRUE_LABELS, including all new posts

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

Highly sensitive to newly added posts
Adding 5 new posts improved handling of mixed emotions, slang, and emojis
Training on small dataset leads to high training accuracy (1.0) but may overfit

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

Strengths: Learns patterns automatically, can handle slang and mixed emotions present in training data
Weaknesses: Overfits small dataset, fails on unseen slang or sarcastic phrasing not in training data

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.

Evaluated both models on all posts in SAMPLE_POSTS.
Rule-based accuracy: 0.67 after adding new posts
ML accuracy: 1.0 (perfect on training data)

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.

"I love this class so much" -> positive
"I am not happy about this" -> negative

**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.

rule-based:
"Feeling lowkey happy but also stressed 😅" -> predicted neutral (should be mixed)
"LOL that was so funny 😂" -> predicted neutral (should be positive)
"That exam was brutal 💀" -> predicted neutral (should be negative)

ML/rule-based failures:
ML corrected many failures of the rule-based model for slang, emojis, and mixed emotions.
ML is limited to training data, unseen slang or sarcasm outside the dataset might still fail.

## 6. Limitations

Describe the most important limitations.  
Examples:  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled

Small dataset -> may not generalize to other text sources
Cannot reliably detect sarcasm: "I love getting stuck in traffic" still misclassified by rule-based model
Rule-based relies on predefined word lists
ML model may overfit and fail on unseen slang, culture-specific terms, or longer posts

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
Examples: 

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

Misclassifying mood could lead to incorrect interpretation of distress or excitement
Slang, dialects, or emojis used by certain communities may be misinterpreted
Any use on personal messages must respect privacy and consent

## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only

Add more labeled posts, especially covering slang, sarcasm, and emojis
Enhance preprocessing: punctuation removal, emoji normalization, repeated-character handling
Use TF-IDF or word embeddings for ML model
Consider small neural networks or transformer models for better generalization
Improve rule-based scoring with more comprehensive word lists and better negation handling
Evaluate on a real test set, not just training accuracy
