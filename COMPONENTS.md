# Stanza Pipeline Components & NLP Concepts

Stanza processes raw text by pushing it through a sequence of mathematical models called "components" (or processors). Each component accomplishes a specific linguistic task, adding a new layer of understanding to the text.

Below is a simple-language guide explaining each major component in Stanza, what it does, and links to free educational resources if you want to learn the underlying Natural Language Processing (NLP) concepts.

---

## 1. Tokenization & Sentence Segmentation (`tokenize`)
**What it does:** It takes a large chunk of raw text and chops it up into individual sentences, and then splits those sentences into individual words and punctuation marks (called "tokens").
**Why it's useful:** Computers can't easily read an entire book as a single string. They need the text broken down into distinct puzzle pieces (words) to analyze grammar and meaning.
- 🎓 **Learn more:** [Hugging Face NLP Course: Tokenizers](https://huggingface.co/learn/nlp-course/chapter2/4)
- 🎓 **Learn more:** [Stanford SLP Textbook: Regular Expressions & Text Normalization](https://web.stanford.edu/~jurafsky/slp3/2.pdf)

## 2. Multi-Word Token Expansion (`mwt`)
**What it does:** It takes contracted or joined words and splits them into their base grammatical parts. For example, in French, the word "du" is expanded to its underlying words "de" + "le".
**Why it's useful:** It reveals the hidden grammatical words that humans merge together for easier pronunciation, giving the computer a more accurate picture of the sentence structure.
- 🎓 **Learn more:** [NLTK Book: Morphology and Word Structure](https://www.nltk.org/book/ch03.html)

## 3. Part-of-Speech & Morphological Tagging (`pos`)
**What it does:** It looks at each word and assigns it a grammatical category (Noun, Verb, Adjective, Pronoun). It also figures out "morphological features" (e.g., is the noun singular or plural? Is the verb past, present, or future tense?).
**Why it's useful:** It helps the computer understand the role of a word in a sentence, distinguishing between pairs like "She will **record** the song" (Verb) and "She broke the world **record**" (Noun).
- 🎓 **Learn more:** [Coursera: POS Tagging & Hidden Markov Models](https://www.coursera.org/learn/probabilistic-models-in-nlp)
- 🎓 **Learn more:** [Stanford SLP Textbook: Part-of-Speech Tagging](https://web.stanford.edu/~jurafsky/slp3/8.pdf)

## 4. Lemmatization (`lemma`)
**What it does:** It converts a word into its dictionary root form (called a "lemma"). For example, "running", "ran", and "runs" all get converted to "run". "Mice" gets converted to "mouse".
**Why it's useful:** If you want to count how many times someone talks about running, you want the computer to treat "run", "ran", and "running" as the same core concept rather than entirely different words.
- 🎓 **Learn more:** [Kaggle/Coursera: Text Preprocessing & Lemmatization vs Stemming](https://www.kaggle.com/code/sudalairajkumar/getting-started-with-text-preprocessing)

## 5. Dependency Parsing (`depparse`)
**What it does:** It figures out the grammatical relationships between words and links them together in a tree. It determines which word is the subject, which is the object, and which adjectives modify which nouns.
**Why it's useful:** It tells you *who* is doing *what* to *whom*. In "The quick brown fox jumped over the lazy dog", parsing connects "quick" and "brown" directly back to "fox", and identifies "fox" as the subject doing the jumping.
- 🎓 **Learn more:** [Stanford CS224N: Dependency Parsing Video](https://www.youtube.com/watch?v=wRWcqyrcA_k)
- 🎓 **Learn more:** [Stanford SLP Textbook: Dependency Parsing](https://web.stanford.edu/~jurafsky/slp3/18.pdf)

## 6. Named Entity Recognition (`ner`)
**What it does:** It scans the text specifically looking for proper nouns and categorizes them. It identifies People (e.g., "Nelson Mandela"), Places (e.g., "Paris", "Mount Everest"), Organizations (e.g., "United Nations", "Apple"), and sometimes dates or money.
**Why it's useful:** It is incredibly powerful for information extraction. You can feed it 10,000 news articles and automatically extract every company and CEO mentioned.
- 🎓 **Learn more:** [Stanford CS224N: Named Entity Recognition](https://www.youtube.com/watch?v=qX1QvG42uoo)
- 🎓 **Learn more:** [Hugging Face Course: Token Classification (NER)](https://huggingface.co/learn/nlp-course/chapter7/2)

## 7. Sentiment Analysis (`sentiment`)
**What it does:** It estimates the emotion or tone hidden inside a sentence, typically scoring it as Negative, Neutral, or Positive.
**Why it's useful:** Companies use this to automatically read thousands of product reviews or tweets to see if people are generally happy or angry about a new product release.
- 🎓 **Learn more:** [Coursera: Sentiment Analysis with Logistic Regression](https://www.coursera.org/learn/classification-vector-spaces-in-nlp)
- 🎓 **Learn more:** [DeepLearning.ai: Sentiment Analysis Guide](https://www.deeplearning.ai/resources/sentiment-analysis/)

## 8. Constituency Parsing (`constituency`)
**What it does:** Instead of linking individual words directly to each other (like Dependency Parsing), this breaks sentences into nested grammatical blocks—like a Noun Phrase, which is inside a Verb Phrase, which sits inside a Sentence block.
**Why it's useful:** It represents sentences the way theoretical linguists map them out (often using Chomskyan grammar), useful for advanced rule-based extraction or translation.
- 🎓 **Learn more:** [Stanford SLP Textbook: Constituency Grammars](https://web.stanford.edu/~jurafsky/slp3/17.pdf)

## 9. Language Identification (`langid`)
**What it does:** It looks at a piece of text and guesses which human language it is written in (e.g., classifying a text as English, French, Chinese, or Inuktitut).
**Why it's useful:** When dealing with millions of web pages, you first need to identify the language so you know which Stanza pipeline (English or French) you need to load to properly process it.
- 🎓 **Learn more:** [FastText: Language Identification Tutorial](https://fasttext.cc/docs/en/language-identification.html)

---
*Note: Stanza allows you to pick and choose exactly which of these components you want to run. If you only need Tokenization and NER, you can tell the pipeline to skip the rest, which saves time and computer memory!*
