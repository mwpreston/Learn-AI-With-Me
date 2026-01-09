# 🧠 Lesson 4: Embeddings — How Meaning Becomes Something a System Can Use

> ***Goal:*** Understand what embeddings are, what they actually look like, how vectors and vector databases fit together, and how embeddings are used to work with documents and past conversations when using an LLM.

🤔 If the Model Can’t Remember… Then What?

In Lesson 3, we hit a hard limit. We learned that:

* Models can only see a fixed number of tokens
* Anything outside that window is invisible
* Long documents and conversations don’t fit

So a very natural question comes up: **If the model can’t remember everything, how do real systems work with lots of data and long conversations?**

The answer isn’t longer prompts or increased context windows.

The answer is **embeddings**.

## 🧠 So, Why Do We Need Embeddings Again? What Problem Do They Solve?

In the real world, we want models to work with more than just the current prompt. We want, and need them to work with things like:

* Documentation
* Policies
* Tickets
* Code
* Logs
* Knowledge bases
* Past conversations

But we can’t keep all of that text in the context window - It's way too big, and the window is much too small!

Embeddings solve this problem by letting us represent meaning in a compact, comparable form. And one that lives outside the context window.

Instead of asking the model to remember everything, we ask a different question:

> What information is most relevant right now?

## 📌 What an Embedding Is

Simply put, an embedding is a numerical representation of the meaning of a piece of text.

Instead of treating text as words and sentences, we convert it into a structured list of numbers that captures what the text is about. What the **meaning** of the text is

In the end, pieces of text with similar meaning produce similar embeddings


### 🔢 What an Embedding Actually Looks Like

Let’s start with a single sentence.

“Ransomware encrypts systems and prevents access to critical data.”

When we generate an embedding for this sentence, we might get something like:

`[ 0.013, -0.227, 0.884, 0.041, -0.562, 0.198, ... ]`

A few important things to notice:

* This list may contain hundreds or thousands of numbers
* Every embedding produced by the same model has the same length
* The individual numbers do not correspond to words or concepts

On its own, this embedding means nothing.

There is no:

* “this number = ransomware”

* “this position = encryption”

* “this part = severity”

So where does the meaning come from?

### 🔁 Embeddings Only Matter When Compared

An embedding becomes useful only when we compare it to other embeddings - by itself, it's pretty much useless.

Remember that first sentence? Let's add a couple more to illustrate how this works...

| Sentence | Embedding |
|----------|----------|
| Ransomware encrypts systems and prevents access to critical data.  | [ 0.013, -0.227, 0.884, 0.041, -0.562, 0.198, ... ]  |
| Recovering data after a malware-driven encryption event.  | [ 0.017, -0.213, 0.871, 0.038, -0.549, 0.204, ... ]  |
| What’s the weather forecast for tomorrow? | [ -0.492, 0.118, -0.031, 0.774, 0.062, -0.901, ... ]  |

Now we can compare them by looking at how far away each embedding number is from the others:

* Sentence 1 ↔ Sentence 2 → very similar
* Sentence 1 ↔ Sentence 3 → very different
* Sentence 2 ↔ Sentence 3 → very different

Even though Sentences 1 and 2 use different words, their embeddings are numerically close.

That’s what we mean when we say embeddings capture meaning.

## 📐 So… What Are Vectors?

To explain comparison, we need one more concept: **vectors**.

I've came across vectors and embeddings, almost sometimes being used interchangeably, the key point to understanding vectors is:

**An embedding is stored as a vector.**

They are not competing ideas.

In essense:

* Embedding → the concept (a representation of meaning)
* Vector → the data structure (an ordered list of numbers)

If it helps, think of it in the same relation as:

* A photo vs a JPEG file
* A song vs an MP3 file

Once created, an embedding is a vector.

### 📍 I'm still confused

Yeah - don't worry - me too!

When digging around I kept seeing examples and definitions that said something along the lines of vectors are a point in a space defined by numbers:

* 2 numbers -> a point on a flat map
* 3 numbers -> a point in 3D space
* 1000 numbers -> a point in high-dimensional space

😕 Clear as mud eh?  This doesn't help at all!

How about this - forget AI, forget LLMs, forget it all.  Let's rank a song by it's characteristics - Say we have the following song...

| Song Name | Sadness | Energy | Tempo | Bass |
|----------|----------|----------|----------|----------|
| Prompt Me Maybe | 3 | 8 | 7 | 2 |

This song is basically represented by the following `[3,8,7,2]`

Let's now add a couple other songs to the mix...

| Song Name | Sadness | Energy | Tempo | Bass |
|----------|----------|----------|----------|----------|
| Prompt Me Maybe | 3 | 8 | 7 | 2 |
| Object Storage of Broken Dreams | 8 | 5 | 3 | 1 |
| Air-Gapped My Heart | 3 | 7 | 7 | 1 |

With these representations we can gather the following:

Prompt me Maybe and Air-Gapped My Heart are similar songs given the closeness of their numbers

[3,8,7,2]
[3,7,7,1]

Object Storage of Broken Dreams and Prompt Me Maybe, not so much the same 

[3,8,7,2]
[8,5,3,1]

You only ever really need to answer the following question to understand what is relative...

**How close is this point to another point?**

Points close together → similar meaning
Points far apart → unrelated meaning

## 🗄️ Where Do These Embeddings Live?

Embeddings do not live in the model’s context window.

They are usually:

* Generated once
* Stored externally
* Compared many times

This brings us to vector databases.

### 🗃️ What Is a Vector Database?

A vector database is a system designed to store large numbers of vectors (embeddings), compare them efficiently using something called a *similarity search* and return the closest matches

It simply answers:

> Which stored embeddings are most similar to this one?

### 📂 What a Vector Database Stores

A typical entry looks like this:

Vector:
  [ 0.013, -0.227, 0.884, ... ]

Metadata:
  text: "Ransomware encrypts systems and prevents access to critical data."
  source: "incident-response-guide.md"
  type: "documentation"


The vector itself is used for similarity comparison - the text is what you eventually pass back to the LLM

## 🔄 How All This Works With an LLM (End-to-End Example)

Let’s walk through a complete example of how this all fits together...

### Step 1: The data for the embeddings is prepared

Documents, notes, or past conversation chunks are broken into pieces. Each piece is then converted into an embedding. These embeddings are stored in a vector database

**Note:** If we are using something like ChatGPT - when we upload a file, this is done automatically for us - no need to even know how.  When we are developing our own application or agent, or simply consuming the LLM through code, we will need to do this manually - Creating chunks with python or javascript, as well as by leveraging common frameworks like LangChain or LlamaIndex. Creating embeddings from the chunks with Cohere or Hugging Face. Then storing in the vectordb using something like Pinecone or Chroma.

### Step 2: A user asks a question

“How do we recover from a ransomware attack?”

Well this part is simple!

### Step 3: Embed the question

The user’s question is converted into an embedding - again, automatically with ChatGPT, manually if using code.

### Step 4: Similarity search

That embedding is compared to stored embeddings.
The database finds the closest matches, such as:

“Ransomware recovery procedures”
“Backup restoration best practices”

Obviously there is much more to this piece, and we will dive into it further in the next lesson.

### Step 5: Retrieve relevant text

Only the associated text is retrieved — not the embeddings themselves.

### Step 6: Pass to the LLM

That text is added to the context window.
The model uses it to answer the question.

This is how embeddings help an LLM!

## 🗣️ What About Past Conversations?

Yes — past conversations can be handled the same way.

The model does not remember them if outside of the context window.

Instead, the application can:

* Embed past conversation turns
* Store them in a vector database
* Retrieve the most relevant past exchanges
* Re-introduce them into context when needed

This is how systems simulate “memory” without breaking context limits.

We’ll go much deeper into this later.

## ⚠️ What Embeddings Still Don’t Do

Even with all this power, embeddings:

❌ Don’t answer questions

❌ Don’t store facts in the model

❌ Don’t validate correctness

❌ Don’t magically give memory to the LLM

They give your system a way to decide what the model should see.

## So with that, let's see it in action

The code we are going to run today is pretty simple - it takes a small set of sentences and converts them into embeddings. It then compares those embeddings for us using cosine similarity (no need to learn this...yet) - this creates a single score that describes how close two pieces of text are in meaning.

It will then print a matrix, showing us how close each sentence is to each other sentence in terms of meaning, and show us each individual sentence with it's closest matched sentence.

At this point, we aren't using any vector databases - we are simply just comparing embeddings to illustrate how it all works...

### Getting Started

Before we can interact with OpenAI, you'll need to give the code access to your API key. 

If you need help signing up for OpenAI and creating an API key - [follow these instructions](https://platform.openai.com/docs/quickstart)...

Within the examples folder you will find a file called `.env.example` - Go ahead and paste your API key in there, rename the file to just `.env` and save!

Also, as with many python based projects, we are probably best to leverage venv - so let's do that! 

From inside the `lesson-04-embeddings/examples/`:

*Mac OS / Linux*

```bash
python3 -m venv .venv
source .venv/bin/activate
```

* Windows PowerShell*
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Finally, let's install our packages
```bash
pip install -r requirements.txt
```

### The Fun Part

Alright, let's go ahead and run the Python
```
python embedding_inspector.py
```

Here's the output I had...

```
=== Sentences ===
1. Ransomware encrypts systems and prevents access to critical data.
2. Recovering data after a malware-driven encryption event is a core part of incident response.
3. What's the weather forecast for tomorrow in Toronto?
4. Backups are only useful if you regularly test restores and verify you can recover cleanly.

=== Embedding Details ===
Embedding model: text-embedding-3-small
Number of embeddings: 4
Embedding dimension: 1536

Sentence 1: Ransomware encrypts systems and prevents access to critical data.
Vector preview (first 10 values): [-0.013, 0.041, 0.023, 0.009, -0.001, -0.042, -0.059, 0.044, -0.028, -0.042, ...]

Sentence 2: Recovering data after a malware-driven encryption event is a core part of incident response.
Vector preview (first 10 values): [0.000, 0.068, 0.024, 0.032, 0.023, -0.008, -0.002, 0.067, 0.011, 0.020, ...]

Sentence 3: What's the weather forecast for tomorrow in Toronto?
Vector preview (first 10 values): [-0.011, -0.016, -0.030, -0.019, -0.014, 0.002, 0.030, -0.030, -0.009, -0.014, ...]

Sentence 4: Backups are only useful if you regularly test restores and verify you can recover cleanly.
Vector preview (first 10 values): [-0.000, 0.029, 0.027, -0.004, 0.023, 0.004, -0.031, 0.026, 0.006, 0.013, ...]

=== Cosine Similarity Matrix ===
           1       2       3       4
   1   1.000   0.514   0.048   0.201
   2   0.514   1.000  -0.032   0.357
   3   0.048  -0.032   1.000  -0.026
   4   0.201   0.357  -0.026   1.000

=== Closest Match For Each Sentence ===

Sentence 1 is closest to Sentence 2 (score=0.514)
- Ransomware encrypts systems and prevents access to critical data.
-> Recovering data after a malware-driven encryption event is a core part of incident response.

Sentence 2 is closest to Sentence 1 (score=0.514)
- Recovering data after a malware-driven encryption event is a core part of incident response.
-> Ransomware encrypts systems and prevents access to critical data.

Sentence 3 is closest to Sentence 1 (score=0.048)
- What's the weather forecast for tomorrow in Toronto?
-> Ransomware encrypts systems and prevents access to critical data.

Sentence 4 is closest to Sentence 2 (score=0.357)
- Backups are only useful if you regularly test restores and verify you can recover cleanly.
-> Recovering data after a malware-driven encryption event is a core part of incident response.

Done.
```

So what do you notice?
Well, I can see one thing - Setence 1 and Sentence 2 are the most closest match out of the 4 - and reading the sentences, that makes sense..
Another odd thing, Look how far away Sentence 3 is from the rest of them, even returning negative numbers - yeah, ransomware doesn't care about Toronto's forecast that's for sure!

The code itself is using OpenAI to create the embeddings for us, we can see that in the `client.embeddings.create` command in the `get_embeddings` function
We are using the NumPy library to do the match and the cosine similarity calculations - it's just easier :)

#### Let's have some fun

Feel free to play around here with the sentences and see how the similarity search reacts - it's quite interesting.

For example, I ran with the following:

```python
SENTENCES: List[str] = [
    "The concert was cancelled due to rain",
    "Severe weather forced the event to be called off",
    "I saw the man through the telescope.",
    "I saw the man who had a telescope.",
]
```

and got the following:

```
Sentence 1 is closest to Sentence 2 (score=0.610)
- The concert was cancelled due to rain
-> Severe weather forced the event to be called off

Sentence 2 is closest to Sentence 1 (score=0.610)
- Severe weather forced the event to be called off
-> The concert was cancelled due to rain

Sentence 3 is closest to Sentence 4 (score=0.855)
- I saw the man through the telescope.
-> I saw the man who had a telescope.

Sentence 4 is closest to Sentence 3 (score=0.855)
- I saw the man who had a telescope.
-> I saw the man through the telescope.
```

Sentence 3 and 4 are closer than 1 and 2?  I wouldn't expect this, but LLMs and software really have trouble with ambiguous content. As humans, our brains understand that seeing a man through a telescope and seeing a man with a telescope are two very different things.

Embeddings a great at capturing *typical meaning*, but not so much at resolving ambiguous interpretations!

Swap up some of the sentences and have some fun!!!

## 🧠 Final Reset: How all the pieces we've learned so far fit

Tokens → how text is processed
Context window → how much text the model can see
Embeddings → representations of meaning
Vectors → how embeddings are stored
Vector databases → how embeddings are searched
LLMs → generate responses using selected text

Each has a specific job.

## 📝 Lesson 4 Takeaways (Lock These In)

Before moving on, you should be comfortable with these ideas:

* 🔢 Embeddings represent meaning numerically
* 📐 Embeddings are stored as vectors
* 📍 Similar meaning = vectors close together
* 🗄️ Vector databases store and search embeddings
* 🔄 LLMs use retrieved text, not embeddings directly
* 🗣️ Past conversations can be embedded and retrieved by the application

If this feels clearer than before — that’s the point.

## 👀 Looking Ahead

In the next lesson, we’ll make this real:

Lesson 5: Similarity Search — actually finding relevant information using embeddings.

This is where the theory turns into something you can build.