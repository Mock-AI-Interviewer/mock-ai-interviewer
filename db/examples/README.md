# Database Schema Examples

This directory contains examples of JSON NoSQL Schema files.
Different files represent 1 or more documents that would go into mongo db collection
The different collections currently are:

- **Interview Types**
  - A collection of documents showing the different interview types as well as other associated metadata
- **Conversation History**
  - The conversation history of a single interview
  - References the interview type directly and stores a copy of the interview type inside it
