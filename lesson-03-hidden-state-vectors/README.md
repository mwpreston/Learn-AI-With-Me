# 🧠 Lesson 3: Hidden State. What the Model Is Thinking *Right Now*

> **Goal:** Understand what a hidden state is, how a language model represents meaning internally while reading tokens, and why this internal state is temporary, inaccessible, and different from embeddings.

---

## 🤔 We Know the Model Reads Tokens… But Then What?

In [Lesson 2](../lesson-02-tokens/README.md), we learned that:

* Text is broken into tokens.  
* Tokens are what the model actually reads  
* The model predicts what comes next, one token at a time  

That naturally leads to a very reasonable question:

> **As the model reads tokens, how does it keep track of what’s going on?**

It’s clearly not just looking at the *last* token in isolation.

This is where **hidden state** comes in.

## 🧠 What Is a Hidden State?

A **hidden state** is the model’s internal representation of everything it has seen *so far*.

It’s how the model keeps track of:

* The topic  
* The intent  
* The structure of the response  
* The relationships between earlier and later tokens  

At a high level:

> **The hidden state is “what the model currently understands” at a given moment in time.**

You never see it, you never store it, and you never retrieve it.  

But it's there. It exists during generation, and it’s doing all the work.

## 🔁 The Core Loop

Every modern language model runs this loop repeatedly:

1. Read the next token
2. Update the hidden state
3. Use the hidden state to predict the next token

Then it repeats - over and over - one token at a time until it's complete.

### An Example

Let's say the model sees the following prompt:

> "How can a midsize company protect against ransomware?"

Remember - the model doesn't see this as a sentence, but rather a sequence of tokens, left to right, maybe something like:

`["How", " can", " a", " midsize", " company", " protect", " against", " ransomware", "?"]`

Therefore, this may get processed as follows:

1. The first token is read `How`. At this point, hidden state may reflect the following:

    * Intent: Question

2. We now see the next token ` can`. Again, the model may now recognize that this is a request for guidance, updating hidden state again

    * Intent: Advice/Best Practices

3. As we continue, we see `a midsize company`. And again, hidden state is updated

    * Intent: Advice/Best Practices
    * Audience: Midsize Company
    * Constraints: Not a startup, not a massive enterprise

4. And so on with ` protect`

    * Intent: Advice/Best Practices
    * Audience: Midsize Company
    * Constraints: Not a startup, not a massive enterprise
    * Domain: Security

5. Again, we now have ` against`

    * Intent: Advice/Best Practices
    * Audience: Midsize Company
    * Constraints: Not a startup, not a massive enterprise
    * Domain: Security
    * Threat Framing: Defensive Posture
    * Expectation: A specific risk or adversary might be coming

6. And finally ` ransomware`

    * Intent: Advice/Best Practices
    * Audience: Midsize Company
    * Constraints: Not a startup, not a massive enterprise
    * Domain: Cybersecurity
    * Threat Framing: Defensive Posture
    * Topic: Ransomware
    * Sub Topics: Backup, Recovery, Incident Response

The model will then use this hidden state as it generates answers (tokens), one by one, updating it after each and every token generation.

***NOTE:*** We have represented hidden state here as text, but in reality, it's just a bunch of numbers, like a lot of them! It could contain up to hundreds or thousands of values that the model uses to compare and contrast when selecting the next token.

## ⚠️ Hidden State Is Temporary

This is one important fact to remember. Hidden state only exists while the model is running!

Once the response has been generated the hidden state is discarded - nothing is stored and nothing is remembered.

When we begin a new prompt, a brand new hidden state is created and model begins from scratch.

## No Code Today

Remember hidden state is temporary and is internal to the model, so writing code to help illustrate it doesn't really make sense.

Even if we could see it, it would simply be a series of numbers that means nothing to us but everything to the model.

So, no homework tonight kids!

## 📝 Lesson 3 Takeaways

Before moving on, you should be comfortable with these ideas:

* 🧠 Hidden state represents what the model understands so far
* 🔁 It is updated after every token
* ⏳ It exists only during generation
* ❌ It is not memory and cannot be stored
* 🧱 It is influenced only by tokens inside the context window

👀 Looking Ahead

You may be wondering what I meant when I mentioned Context Window above. In the [next lesson](../lesson-04-context/README.md), we will discuss exactly that.

* Why models forget
* Why long conversations break down
* Why “just add more text” doesn’t work

Hidden state explains how the model understands.

Context explains what it’s allowed to understand.
