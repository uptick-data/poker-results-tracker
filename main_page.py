import awesome_streamlit as ast
import streamlit as st

import src.pages.poker_app
import src.pages.poker_results_charts

ast.core.services.other.set_logging_format()

PAGES = {"Home": src.pages.poker_results_charts, "Input Results": src.pages.poker_app}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This is a simple poker results tracker with some charts built into it
        """
    )


if __name__ == "__main__":
    main()
