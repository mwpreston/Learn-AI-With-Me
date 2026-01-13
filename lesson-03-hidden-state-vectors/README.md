# 🧠 Lesson 3: Hidden State. What the Model Is Thinking *Right Now*

> **Goal:** Understand what a hidden state is, how a language model represents meaning internally while reading tokens, and why this internal state is temporary, inaccessible, and different from embeddings.

---

## 🤔 We Know the Model Reads Tokens… But Then What?

In [Lesson 2](../lesson-02-tokens/README.md), we learned that:

* Text is broken into tokens  
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
    * Domain: Cyber Security
    * Threat Framing: Defensive Posture
    * Topic: Ransomware
    * Sub Topics: Backup, Recovery, Incident Response

The model will then use this hidden state as it generates answers (tokens), one by one, updating it after each and every token generation.