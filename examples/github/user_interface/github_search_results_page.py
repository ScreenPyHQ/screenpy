"""
Locators for the GitHub search results page.
"""


from screenpy import Target

RESULTS_MESSAGE = Target.the("search results message").located_by(
    "div.codesearch-results > div > div > h3"  # ew
)
SEARCH_RESULTS = Target.the("search results items").located_by("li.repo-list-item")
