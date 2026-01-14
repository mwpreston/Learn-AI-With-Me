# 🤖 Learn AI with Me

👋 Hi There!  I'm Mike and as of writing this I know very little about AI. But that's about to change...I hope!

Backstory - After a solid year of going back and forth with ChatGPT I noticed that these LLMs were getting better, producing significantly more accurate content. It was at this point I figured I better learn how this is all working, as it's honestly, beginning to accomplish more and more things that I do on a daily basis, but faster, and most the time, better!

💡 This is where I realized I have no idea how this stuff works, no idea what is happening underneath the hood - and being such a complex topic, I honestly don't know if I ever will - but that isn't going to stop me from trying!

Which leads me to now and this series - This repository, once completed, will contain a from-scratch, hands-on learning series designed to help practitioners understand how modern AI systems work, not just how to call an API or simply prompt ChatGPT

The goal of this series is simple:

🎯 Go from “I know nothing about AI” → “I can confidently build an AI agent and understand how it 'reasons'”

Each lesson will build on the previous one, combining:

* 🧠 Explanations of the concept
* 💻 Runnable code examples
* 🛠️ Practical exercises you can do on your own

No prior AI background is required. Which is obvious, because I have none - so let's learn this together!

## 📁 How This Repository is Organized

The repository is structured as one folder per lesson, in learning order.

```text
/
├── README.md
├── lesson-01-foundations/
├── lesson-02-tokens/
├── lesson-03-hidden-state-vectors/
├── lesson-04-context/
├── future_lessons
```

Each lesson is self-contained and will typically include:

```text
lesson-XX-lesson-name/
├── README.md          # 📘 Lesson explanation (theory + mental models)
├── examples/          # 💻 Runnable code samples
├── images/            # 🏋️ Images
```

Feel free to work through lessons sequentially, or jump to a specific topic if you already have some background. I really don't care :)

## 📚 What This Series Covers

You will see this get updated as new lessons are created - For now, this is what we've got!

* 🧠 [Lesson 1 - Foundations](lesson-01-foundations/README.md) -> Understand, at a high level, how LLMs actually work - and why even when we send the same prompt, we get different answers - all that seem to make sense...
* 🔤 [Lesson 2 - Tokens](lesson-02-tokens/README.md) -> Understand what tokens are, why language models use them, and why tokens explain things like weird wording, context limits, and cost!
* 🏡 [Lesson 3 - Hidden State](lesson-03-hidden-state-vectors/README.md) -> Understand how the model track meaning and why that is important.
* ✍️ [Lesson 4 - Context Windows](lesson-04-context/README.md) -> Understand what a context window is, what fits inside it, and why exceeding it leads to forgotten details, ignored instructions, and degraded responses.
* ❓ [Lesson 5 - Embeddings](lesson-05-embeddings/README.md) -> Understand what embeddings are, what they actually look like, how vectors and vector databases fit together, and how embeddings are used to work with documents and past conversations when using an LLM.
* 🔍 [Lesson 6 - Similarity Search](lesson-06-simularity_search/README.md) -> Understand the differences between keyword and similarity search and why the latter is the chosen method for AI applications.

## 🚀 How to Use This Repo

Recommended approach:

* ▶️ Start with Lesson 1
* 📖 Read the lesson README
* 💻 Run the examples locally
* 🧪 Modify the code and break things
* ➡️ Move on when the concepts feel intuitive

You don’t need to memorize anything. There is no test at the end. The focus is really all about understanding why things behave the way they do.

## 🧰 Prerequisites

* 🧑‍💻 Basic familiarity with programming concepts
* 🔑 API access into an LLM - I'll be using OpenAI
* 🐍 Python (used in most examples)
* 🤔 Curiosity and willingness to experiment

Specific setup instructions (virtual environments, dependencies, API keys, etc.) are included inside each lesson folder.

## 👥 Who This Is For

This series is aimed at:

* ☁️ Cloud and platform engineers
* 🔧 DevOps and SREs
* 📣 Technical marketers and architects
* 👨‍💻 Developers new to AI
* 🧑‍🤝‍🧑 Moms & Dads & Sons & Daughters and everything else
* 😤 Anyone tired of “just prompt it” explanations

If you’ve ever wondered how the model actually came up with that answer, you’re in the right place.

## 🤝 Contributing

This project is meant to be approachable, practical, and accurate. Contributions that help improve clarity and understanding are always welcome.

You don’t need to be an AI expert to contribute — in fact, some of the best contributions come from people learning this material for the first time as that is who it is targeted at. If you don't understand, then many others don't - please contribute however you can...

### 💡 Ways to Contribute

Here are some great ways to help:

* ✏️ Correct errors or typos
Small fixes matter, especially in explanations and comments.
* 🧠 Add clarity or context
If something didn’t click for you at first, improving the explanation helps everyone.
* ❓ Send me your questions
If you have a question that came up during a lesson, let me know. The idea is to try to be holistic and I don't know everything. Bonus points if you have the answer too!
* 🧩 Improve examples
Simplify code, add comments, or provide an alternative example that’s easier to reason about.
* 🧭 Add diagrams or visuals
Mental models always help. Visuals are always welcome.
* 📝 Expand lesson notes
Extra context, common pitfalls, or “things that confused me” notes are incredibly valuable.

### 🔁 How to Contribute

* 🍴 Fork the repository
* 🌱 Create a feature or fix branch
* ✏️ Make your changes
* 📬 Open a pull request with a short explanation of what you changed and why

If you’re unsure where something belongs, that’s okay — open a PR or issue, and we’ll figure it out.

### 🧭 Contribution Guidelines

A few simple guidelines to keep things consistent:

* Keep explanations plain-language and practical
* Avoid unnecessary jargon where possible
* Prefer understanding over completeness
* Examples should favor clarity over cleverness
* If adding code, include comments explaining why, not just what
* Be polite and respectful

This is a learning-first repository, not a reference manual.

### 🗣️ Feedback & Discussion

If you spot something confusing but aren’t sure how to fix it:

* Open an issue
* Ask a question
* Suggest an improvement

Feedback from people actively working through the lessons is especially valuable.
