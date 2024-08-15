import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Probabilities dictionaries to return
    probabilidades = {}

    # Links to go using the damping factor probability
    links_page = corpus[page]

    # Pages to go with the 1-damping factor probability
    links_available = []
    for page in corpus:
        links_available.append(page)
        probabilidades[page] = 0

    # When a link is visited within the page, construct the transition model
    for link in links_page:
        probabilidades[link] = (1/len(links_page)) * (damping_factor)

    # When link is choosen at random throught the entire corpus
    for link in links_available:
        probabilidades[link] = probabilidades[link] + ((1/len(links_available)) * (1 - damping_factor))

    return probabilidades


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())

    # Random first page from those available
    page_first = random.choice(pages)

    # Dictionary with sample probablities
    pages_created = {}

    # Ser a starting probability of 0 for each different page
    for page in pages:
        pages_created[page] = 0

    # Set the probability of page_first = 1/N
    pages_created[page_first] = 1/n

    # Define probabilities to go to other pages based on the page_first
    current_probabilities = transition_model(corpus, page_first, damping_factor)

    # Sample over n-1, because first one is already done before
    for i in range(0, n-1):
        # Get random page based on the probabi. already had
        new_page = random.choices(list(current_probabilities.keys()),
                                  list(current_probabilities.values()), k=1)
        # Add this page probability
        pages_created[new_page[0]] = pages_created[new_page[0]] + (1/n)
        # Get new probability
        current_probabilities = transition_model(corpus, new_page[0], damping_factor)

    return pages_created


# def sum_ranks(corpus, damping_factor):
#     """
#     Implement the formula in other function
#     """


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize variables
    number_pages = len(corpus)
    pageranks = {page: 1 / number_pages for page in corpus}
    new_pageranks = pageranks.copy()

    # Iterate until convergence
    while True:
        for page in corpus:
            rank = (1 - damping_factor) / number_pages

            for current_page in corpus:
                if corpus[current_page]:
                    if page in corpus[current_page]:
                        rank += damping_factor * pageranks[current_page] / len(corpus[current_page])
                else:
                    rank += damping_factor * pageranks[current_page] / number_pages

            new_pageranks[page] = rank

        if all(abs(new_pageranks[page] - pageranks[page]) < 0.001 for page in pageranks):
            break

        pageranks = new_pageranks.copy()

    return pageranks


if __name__ == "__main__":
    main()
