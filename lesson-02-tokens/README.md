# 🧩 Lesson 2: Tokens - What the Model Actually Sees

> **Goal:** Understand what tokens are, why language models use them, and why tokens explain things like weird wording, context limits, and cost!

👋 Hey There - Remember waaaaay back in [Lesson 1](../lesson-01-foundations/README.md) when we said this:
> A language model predicts the next piece of text based on everything that came before it.

In this lesson, we'll answer a super important follow-up question that you probably had
> What does the model consider a "piece of text"?

The answer is: **tokens**

## 🧠 First, Why Tokens Exist At All

As a human, you probably think in:

* Words
* Sentences
* Ideas

Language models don't.

Internally, models work with **numbers**, not text.
So before a model can do anything useful, the text we send it needs to be turned into something numerical.

Tokens are a bridge between Human-readable text and Machine-readable numbers!

## 🛑 Hard Stop - WTH Does That Even Mean - Like, What's A Token?

Okay, okay - let's just get to the point - A token is a small chunk of text that the model works with internally.

So, with that, a token could be:

* A whole word
* Part of a word
* A space
* Punctuation
* A short sequence of characters
* or a mixture of all the above...

The most important part to remember: tokens are not words

Sometimes one word = one token
Sometimes one word = several tokens
Sometimes several words = one token

## ✂️ How Text Gets Broken Down

Let's take the following simple sentence
> "Explain how backups protect against ransomware"

Our models don't see this as a sentence.

It sees something more like the following (not exact):

```text
"Explain" | " how" | " backups" | " protect" | " against" | " ransomware" | "."
```

Each of those chunks is a token.

A few things to note here:

* Spaces often belong to the token/text that follows
* Common words tend to be single tokens
* Longer or less common words may be split up

The exact splitting depends on the tokenizer, but the idea always stays the same!

😕 Tokenizer?  Huh? Again! WTH?!?!

Yeah, tokenizers basically define how the text is chopped into tokens. Different models will use different tokenizers. So, depending on the tokenizer, the same sentence can become different token sequences.

Some of the most common tokenizers are:

1️⃣ Word-Based - These are old, mostly obsolete - sort of work on a one to one mapping of words to token (IE: "ransomware" becomes ["ransomware"])
2️⃣ Subword-Based - This is mostly what see in popular LLMs today. They split text into frequently occurring pieces. (IE "ransomware" becomes ["ransom","ware"] OR "ransomware" becomes ["rans","om","ware"])
3️⃣ Byte-Level - These tokenizers operate on the byte level, so any text is can be tokenized (IE "ransomware" becomes ["ra","nsom","w","a","re"])

Which one is used does matter. It has the implication to affect any limits and/or costs incurred, increase/decrease sensitivity of wording in prompts, and much more - but the main takeaway here is **1 token <> 1 word**

## 🔢 From Tokens to Numbers

Once we have our tokens, each token is then mapped to a number.

For example:

```text
" backups"  →  18472
" ransomware" → 27891
"." → 30
```

At this point, our models are no longer working with text, instead, they work with the sequences of numbers.

It's these numbers that the LLM uses to:

* Recognize patterns
* Determine and estimate probability
* Generate what comes next.

These numbers are then translated into something called embeddings - but that's out of scope for this lesson - we will cover that in [Lesson 4](../lesson-04-embeddings/README.md)

## 🔁 How This All Connects Back to Lesson 1

In Lesson 1, we said:
> The model predicts what comes next, and more than one continuation/prediction can make sense

Now we can be a bit more precise and say:

* The model predicts the next **token**
* It does this one token at a time
* Each choice influences the next one - yeah, like the butterfly effect

Even a small change early on in the response can cascade into complete different phrasing, a complete different structure, or slightly different emphasis([think Christopher Walken introducing the Foo Fighters](https://www.youtube.com/shorts/JGGsft6zq4k)).

The answers feel consistent in meaning, but not in wording!

## ⚠️ Why Tokens Matter More Than You Expect

Understanding tokens really does help explain a lot of real-world behavior we see when interacting with LLMs.

1️⃣ Context Limits

Models can only “see” a limited number of tokens at once.

That limit includes:

* Your prompt
* System instructions
* Conversation history
* The model’s own previous output

Long prompts don’t fail because they’re long in words. They fail because they exceed the token limit. The [next lesson](../lesson-03-context/README.md) will explore these context limits in more detail.

2️⃣ Cost

Most AI APIs charge based on:

* Input tokens
* Output tokens

Not characters.
Not words.

Two prompts that look similar to you may cost very different amounts depending on how they tokenize.

3️⃣ Weird Splits and Odd Behavior

Ever noticed:

* Strange word breaks?
* The model handling punctuation “oddly”?
* Small wording changes producing different results?

That’s often explained by token boundaries and limits.

The model isn’t confused. It’s just operating at a level that is much different from the way you and I do.

## 📺 Seeing Tokens For Yourself

In the practical section of this lesson we will visually see how our text is broken down into tokens. Within the `examples` folder, you'll see a small script that:

* Takes a piece of text
* Runs it through a few different tokenizers
* Prints out the details

While this is honestly not something we would normally need to do, it's still cool to see.

So with that, let's get started...

### Getting Started

No need to configure an OpenAI key for this lesson - we are simply using the `tiktoken` library to tokenize our text, rent free!

Also, as with many python based projects, we are probably best to leverage venv - so let's do that!

From inside the `lesson-02-tokens/examples/`:

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

Finally, let's install our required packages - in this case, just tiktoken.

```bash
pip install -r requirements.txt
```

### Now, The Code

Let's dive into some code in the `tokenize_text.py` file, so we understand it...

First, we see a couple variables getting initialized

```python
TEXT = "In one or two sentences, what’s the best way to protect against ransomware?"

TOKENIZERS = {
    "cl100k_base (modern GPT models)": "cl100k_base",
    "p50k_base (older GPT-3.5 era)": "p50k_base",
    "r50k_base (very old / GPT-2 style)": "r50k_base",
}
```

We have `TEXT` - this is our prompt

And we have an array of 3 different tokenizers cleverly called `TOKENIZERS`. Here we are using cl100k_base, p50k_base, and r50k_base.

Each of these tokenizers was designed for a different generation of models.

They all do the same job — split text into tokens — but they:

* Use different vocabularies
* Make different assumptions about common patterns
* Split text in slightly different ways

We can also see this function:

```python
def visualize_whitespace(text: str) -> str:
    return (
        text.replace(" ", "␠")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
    )
```

This code basically replaces any whitespace with some characters, so we can actually see that things like spaces are indeed included within the token.

And finally, we run the text through the various tokens using the following:

```python
for label, encoding_name in TOKENIZERS.items():
    encoding = tiktoken.get_encoding(encoding_name)
    token_ids = encoding.encode(TEXT)
```

And of course, print out some results - so with that, let's run it!

```bash
python3 tokenize_text.py
```

See anything interesting? Here's my output

```text
Original text:
In one or two sentences, what’s the best way to protect against ransomware?
================================================================================

Tokenizer: cl100k_base (modern GPT models)
Encoding name: cl100k_base
Token count: 17
--------------------------------------------------------------------------------
  1. 'In'
  2. '␠one'
  3. '␠or'
  4. '␠two'
  5. '␠sentences'
  6. ','
  7. '␠what'
  8. '’s'
  9. '␠the'
 10. '␠best'
 11. '␠way'
 12. '␠to'
 13. '␠protect'
 14. '␠against'
 15. '␠ransom'
 16. 'ware'
 17. '?'
--------------------------------------------------------------------------------

Tokenizer: p50k_base (older GPT-3.5 era)
Encoding name: p50k_base
Token count: 18
--------------------------------------------------------------------------------
  1. 'In'
  2. '␠one'
  3. '␠or'
  4. '␠two'
  5. '␠sentences'
  6. ','
  7. '␠what'
  8. '�'
  9. '�'
 10. 's'
 11. '␠the'
 12. '␠best'
 13. '␠way'
 14. '␠to'
 15. '␠protect'
 16. '␠against'
 17. '␠ransomware'
 18. '?'
--------------------------------------------------------------------------------

Tokenizer: r50k_base (very old / GPT-2 style)
Encoding name: r50k_base
Token count: 18
--------------------------------------------------------------------------------
  1. 'In'
  2. '␠one'
  3. '␠or'
  4. '␠two'
  5. '␠sentences'
  6. ','
  7. '␠what'
  8. '�'
  9. '�'
 10. 's'
 11. '␠the'
 12. '␠best'
 13. '␠way'
 14. '␠to'
 15. '␠protect'
 16. '␠against'
 17. '␠ransomware'
 18. '?'
--------------------------------------------------------------------------------
```

As we can see, we get a different number of tokens depending on which tokenizer we use - and as we described earlier, this can have a drastic effect on not only token limits, but also cost when using this at scale...

At this point, you don’t need to memorize token rules — you just need to recognize when token behavior is influencing what you see - so an understanding that tokens aren't words, tokens are...tokens - that's it! <- This is the main message of this lesson!

## 📝 Lesson 2 Takeaways (Lock These In)

Before moving on, you should be comfortable with these ideas:

* 🔢 Models don’t see words, they see tokens
* ✂️ Tokens are chunks of text, not whole ideas
* 🔁 Models generate output one token at a time
* 📏 Context limits are measured in tokens
* 💰 Cost is usually based on tokens

If this all still feels a bit foreign, that’s okay - After the first 4 or 5 lessons things will start to click - but it's best to break this down, and understand each concept on its own - it will click for you - I promise!

## 👀 Looking Ahead

In the [next lesson](../lesson-03-hidden-state-vectors/README.md), we'll explore hidden state - the secret helper models have to help understand intent and generate answers
