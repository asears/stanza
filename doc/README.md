# CoreNLP Protocol Buffers Documentation

This directory contains protocol buffer definitions for interfacing with Stanford CoreNLP and related NLP tools.

## CoreNLP.proto

The `CoreNLP.proto` file defines the protocol buffer schema for serializing and deserializing NLP annotations between Stanza and Stanford CoreNLP. This enables efficient binary communication and data exchange.

### Building the Protocol Buffers

#### For Python (Stanza)

From the repository root, regenerate the Python protocol buffer code:

```bash
protoc -I=./doc --python_out=./stanza/protobuf ./doc/CoreNLP.proto
```

This generates `stanza/protobuf/CoreNLP_pb2.py`, which is used by Stanza's CoreNLP client interface.

#### For Java (CoreNLP)

From the CoreNLP repository (JAVANLP_HOME):

```bash
protoc -I=src/edu/stanford/nlp/pipeline/ --java_out=src src/edu/stanford/nlp/pipeline/CoreNLP.proto
```

This generates the corresponding Java classes for CoreNLP.

### Java Dependencies

To work with Stanford CoreNLP or compile the Java protocol buffers, you need:

- Java Development Kit (JDK) 8 or later
- Protocol Buffers compiler (protoc)

#### Java Distribution Options

While Oracle JDK is an option, there are several excellent open-source and commercially-supported alternatives:

- [Microsoft OpenJDK](https://learn.microsoft.com/en-us/java/openjdk/download) - Microsoft's build of OpenJDK with long-term support
- [OpenJDK](https://openjdk.org/) - The official open-source Java reference implementation
- [Eclipse Temurin (Adoptium)](https://adoptium.net/) - High-quality, TCK-certified OpenJDK builds from the Eclipse Foundation
- [Red Hat OpenJDK](https://developers.redhat.com/products/openjdk/download) - Enterprise-grade OpenJDK from Red Hat
- [Ubuntu OpenJDK Toolchains](https://ubuntu.com/toolchains/java) - Pre-packaged OpenJDK for Ubuntu systems
- [Azul Zulu](https://www.azul.com/downloads/#zulu) - Certified OpenJDK builds with commercial support options

All of these distributions are compatible with Stanford CoreNLP and protocol buffer compilation.

### Protocol Buffer Installation

Install the Protocol Buffers compiler:

**Ubuntu/Debian:**
```bash
sudo apt-get install protobuf-compiler
```

**macOS (Homebrew):**
```bash
brew install protobuf
```

**Windows:**
Download pre-built binaries from the [Protocol Buffers releases page](https://github.com/protocolbuffers/protobuf/releases).

**Python package (for development):**
```bash
pip install protobuf
```

### Usage in Stanza

The generated protocol buffer classes are used internally by Stanza's CoreNLP client to:

- Serialize documents for Stanford CoreNLP server requests
- Deserialize annotated documents from CoreNLP responses
- Exchange structured NLP data efficiently between Python and Java

See `stanza/server/client.py` and related modules for implementation details.

### Schema Overview

The protocol buffer schema includes definitions for:

- `Document` - Complete document annotation
- `Sentence` - Sentence-level annotations with tokens and parse trees
- `Token` - Word-level features (POS tags, NER, lemmas, etc.)
- `DependencyGraph` - Dependency parse representations
- `CorefChain` - Coreference resolution chains
- `ParseTree` - Constituency parse trees
- Various specialized structures for NER, relations, semantic roles, and more

Refer to `CoreNLP.proto` for the complete schema definition and field descriptions.
