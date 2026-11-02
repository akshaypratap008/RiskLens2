## Credit policy
Synthetically generated credit policy covers everything from underwriting standards, governance processes, delegated authorities, portfolio management etc. Since the objective is SME credit assessment only, only certain sectionof the full credit policy to be used as RAG knowledge base to avoid noise and imporve retrieval. The full policy remain the source doc and the extracted knowledge base was treated as domain specific subset for credit assessment. 

## Chunking
Used Docling for chunking so that the tables can be retained. Used HierarchicalChunker initially so that Hierarchy of the sections can also be retained. Will try Hybrid chunker also and check results

## Vector store
Since the credit policy doc is not big, will use chromadb persistent client at the moment. 
If later other poclicy docs are added to the project, will move to Quadrant or other managed vector db
