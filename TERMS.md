# Stanza Terms, Acronyms, and Entities Reference

List of unique terms, acronyms, people, organizations, and entities found in the Stanza project codebase and documentation.

## Table of Contents
- [Acronyms and Technical Terms](#acronyms-and-technical-terms)
- [NLP Concepts](#nlp-concepts)
- [Frameworks and Tools](#frameworks-and-tools)
- [People and Contributors](#people-and-contributors)
- [Organizations and Conferences](#organizations-and-conferences)
- [Stanza Components](#stanza-components)

---

## Acronyms and Technical Terms

| Term | Acronym | Description | Confidence | Search Links |
|------|---------|-------------|------------|--------------|
| Bidirectional Encoder Representations from Transformers | BERT | A pre-trained transformer-based model for natural language understanding developed by Google. Used in Stanza for embeddings and feature extraction. | 95% | [Wikipedia](https://en.wikipedia.org/wiki/BERT_(language_model)) \| [Google Search](https://www.google.com/search?q=BERT+language+model) |
| Named Entity Recognition | NER | Task of identifying and classifying named entities (persons, organizations, locations, etc.) in text. | 98% | [Wikipedia](https://en.wikipedia.org/wiki/Named-entity_recognition) \| [Google Search](https://www.google.com/search?q=named+entity+recognition) |
| Natural Language Processing | NLP | Field of artificial intelligence concerned with the interactions between computers and human language. | 99% | [Wikipedia](https://en.wikipedia.org/wiki/Natural_language_processing) \| [Google Search](https://www.google.com/search?q=natural+language+processing) |
| Part-of-Speech | POS | Grammatical category of words (noun, verb, adjective, etc.). POS tagging is the task of assigning these labels. | 98% | [Wikipedia](https://en.wikipedia.org/wiki/Part_of_speech) \| [Google Search](https://www.google.com/search?q=part+of+speech+tagging) |
| Multi-Word Token | MWT | A token that represents multiple words, common in languages with clitics or contractions. | 90% | [UD Documentation](https://universaldependencies.org/format.html) \| [Google Search](https://www.google.com/search?q=multi+word+token) |
| Universal Dependencies | UD | A framework for consistent annotation of grammatical structure across different languages. | 95% | [Wikipedia](https://en.wikipedia.org/wiki/Universal_Dependencies) \| [Google Search](https://www.google.com/search?q=universal+dependencies) |
| Conference on Computational Natural Language Learning | CoNLL | Major annual conference and shared task for NLP. | 92% | [Wikipedia](https://en.wikipedia.org/wiki/Conference_on_Computational_Natural_Language_Learning) \| [Google Search](https://www.google.com/search?q=CoNLL+conference) |
| Long Short-Term Memory | LSTM | A type of recurrent neural network architecture capable of learning long-term dependencies. | 97% | [Wikipedia](https://en.wikipedia.org/wiki/Long_short-term_memory) \| [Google Search](https://www.google.com/search?q=LSTM+neural+network) |
| Conditional Random Field | CRF | A probabilistic graphical model used for structured prediction, commonly used in NLP tasks. | 95% | [Wikipedia](https://en.wikipedia.org/wiki/Conditional_random_field) \| [Google Search](https://www.google.com/search?q=conditional+random+field+NLP) |
| Character Language Model | CharLM | A language model that operates at the character level rather than word level. | 85% | [Google Search](https://www.google.com/search?q=character+language+model) \| [Research Papers](https://www.google.com/search?q=character+level+language+model+NLP) |
| Convolutional Neural Network | CNN | Neural network architecture using convolution operations, applied to text in Stanza classifiers. | 96% | [Wikipedia](https://en.wikipedia.org/wiki/Convolutional_neural_network) \| [Google Search](https://www.google.com/search?q=CNN+text) |
| Protocol Buffers | Protobuf | Method of serializing structured data developed by Google, used for efficient data exchange. | 90% | [Wikipedia](https://en.wikipedia.org/wiki/Protocol_Buffers) \| [Google Search](https://www.google.com/search?q=protocol+buffers) |
| Dependency Graph | DepGraph | A representation of grammatical relationships between words in a sentence as a directed graph. | 88% | [Google Search](https://www.google.com/search?q=dependency+graph+NLP) \| [UD Format](https://universaldependencies.org/format.html) |
| Semantic Graph Regular Expressions | Semgrex | A language for searching and manipulating dependency graphs. | 85% | [Google Search](https://www.google.com/search?q=Semgrex+Stanford) \| [Official Documentation](https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/semgraph/semgrex/SemgrexMatcher.html) |
| Syntax Surgeon | Ssurgeon | A tool for manipulating dependency graphs based on patterns matched by Semgrex. | 82% | [Google Search](https://www.google.com/search?q=Ssurgeon+Stanford+NLP) \| [Documentation](https://github.com/stanfordnlp/CoreNLP) |
| Parameter-Efficient Fine-Tuning | PEFT | Technique to fine-tune large pre-trained models with fewer trainable parameters. | 85% | [Google Search](https://www.google.com/search?q=PEFT+parameter+efficient+fine+tuning) \| [Hugging Face](https://huggingface.co/docs/peft) |

---

## NLP Concepts

| Term | Description | Confidence | Search Links |
|------|-------------|------------|--------------|
| Tokenization | Process of splitting text into words, sentences, or subword units. | 99% | [Wikipedia](https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization) \| [Google Search](https://www.google.com/search?q=tokenization+NLP) |
| Lemmatization | Morphological process of reducing words to their base or dictionary form (lemma). | 97% | [Wikipedia](https://en.wikipedia.org/wiki/Lemmatization) \| [Google Search](https://www.google.com/search?q=lemmatization+NLP) |
| Dependency Parsing | Syntactic analysis that represents grammatical relationships between words. | 95% | [Wikipedia](https://en.wikipedia.org/wiki/Dependency_parsing) \| [Google Search](https://www.google.com/search?q=dependency+parsing) |
| Constituency Parsing | Syntactic analysis that builds a parse tree showing hierarchical phrase structure. | 93% | [Wikipedia](https://en.wikipedia.org/wiki/Parsing) \| [Google Search](https://www.google.com/search?q=constituency+parsing) |
| Coreference Resolution | Task of identifying which noun phrases refer to the same entity in a discourse. | 92% | [Wikipedia](https://en.wikipedia.org/wiki/Coreference) \| [Google Search](https://www.google.com/search?q=coreference+resolution) |
| Morphological Segmentation | Process of segmenting words into morphemes (smallest meaningful units). | 88% | [Google Search](https://www.google.com/search?q=morphological+segmentation) \| [Research](https://www.google.com/search?q=morpheme+segmentation+NLP) |
| Sentiment Analysis | Task of determining the sentiment (positive, negative, neutral) expressed in text. | 96% | [Wikipedia](https://en.wikipedia.org/wiki/Sentiment_analysis) \| [Google Search](https://www.google.com/search?q=sentiment+analysis) |
| Language Identification | Task of automatically determining which language a text is written in. | 94% | [Wikipedia](https://en.wikipedia.org/wiki/Language_identification) \| [Google Search](https://www.google.com/search?q=language+identification) |
| Embedding | Vector representation of words or text in a continuous space. | 96% | [Wikipedia](https://en.wikipedia.org/wiki/Word_embedding) \| [Google Search](https://www.google.com/search?q=word+embedding+NLP) |
| Pretrained Model | Large language model trained on large corpora and fine-tuned for specific tasks. | 95% | [Google Search](https://www.google.com/search?q=pretrained+language+model) \| [Hugging Face](https://huggingface.co/models) |

---

## Frameworks and Tools

| Tool/Framework | Description | Type | Confidence |
|---|---|---|---|
| PyTorch | Open-source machine learning library for Python used for neural models. | Deep Learning Framework | 98% |
| Transformers | Hugging Face library providing access to pre-trained transformer models. | Library | 95% |
| CUDA | Parallel computing platform by NVIDIA for GPU acceleration. | GPU Computing | 97% |
| CoreNLP | Java-based NLP toolkit from Stanford providing various NLP tools. | NLP Toolkit | 98% |
| Protobuf | Google's protocol for serializing structured data | Data Format | 92% |
| Jieba | Chinese text segmentation library used as external tokenizer. | External Tool | 85% |
| PyThaiNLP | Thai NLP library used as external tool in Stanza. | External Tool | 85% |
| Sudachi | Japanese morphological analyzer. | External Tool | 82% |
| spaCy | Popular open-source NLP library for Python. | NLP Library | 97% |
| crfsuite | Conditional Random Field library wrapped by python-crfsuite. | Machine Learning | 88% |

---

## People and Contributors

| Name | Role/Affiliation | GitHub Handle | Confidence |
|------|---|---|---|
| Peng Qi | Lead Architect, Stanford NLP | @qipeng | 98% |
| Yuhao Zhang | Core Developer, Stanford NLP | @yuhaozhang | 98% |
| Yuhui Zhang | Core Developer, Stanford NLP | @yuhui-zh15 | 98% |
| Jason Bolton | Contributor, CoreNLP Integration | @j38 | 95% |
| Tim Dozat | Contributor, Neural Architecture | @tdozat | 92% |
| John Bauer | Current Maintainer, Stanford NLP | @AngledLuffa | 95% |
| Christopher D. Manning | Stanford NLP Group Leader | - | 99% |
| Curtis P. Langlotz | Co-author of Biomedical Models Paper | - | 85% |
| Arun Chaganty | Original CoreNLP Client Developer | - | 88% |
| Chloé Kiddon | Co-author Semgrex/Ssurgeon Paper | - | 82% |
| Eric Yeh | Co-author Semgrex/Ssurgeon Paper | - | 82% |
| Alex Shan | Co-author Semgrex/Ssurgeon Paper | - | 82% |

---

## Organizations and Conferences

| Organization/Conference | Full Name | Type | Confidence |
|---|---|---|---|
| ACL | Association for Computational Linguistics | Conference | 99% |
| EMNLP | Conference on Empirical Methods in Natural Language Processing | Conference | 98% |
| NAACL | North American Chapter of the Association for Computational Linguistics | Conference | 97% |
| TLT | Treebanks and Linguistic Theories | Workshop | 88% |
| GURT | Georgetown Roundtable on Languages and Linguistics | Conference | 85% |
| SyntaxFest | A combination conference including TLT and others | Event | 80% |
| Stanford NLP Group | Natural Language Processing research group at Stanford University | Organization | 99% |
| Stanford University | Private research university in California | Institution | 99% |
| ACLANTHOLOGY | Archive of papers from ACL conferences | Repository | 94% |
| arXiv | Preprint archive for research papers | Repository | 99% |
| PyPI | Python Package Index | Repository | 99% |
| GitHub | Version control and collaboration platform | Platform | 99% |

---

## Stanza Components

| Component | Description | Module Location | Confidence |
|---|---|---|---|
| Pipeline | Main interface for chaining NLP processors | `stanza.pipeline.core` | 98% |
| TokenizeProcessor | Handles text tokenization and sentence segmentation | `stanza.pipeline.tokenize_processor` | 97% |
| DepparseProcessor | Performs dependency parsing | `stanza.pipeline.depparse_processor` | 96% |
| PosProcessor | Part-of-speech tagging processor | `stanza.pipeline.pos_processor` | 96% |
| LemmaProcessor | Lemmatization processor | `stanza.pipeline.lemma_processor` | 96% |
| NerProcessor | Named entity recognition processor | `stanza.pipeline.ner_processor` | 96% |
| ConstituencyProcessor | Constituency parsing processor | `stanza.pipeline.constituency_processor` | 95% |
| CorefProcessor | Coreference resolution processor | `stanza.pipeline.coref_processor` | 92% |
| MwtProcessor | Multi-word token processor | `stanza.pipeline.mwt_processor` | 90% |
| MorphsegProcessor | Morphological segmentation processor | `stanza.pipeline.morphseg_processor` | 88% |
| SentimentProcessor | Sentiment analysis processor | `stanza.pipeline.sentiment_processor` | 88% |
| LangidProcessor | Language identification processor | `stanza.pipeline.langid_processor` | 88% |
| Document (Doc) | Core data structure containing processed text | `stanza.models.common.doc` | 98% |
| Sentence | Component of Document with word/token information | `stanza.models.common.doc` | 97% |
| Token/Word | Smallest unit of processed text | `stanza.models.common.doc` | 98% |
| MultilingualPipeline | Pipeline supporting multiple languages simultaneously | `stanza.pipeline.multilingual` | 92% |
| Registry | System for registering and managing processors | `stanza.pipeline.registry` | 88% |
| Trainer | Base class for model training | `stanza.models.common.trainer` | 92% |
| Vocab | Vocabulary management class | `stanza.models.common.vocab` | 94% |
| CharVocab | Character-level vocabulary | `stanza.models.common.vocab` | 88% |

---

## Data Format Terms

| Term | Meaning | Usage | Confidence |
|---|---|---|---|
| CoNLL-U | CoNLL Universal format | Standard annotation format for UD treebanks | 97% |
| conllu | File extension for CoNLL-U formatted files | Data format | 96% |
| TreeBank | Corpus of parse trees for human language | Training data source | 98% |
| Treebank Name | Short identifier like "en_ewt", "en_gum" | Dataset reference | 88% |
| Pretrained Vectors | Word embeddings trained on large corpora | Model initialization | 92% |
| Model Packages | Downloadable trained model files | Runtime dependencies | 93% |

---

## Related Links

- [Stanza Official Website](https://stanfordnlp.github.io/stanza/)
- [Stanza GitHub Repository](https://github.com/stanfordnlp/stanza)
- [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)
- [Universal Dependencies](https://universaldependencies.org/)
- [ACL Anthology](https://aclanthology.org/)
- [Stanza Biomedical Models](https://stanfordnlp.github.io/stanza/biomed.html)

---

## Citation

If using this terminology reference, please cite the original Stanza papers:

- Qi et al. (2020): ACL2020 Stanza system demo paper
- Zhang et al. (2021): Biomedical and clinical English model packages paper
- Bauer et al. (2023): Semgrex and Ssurgeon paper

---

*Last Updated: February 28, 2026*
*Source: Stanza Project Repository*
