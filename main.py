import sys
from graph.workflow import create_workflow

def main():
    print("=" * 60)
    print("      AI Multi-Agent Blog Generator using LangGraph & Groq")
    print("=" * 60)
    
    # Prompt the user for the topic
    topic = input("\nEnter the topic for the blog post: ").strip()
    if not topic:
        print("Error: Topic cannot be empty.")
        sys.exit(1)
        
    print(f"\nInitializing agents workflow for topic: '{topic}'...")
    
    try:
        # Create the compiled graph workflow
        app = create_workflow()
        
        # Set the initial state
        initial_state = {
            "topic": topic,
            "research_data": "",
            "blog_post": ""
        }
        
        # Run the workflow with the initial state
        final_state = app.invoke(initial_state)
        
        # Display the result
        print("\n" + "=" * 60)
        print("                    GENERATED BLOG POST")
        print("=" * 60 + "\n")
        print(final_state["blog_post"])
        print("\n" + "=" * 60)
        
        # Save the generated blog post to a markdown file
        safe_title = "".join(c for c in topic.lower() if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
        filename = f"{safe_title}_blog.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_state["blog_post"])
        print(f"\nBlog post successfully saved to: {filename}")
        
    except Exception as e:
        print(f"\nAn error occurred during workflow execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
