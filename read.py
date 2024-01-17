from heapq import heappush, heappop

class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

class ShannonNode:
    def __init__(self, symbol, probability):
        self.symbol = symbol
        self.probability = probability
        self.code = ""

def build_huffman_tree(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heappush(priority_queue, HuffmanNode(None, 0))

    while len(priority_queue) > 1:
        node1 = heappop(priority_queue)
        node2 = heappop(priority_queue)

        merged_node = HuffmanNode(None, node1.frequency + node2.frequency)
        merged_node.left = node1
        merged_node.right = node2

        heappush(priority_queue, merged_node)

    return priority_queue[0]

def build_huffman_codes(node, current_code="", codes={}):
    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + "0", codes)
        build_huffman_codes(node.right, current_code + "1", codes)
    return codes

def build_shannon_fano_tree(nodes):
    if len(nodes) == 1:
        return nodes

    nodes.sort(key=lambda x: x.probability, reverse=True)
    total_prob = sum(node.probability for node in nodes)
    cumulative_prob = 0

    for i, node in enumerate(nodes):
        cumulative_prob += node.probability
        if cumulative_prob >= total_prob / 2:
            return build_shannon_fano_tree(nodes[:i+1]), build_shannon_fano_tree(nodes[i+1:])

def assign_codes(node, code=""):
    if len(node) == 1:
        node[0].code += code
    else:
        assign_codes(node[0], code + "0")
        assign_codes(node[1], code + "1")

def huffman_and_shannon_fano_encoding(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    # Huffman
    huffman_root = build_huffman_tree(text)
    huffman_codes = build_huffman_codes(huffman_root)

    print("Huffman Codes:")
    for char, code in huffman_codes.items():
        print(f"{char} {code}")

    # Shannon-Fano
    symbols_frequency = {}
    for symbol in text:
        if symbol in symbols_frequency:
            symbols_frequency[symbol] += 1
        else:
            symbols_frequency[symbol] = 1

    shannon_nodes = [ShannonNode(symbol, freq/len(text)) for symbol, freq in symbols_frequency.items()]
    shannon_tree = build_shannon_fano_tree(shannon_nodes)
    assign_codes(shannon_tree)

    print("\nShannon-Fano Codes:")
    for node in shannon_nodes:
        print(f"{node.symbol} {node.code}")

if __name__ == "__main__":
    file_name = "bajki.txt"
    huffman_and_shannon_fano_encoding(file_name)
