from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ============================================================
    # STEP 1 - SEARCH AGENT
    # ============================================================

    print("\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch Result:\n")
    print(state["search_results"])


    # ============================================================
    # STEP 2 - READER AGENT
    # ============================================================

    print("\n" + " =" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Based on the following search results about '{topic}',
pick the most relevant URL and scrape it for deeper content.

Search Results:
{state["search_results"][:3000]}
"""
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n")
    print(state["scraped_content"])


    # ============================================================
    # STEP 3 - WRITER
    # ============================================================

    print("\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report:\n")
    print(state["report"])


    # ============================================================
    # STEP 4 - CRITIC
    # ============================================================

    print("\n" + " =" * 50)
    print("step 4 - Critic is reviewing the report ...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Report:\n")
    print(state["feedback"])


    return state