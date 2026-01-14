# 🧠 Lesson 5: Similarity Search — Finding Relevant Information

> **Goal:** Understand how systems use embeddings to retrieve relevant information, why keyword search often fails, and how simularity search selects the right context for an LLM.

## 🤔 From “Meaning” to “Retrieval”

In [Lesson 5](../lesson-05-embeddings/README.md), we learned how embeddings work:

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

## 👀 Lets See It In Action

Alright, let's walk through a small code example where we can see how keyword search and similarity search work, mainly highlighting the differences between them. After running this, you'll see why keyword search just doesn't cut it in the world of LLMs.

### Getting Started

Before we can interact with OpenAI, you'll need to give the code access to your API key.

If you need help signing up for OpenAI and creating an API key - [follow these instructions](https://platform.openai.com/docs/quickstart)...

Within the `examples` folder you will find a file called `.env.example` - Go ahead and paste your API key in there, rename the file to just `.env` and save!

Also, as with many python based projects, we are probably best to leverage venv - so let's do that! 

From inside the `lesson-06-similarity-search/examples/`:

**Mac OS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Finally, let's install our packages

```bash
pip install -r requirements.txt
```

### The Fun Part

Alright - Let's talk about the code that we have in `examples/search.py`

The code itself runs a couple of different searches; a keyword search and a similarity search.

At the beginning, we load the data contained within `knowledge.txt` into a list of lines:

```python
lines = load_lines(knowledge_path)
```

Each line becomes a chunk that we can search over.

For keyword search, we can see that both the query and the doc are tokenized and then a score is computed based on word overlap with:

```python
q_terms = set(tokenize(query))
d_terms = set(tokenize(doc))
return len(q_terms.intersection(d_terms)) / len(q_terms)
```

So, keyword search baseically asks "How many of the query words appear in this line?"

For similarity search we first cache all the embeddings to disk with:

```python
idx_data = build_or_load_embedding_cache(client, knowledge_path, cache_path, args.model)
```

We also perform checks to see if the `knowledge.txt` file has changed to determine whether or not to "re-cache" everything.

Then, the following lines basically convert the query text to an embedding, compare the query embedding with each lines embedding, and returns a score based on similarity.

```python
q_vec = get_embeddings(client, [query], model=embed_model)[0]
vectors = np.array(idx_data["vectors"], dtype=np.float32)
scored = [(cosine_similarity(q_vec, vectors[i]), i) for i in range(len(lines))]
```

Similarity search answers "How close in meaning is this line with the query?"

So know that we understand a bit about the code, let's go ahead and run it.

### 🟢 Running the code

Let's kick it off

```bash
python3 search.py --text "Best way to recover from malware"
```

This will run both searches on our provided text.  You should see a return similar to the following:

```text
=== Query ===
Best way to recover from malware

=== Keyword Search Results ===
(no matches found)

=== Similarity Search Results ===

#1  score=0.4857  line=6
Use a clean recovery environment to reduce the risk of reinfection during restoration.

#2  score=0.4306  line=2
Safe recovery starts by restoring from known-clean backups, not the most recent backups.

#3  score=0.4061  line=13
Recovery point selection matters: choose a restore point before the intrusion, not just before encryption.

(Cache: knowledge.text-embedding-3-small.cache.json)

Done.
```

As you can see, even though our entire `knowledge.txt` file is full of key insights around recovering from malware, it doesn't actually use those words - so the keyword search comes up with a whopping ZERO results.  Yet our similarity search, well, it scores each line and gives us the closest three matches based on meaning, rather than looking for a specific word.

So, play around, change the text, try each search, see what you can figure out! Maybe try searching for "best way to cook potatoes". The similarity search, even though none of the results really cover off potatoes at all, will still return results, just with lower scores. This is why sometimes models seem to answer confidently, but are completely wrong.

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