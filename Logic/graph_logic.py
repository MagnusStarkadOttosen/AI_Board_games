from Logic.tree_logic import GameTreeNode
from anytree import Node
from anytree.exporter import DotExporter

def build_anytree(node, parent=None):
    """
    Recursively converts a GameTreeNode into an `anytree` structure.
    """
    if node.winner == "B":
        color = "red"
    elif node.winner == "W":
        color = "green"
    elif node.winner == "Tie":
        color = "blue"
    else:
        color = "white"
    
    move_text = f"Move: {node.move}" if node.move else "Root"
    tree_node = Node(f"{move_text}\n{node.board_str()}", parent=parent, winner=node.winner, color=color)

    for child in node.children:
        build_anytree(child, tree_node)

    return tree_node


def export_colored_tree(anytree_root, filename="tree.dot"):
    """
    Exports the game tree visualization in a DOT file for Graphviz.
    """
    DotExporter(anytree_root, nodeattrfunc=lambda node: f'style=filled, fillcolor={node.color}').to_dotfile(filename)

