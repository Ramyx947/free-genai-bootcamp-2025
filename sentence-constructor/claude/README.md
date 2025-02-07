# Anthrop / Claude 3.5 Sonnet

## Prompting Guides
https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags

Anthropic have very specific suggestions for providing good prompting.

## Key Points for Claude Prompt Engineering Using XML Tags

### Structure Your Prompts with XML Tags:
- Use XML tags (e.g., <instructions>, <example>, <formatting>) to clearly separate components like context, instructions, and examples.

### Benefits of XML Tagging:
- Clarity: Distinct sections prevent mixing up instructions with examples or context.
- Accuracy: Reduces errors from misinterpretation.
- Flexibility: Easily add, remove, or modify parts without rewriting the entire prompt.
- Parseability: Facilitates extraction of specific parts during post-processing of Claude's output.

### Tagging Best Practices:
- Be Consistent: Use the same tag names throughout your prompts.
- Nest Tags: Use nested tags (e.g., <outer><inner></inner></outer>) for hierarchical content.
- Combine Techniques: Enhance structure by integrating XML tagging with methods like multishot prompting (<examples>) and chain-of-thought prompts (<thinking>, <answer>).