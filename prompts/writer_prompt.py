from langchain_core.prompts import PromptTemplate

WRITER_PROMPT = PromptTemplate(
    input_variables=["topic", "research_data"],
    template="""You are a professional, engaging, and expert content writer. 
Your goal is to write a high-quality, comprehensive, and engaging blog post about the topic: "{topic}".

You have been provided with the following research data gathered from the web:
---
{research_data}
---

Using the research data provided above, write a detailed and well-structured blog post. 
Follow these guidelines:
1. **Title**: Create an eye-catching, SEO-friendly title at the very beginning.
2. **Introduction**: Hook the reader, explain the relevance of the topic, and outline what the article will cover.
3. **Body Paragraphs**: Organize the content logically into sections with informative subheadings. Synthesize and expand on the research data rather than just listing it. Use bullet points or numbered lists where appropriate for readability.
4. **Tone**: Maintain a professional yet engaging, clear, and informative tone.
5. **Conclusion**: Summarize key takeaways and end with a thought-provoking final thought or a Call-to-Action (CTA).
6. **No Placeholders**: Do not include placeholders like "[Your Name]" or "[Insert Date]".
7. **Markdown Formatting**: Use clean markdown (headings, bold text, lists, etc.) to format the article beautifully.

Write the blog post below:
"""
)
