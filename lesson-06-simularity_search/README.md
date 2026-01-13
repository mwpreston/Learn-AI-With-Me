# 🧠 Lesson 5: Similarity Search — Finding Relevant Information

> **Goal:** Understand how systems use embeddings to retrieve relevant information, why keyword search often fails, and how simularity search selects the right context for an LLM.

## 🤔 From “Meaning” to “Retrieval”

In [Lesson 4](../lesson-04-embeddings/README.md), we learned how embeddings work:

* Text is converted into embeddings
* Similar meaning produces similar vectors
* Embeddings can be compared numerically

That answers how meaning is represented.

But it doesn’t answer the next, more practical question:

> How does a system actually find the right information to show the model?

That’s the job of **similarity search**.

## 🔍 What Similarity Search Actually Does

Similarity search answers one simple question: **Given a piece of text, which stored pieces of text are most similar in meaning?

It doesn't
* Generate the answers or next text
* Validate any correctness
* Ensure things are factual or apply reasoning

It simply just ranks stored text by symantic relevance.

## 📦 What Are We Searching?

It's important to understand what exactly we are searching for.

When we perform similarity search, we are searching embeddings, or in other words, our own data. For this lesson, we will similarity search against a text file, but in the real world, this data could be:

* Documentation or runbooks
* Knowledge Base articles
* Notes
* Past conversation summaries

Each line basically represents a small, self contained idea with meaning.

## ❌ Why Keyword Search breaks down

Since the age of the internet, we've always used keyword search - where systems attempt to return results based on matched words.

This works great when we know the exact terminology to search for, wording is consistent across our sources, and queries are precise about what they are looking for.

But real, everyday questions don't follow adhere to these constraints

For example if we were to say "How do we restore systems after they've been encrypted by malware?"

While we may have relevant content that says things like:

* Recoverying from ransomware
* Restoring from clean backups
* Validating our recovery points

Keyword search may miss the above entirely, there are no overlapping words to match on.

The data is there.
The words just don't line up.

## 🧠 How Similarity Search Is Different

Similarity search doesn't compare text - it compares embeddings

And because embeddings capture meaning, I suppose we can say it compares meanings.

This means:

* Paraphrases still match
* Synonyms still connect
* Different wording still returns results

This is the payoff of similarity search and embeddings.

## ⚙️ So What Does Similarity Search Do and Not Do?

It's important to understand where exactly similarity search starts and ends within this entire process.

Earlier, we said it doesn't generate answers - and that's correct - it simply returns the text that the LLM needs to generate answers.

Let's look at the process again

First, we supply our application with some text - that text is broken down into chunks, embeddings are generated, and stored alongside the text in some sort of database. This is done once!

Second, we prompt the LLM or ask a question...

That question or prompt is itself turned into an embedding, and then compared to those that we stored initially. This is where similarity search happens. Scores are calculated and results are ranked.

The top n number of results are returned - these results are then also passed to the LLM via Context and the LLM generates an answer using the results.



## 📝 Lesson 5 Takeaways

Before moving on, you should be comfortable with these ideas:

* 🔍 Similarity search retrieves relevant text, not answers
* 🧠 It compares embeddings, not words
* 📦 Search operates over your own data
* ❌ Relevance ≠ correctness
* 🧩 Good retrieval is critical for good answers

## 👀 Looking Ahead

In the next lesson, we’ll connect retrieval and generation and explain exactly how Retrieval-Augmented Generation or RAG fits in.

This is where everything you’ve learned so far comes together.