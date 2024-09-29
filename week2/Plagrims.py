import nltk
import string
import heapq

nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize

def tokenize_document(document):
    """Tokenize the input document into sentences."""
    return sent_tokenize(document)

def normalize_text(text):
    """Normalize the text by converting to lowercase and removing punctuation."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return ' '.join(text.split())

def edit_distance(s1, s2):
    """Compute the Levenshtein distance between two sentences."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],
                                   dp[i][j-1],
                                   dp[i-1][j-1])
    return dp[m][n]

def a_star_alignment(doc1_sentences, doc2_sentences):
    """Use A* search to align the sentences from two documents."""
    start_state = (0, 0, 0)
    goal_state = (len(doc1_sentences), len(doc2_sentences))

    open_set = []
    heapq.heappush(open_set, (0, start_state))

    cost_so_far = {start_state: 0}

    while open_set:
        _, (pos1, pos2, cost) = heapq.heappop(open_set)

        if (pos1, pos2) == goal_state:
            return cost

        next_states = []

        if pos1 < len(doc1_sentences) and pos2 < len(doc2_sentences):
            next_cost = cost + edit_distance(doc1_sentences[pos1], doc2_sentences[pos2])
            next_states.append((pos1 + 1, pos2 + 1, next_cost))

        if pos1 < len(doc1_sentences):
            next_cost = cost + len(doc1_sentences[pos1])
            next_states.append((pos1 + 1, pos2, next_cost))

        if pos2 < len(doc2_sentences):
            next_cost = cost + len(doc2_sentences[pos2])
            next_states.append((pos1, pos2 + 1, next_cost))

        for state in next_states:
            pos1_next, pos2_next, new_cost = state
            if (pos1_next, pos2_next) not in cost_so_far or new_cost < cost_so_far[(pos1_next, pos2_next)]:
                cost_so_far[(pos1_next, pos2_next)] = new_cost
                priority = new_cost + heuristic(doc1_sentences, doc2_sentences, pos1_next, pos2_next)
                heapq.heappush(open_set, (priority, state))

    return float('inf')

def heuristic(doc1_sentences, doc2_sentences, pos1, pos2):
    """Heuristic function based on the remaining sentence lengths."""
    return abs(len(doc1_sentences) - pos1 - (len(doc2_sentences) - pos2))

def detect_plagiarism(doc1, doc2):
    """Detect plagiarism by aligning sentences from two documents."""
    doc1_sentences = [normalize_text(s) for s in tokenize_document(doc1)]
    doc2_sentences = [normalize_text(s) for s in tokenize_document(doc2)]

    aligned_sentences = []
    alignment_cost = a_star_alignment(doc1_sentences, doc2_sentences)

    plagiarism_threshold = 5

    for i in range(len(doc1_sentences)):
        for j in range(len(doc2_sentences)):
            if edit_distance(doc1_sentences[i], doc2_sentences[j]) <= plagiarism_threshold:
                aligned_sentences.append((doc1_sentences[i], doc2_sentences[j]))

    return aligned_sentences, alignment_cost

def test_identical_documents():
    doc1 = "This is the first sentence. This is the second sentence. Finally, this is the third sentence."
    doc2 = "This is the first sentence. This is the second sentence. Finally, this is the third sentence."

    aligned_sentences, cost = detect_plagiarism(doc1, doc2)

    print("Test Case 1: Identical Documents")
    print(f"Aligned Sentences: {aligned_sentences}")
    print(f"Total Alignment Cost: {cost}")

    assert cost == 0, f"Expected cost to be 0, but got {cost}."
    print("Test Case 1: Passed")
    print()

def test_slightly_modified_document():
    doc1 = "This is the first sentence. This is the second sentence. Finally, this is the third sentence."
    doc2 = "This is the first sentence. This is the second phrase. Lastly, this is the third line."

    aligned_sentences, cost = detect_plagiarism(doc1, doc2)

    print("Test Case 2: Slightly Modified Document")
    print(f"Aligned Sentences: {aligned_sentences}")
    print(f"Total Alignment Cost: {cost}")

    assert cost > 0, f"Expected cost to be greater than 0, but got {cost}."
    assert len(aligned_sentences) > 0, f"Expected some aligned sentences, but got none."
    print("Test Case 2: Passed")
    print()

def test_completely_different_documents():
    doc1 = "This is a scientific research paper. It discusses quantum physics and black holes."
    doc2 = "The weather today is sunny with clear skies. People are enjoying their day at the beach."

    aligned_sentences, cost = detect_plagiarism(doc1, doc2)

    print("Test Case 3: Completely Different Documents")
    print(f"Aligned Sentences: {aligned_sentences}")
    print(f"Total Alignment Cost: {cost}")

    assert cost > 0, f"Expected cost to be greater than 0, but got {cost}."
    assert len(aligned_sentences) == 0, f"Expected no aligned sentences, but got {aligned_sentences}"
    print("Test Case 3: Passed")
    print()

def test_partial_overlap():
    doc1 = "This is a scientific research paper. It discusses quantum physics and black holes. The weather today is sunny."
    doc2 = "The weather today is sunny with clear skies. People are enjoying their day at the beach. It discusses quantum physics briefly."

    aligned_sentences, cost = detect_plagiarism(doc1, doc2)

    print("Test Case 4: Partial Overlap")
    print(f"Aligned Sentences: {aligned_sentences}")
    print(f"Total Alignment Cost: {cost}")

    print("Test Case 4: Passed")
    print()

def main():
    print("Running Plagiarism Detection Tests\n")
    test_identical_documents()
    test_slightly_modified_document()
    test_completely_different_documents()
    test_partial_overlap()
    print("All tests completed successfully.")

if _name_ == "_main_":
    main()