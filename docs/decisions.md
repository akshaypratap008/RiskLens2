## Credit policy
Synthetically generated credit policy covers everything from underwriting standards, governance processes, delegated authorities, portfolio management etc. Since the objective is SME credit assessment only, only certain sectionof the full credit policy to be used as RAG knowledge base to avoid noise and imporve retrieval. The full policy remain the source doc and the extracted knowledge base was treated as domain specific subset for credit assessment. 

## Chunking
Used Docling for chunking so that the tables can be retained. Used HierarchicalChunker initially so that Hierarchy of the sections can also be retained. Will try Hybrid chunker also and check results

## Vector store
Since the credit policy doc is not big, will use chromadb persistent client at the moment. 
If later other poclicy docs are added to the project, will move to Quadrant or other managed vector db

## Evals
used deepeval
to create a golden dataset, used claude with the below prompt
```
I am building a rag for this credit policy document. The rag agent will be used by credit analyst and other agents in the project to asses credit risk for a company. To evaluate the rag, I will be using deepeval. To evaluate the retriever, I will be using contextual precision and contextual recall based on deepeval documentation. I need a LLM test case which should include input (user query) and actual output(the real answer from the credit policy). 

Can you build a LLM test case with 20 questions for me. Make sure the questions are realistic from a credit analyst perspective. Strictly make sure that the actual output is from the credit policy document provided.
```