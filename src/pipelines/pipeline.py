from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ========================================================
    # STEP 1 - SEARCH AGENT
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 1 - Search Agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Find recent, reliable and detailed information about:

{topic}

Search for multiple relevant sources.
Return the titles, URLs and useful information from the sources.
"""
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print("\nSEARCH RESULT:")
    print(state["search_results"])


    # ========================================================
    # STEP 2 - READER AGENT
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 2 - Reader Agent is scraping resources...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Based on the following search results about:

{topic}

Identify the most relevant URL and use the scraping tool
to extract deeper information from that source.

Search Results:

{state["search_results"][:8000]}
"""
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nSCRAPED CONTENT:")
    print(state["scraped_content"])


    # ========================================================
    # STEP 3 - WRITER
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"

        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print("\nFINAL REPORT:")
    print(state["report"])


    # ========================================================
    # STEP 4 - CRITIC
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"],
    })

    print("\nCRITIC REPORT:")
    print(state["feedback"])


    # ========================================================
    # RETURN FINAL STATE
    # ========================================================

    return state