import ete3.ncbi_taxonomy.ncbiquery as nt
from Bio.Phylo import BaseTree
from nbitk.Taxon import Taxon


def _recurse_tree(bp_parent, ete3_parent):

    # iterate over children in ete3 node
    for ete3_child in ete3_parent.children:

        # create a Taxon object for each child
        bp_child = Taxon(
            name=ete3_child.taxname,
            taxonomic_rank=ete3_child.rank,
            guids={"taxon": ete3_child.name},
        )
        bp_parent.clades.append(bp_child)
        _recurse_tree(bp_child, ete3_child)


class Parser:
    def __init__(self, file):
        self.file = file

    def parse(self):

        # Load nodes.dmp and names.dmp via ETE3
        tree, synonyms = nt.load_ncbi_tree_from_dump(self.file)

        # Create a new base tree and root node
        root = Taxon(name=tree.taxname, taxonomic_rank=tree.rank, guids={"taxon": tree.name})
        bt = BaseTree.Tree(root)

        # Recursively traverse the tree and create Taxon objects
        _recurse_tree(root, tree)

        # Done.
        return bt
