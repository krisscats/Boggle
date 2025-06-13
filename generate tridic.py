import pickle

class TrieNode:
    def __init__(self, char=''):
        self.char = char
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.strip():
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word.strip():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def to_nested_list(self, node=None):
        if node is None:
            node = self.root
        return [node.char, [self.to_nested_list(child) for child in node.children.values()], node.is_end_of_word]

    def from_nested_list(self, nested, parent=None):
        char, children_list, is_end = nested
        node = TrieNode(char)
        node.is_end_of_word = is_end
        for child_nested in children_list:
            child_node = self.from_nested_list(child_nested, node)
            node.children[child_node.char] = child_node
        return node

    def save_as_nested_list(self, filename):
        nested = self.to_nested_list(self.root)
        with open(filename, 'wb') as f:
            pickle.dump(nested, f)
        print(f"Trie saved as nested list in '{filename}'")

    def load_from_nested_list_file(self, filename):
        with open(filename, 'rb') as f:
            nested = pickle.load(f)
        self.root = self.from_nested_list(nested)


def build_trie_from_file(filename):
    trie = Trie()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                trie.insert(word)
    return trie


# === Main Usage ===
if __name__ == "__main__":
    source_file = "project 3/dicc.txt"
    output_file = "project 3/trie_nested.pkl"

    trie = build_trie_from_file(source_file)
    trie.save_as_nested_list(output_file)

    # OPTIONAL: Load and test
    # new_trie = Trie()
    # new_trie.load_from_nested_list_file(output_file)
    # print(new_trie.search("cat"))  # Test
