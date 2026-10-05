
import streamlit as st
import urllib.parse
import urllib.request
import json

st.set_page_config(
    page_title="EngiSearch AI",
    page_icon="🔎"
)

st.title("🔎 EngiSearch AI")
st.subheader("AI-Powered Engineering Research Assistant")

st.write(
    "Search engineering research papers, organize results, "
    "and understand technical information."
)

topic = st.text_input(
    "Enter an engineering topic:",
    placeholder="Example: 5G antenna materials"
)

if st.button("Search"):

    if topic:

        st.success(f"Searching for: {topic}")

        try:
            # Prepare the search query
            query = urllib.parse.quote(
                f"{topic} engineering technology research"
            )

            # OpenAlex research database
            url = (
                f"https://api.openalex.org/works"
                f"?search={query}&per-page=5"
            )

            # Get research papers
            with urllib.request.urlopen(url, timeout=15) as response:
                data = json.loads(response.read().decode())

            results = data.get("results", [])

            if results:

                st.subheader("📚 Research Papers Found")

                for i, paper in enumerate(results, start=1):

                    title = paper.get(
                        "display_name",
                        "Title not available"
                    )

                    year = paper.get(
                        "publication_year",
                        "Year not available"
                    )

                    doi = paper.get("doi")

                    authors = []

                    for author in paper.get("authorships", []):
                        name = author.get(
                            "author", {}
                        ).get("display_name")

                        if name:
                            authors.append(name)

                    st.markdown(f"### {i}. {title}")

                    st.write(f"**Year:** {year}")

                    if authors:
                        st.write(
                            "**Authors:** " +
                            ", ".join(authors[:5])
                        )

                    if doi:
                        st.markdown(f"**DOI:** [Open Paper]({doi})")

                    # Abstract
                    abstract = paper.get("abstract_inverted_index")
                    abstract_text = "Abstract is not available for this paper."

                    if abstract:
                        words = [""] * (
                            max(
                                max(positions)
                                for positions in abstract.values()
                            ) + 1
                        )

                        for word, positions in abstract.items():
                            for position in positions:
                                words[position] = word

                        abstract_text = " ".join(words)
                        simple_explanation = (
                            "This research paper is about " + title
                            + ". The abstract explains the main idea, method, and findings."
                        )
                    with st.expander(
                        "📖 Read Abstract / Simple Explanation"
                    ):
                        st.write(abstract_text)
                        st.write(simple_explanation)
                    
                    st.markdown("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
            else:
                st.info(
                    "No research papers were found. "
                    "Try another engineering topic."
                )

        except Exception as e:
            st.error(
                "Unable to fetch research results right now."
            )

            st.write(
                "Please check your internet connection "
                "and try again."
            )

    else:
        st.warning("Please enter an engineering topic.")