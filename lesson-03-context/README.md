# 🧠 Lesson 3: Context Windows — Why AI Forgets

> **Goal:** Understand what a context window is, what fits inside it, and why exceeding it leads to forgotten details, ignored instructions, and degraded responses.

A while back I was in a pinch to complete a project that involved quite a bit of configuration and coding on both a platform that I was unfamiliar with and a programming language I've never used - needless to say, ChatGPT was a godsend in walking me through syntax and configurations well into the wee hours of the morning 

That is, until I hit an error, and needed to go back to reconfigure something we'd already configured a few hours before that - but the LLM had no idea what I was talking about - and of course, it didn't really tell me that - instead, just started making up a bunch of stuff that sounded great, but I knew was wrong...

🤔 “But I Already Told You That…” - I can clearly remember prompting this multiple times...

If you’ve spent any time chatting with an LLM, you’ve probably had this experience:

You explain something carefully
The model responds correctly
After repetition may times, it forgets
Or contradicts itself
Or ignores earlier instructions

It feels like it's literally lost its memory, but it is not that...

It’s something much simpler. It involves the amount of information that a model can see and/or understand at once.

To help illustrate this, we really need to understand what the model actually "sees".

## 🧠 What the Model Can Actually See

A language model does not have access to:

* Your entire conversation history
* Previous chats
* Long-term memory
* Anything outside the current interaction

So what does it have access to? Basically, a fixed window of tokens

That window is called the **context window**.

## 📦 What Is a Context Window?

At its very core, a context window is just the maximum number of tokens that the model is able to consider when generating a response.

A context window includes everything the model is given:

* System instructions
* Your prompt
* Conversation history
* Retrieved documents
* The model’s own previous output

If something doesn’t fit inside that window the model **cannot** see it.

Not partially, not kind of - it's gone!

## 🔢 Sounds terrible - so how big are these context windows?

Well, like many other answers to many other questions related to IT the response is  **It Depends**

Different models support different context window sizes, and those limits can change over time. As a ballpark, many modern general-purpose language models support context windows on the order of tens of thousands of tokens.

So how much is tens of thousands of tokens?  Well:

* A few thousand tokens ≈ a couple pages of text
* Tens of thousands of tokens ≈ a short technical document or a long conversation

Remember from the previous lesson when we talked about tokens - one of the main takeaways was **tokens are not words**

That's why back and forth conversations that appears to be *small* can actually be much larger than you would expect once it's tokenized.

The key takeaway here is to really ignore the hard number, just know that once a context window has exceeded its token limit, things start to get... weird...

## 🧯 So What Actually Happens When the Context Window Fills Up

Yeah, so, when these things actually fill up - what happens?

Well, let's start by saying what doesn't happen

The model doesn't warn you, it doesn't slow down, and it doesn't make any guesses around what might be important to save...

Instead - Older tokens are simply removed or purged to make room for new ones.

What gets dropped depends on the system managing the conversation, not the model itself. In many cases, this means:

* Early instructions disappear
* Initial constraints vanish
* Important background information silently falls out of view

From the model’s perspective, that information simply no longer exists.

This explains why models can often contradict answers that they gave you earlier, or feel like they are hallucinating, making things up.  

So many times I instruct an LLM to not give me those dang emm dashes - but low and behold, after an hour or so of going back and forth, it starts spitting them out again.

Or it loses context as to what I was even talking about from the beginning!

The odd bit though, the responses still appear very confident, even though they are wrong - the answers still *look* good!

The models are not changing their mind (or losing it), they’re just now working with incomplete information.

### 🧠 A Critical Insight

When learning about context windows, I had this assumption which I'm sure many others will have as well - “Surely the model knows what matters from our past conversations - can't I just tell it that something is important?”

But the opposite is true. Models have no idea what matters - and while I can say something is important, once that instruction falls out of the context window, it really doesn't matter.

It has no concept of priority across time, it only knows what it can see within that window

Presence matters, order matters, recency matters.

That's it! Importance does not.

### 🔁 The Long Conversations Dilemma

Every response the model generates:

* Adds new tokens
* Pushes older tokens further back
* Consumes part of the available context

Over time, this creates a sliding window effect.

This is why long chats feel like they get worse over time. Early agreements and instructions disappear, and you end up having to re-prompt, or repeat yourself

This isn’t a bug.

It’s just how the system works.

## 🔗 Connecting Back To Tokens (Lesson 2)

This is exactly why Lesson 2 mattered.

Context limits are **measured in Tokens**, not words, not characters

Two prompts that look similar can have very different token counts - which in turn will have very different outcomes.

Once you exceed the context window, behavior changes.

## ❓ Common Questions I Had At This Point

These questions tend to come up naturally here. Let's answer them briefly and come back to them later in the series.

**❓ Can I control what stays in the context window?**

Not directly.

Language models don’t have a built-in notion of memory or pinned information. Anything that “persists” across turns is managed outside the model by the system using it.

There are several architectural approaches to handling this such as embeddings, which we’ll explore in the [next lesson](../lesson-04-embeddings/README.md).

**❓ Why do some chat applications seem to remember more than the raw limit?**

Because that chat application is doing all the extra work to make sure the models know what's up.

Many systems summarize, compress, or selectively re-introduce information behind the scenes to stay within limits. The model itself isn’t remembering. It's just being reminded with a short, contextual overview.

We’ll dig into how and why systems do this when we talk about memory, agents, and deployment.

**❓ So how do people actually build around context limits?**

They don’t rely on longer prompts.

In practice, systems solve this by:

* Deciding what information belongs in context
* Representing information outside the model
* Bringing only the most relevant pieces back in when needed

There are multiple ways to do this, each with different trade offs. We’ll cover them in upcoming lessons.

## 🧭 Reframing the Problem

At this point, it’s worth resetting expectations:

Context limits are not something you “work around with better prompts.”
They’re something you design around with better models or systems.

## Wait, No Code This Lesson?

Context windows are a hard constraint of the model. While it’s technically possible to exhaust a real context window programmatically, doing so would be expensive, slow, and dependent on model-specific limits that change over time.

More importantly, simulating this behavior in code often adds complexity without improving understanding. What matters is the mental model: when information falls outside the context window, the model cannot see or use it.

In later lessons, we’ll focus on practical techniques and architectures that design around this limitation, where code examples provide much more value.

## 📝 Lesson 3 Takeaways

Before moving on, you should be comfortable with these ideas:

* 📦 Models can only see a fixed number of tokens at once - this fixed number is called a Context Window
* 🧠 Anything outside the context window is invisible
* 🔁 Long conversations push old information out
* ⚠️ Forgetting is a structural limitation, not a bug
* 🏗️ Context problems require system design, not better prompts

## 👀 Looking Ahead

In the [next lesson](../lesson-04-embeddings/README.md), we’ll explore embeddings - how meaning can be represented outside the context window, and how systems decide what information is worth bringing back in.

This is where we stop trying to fit everything into context…
and start getting intentional about what belongs there.
