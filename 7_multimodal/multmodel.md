# Concepts Practiced in This Multimodal Lecture

This lecture focused on building an AI flow where the model can read an image and then give useful guidance in plain language.

## 1. Multimodal AI (Image + Text)
We practiced sending an image (`blood_work.png`) and a text instruction together.

What this means:
- Normal chat AI reads only text.
- Multimodal AI can read text and also understand image content.

In this demo, the AI read a blood report image and interpreted test values.

## 2. Prompting the Model Clearly
We learned that model output depends heavily on instructions.

- Broad instruction -> very long, detailed report
- Specific instruction -> short, focused summary

By tightening the prompt, we made the answer concise (2-3 sentences) instead of a full medical-style report.

## 3. Tool Calling (Agent + Function)
We added a tool (`get_diet_recommendation`) that returns diet advice based on condition:
- `normal`
- `high_cholesterol`
- `high_sugar`

The agent workflow was:
1. Analyze blood report image
2. Classify condition
3. Call the diet tool
4. Respond with recommendation

This is the core idea of an AI agent: not just generating text, but using tools to perform structured tasks.

## 4. Structured Response Handling
Sometimes model output came as a structured object (like a list of content blocks) instead of plain text.

So we practiced:
- Extracting only the text part
- Ignoring internal metadata
- Displaying clean output for end users

This is important in real apps so users see readable answers, not raw technical data.

## 5. Real-World Troubleshooting
We also handled common integration issues:

### SSL/Connection trust issue
The environment had certificate trust problems while connecting to APIs.

What we applied:
- `truststore` to use system certificates and fix secure connection failures.

### Model access issue
A Groq vision model was unavailable for the account.

What we applied:
- Switched to an accessible image-capable model (`gemini-3.5-flash`).

This teaches an important practical lesson: model availability can vary by account/region, so fallback options matter.

## Final Outcome
You built a working multimodal mini-agent that can:
1. Read a blood report image
2. Detect likely condition (example: high cholesterol)
3. Use a tool to generate diet guidance
4. Return a short and user-friendly recommendation

## Why This Matters
This lecture shows how modern AI apps are built in practice:
- Multimodal input
- Agent decision-making
- Tool integration
- Output formatting
- Production-style debugging

In simple terms: you moved from "chatbot" to a task-oriented assistant that can see, reason, and respond with actionable advice.
