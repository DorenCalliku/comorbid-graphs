#!/usr/bin/env python
# coding: utf-8

import io
from anytree import RenderTree, PreOrderIter, findall
from contextlib import redirect_stdout
from anytree.importer import DictImporter
from anytree.exporter import DictExporter


class AnyTreeMixin(object):
    def import_tree(self, json_data):
        return DictImporter().import_(json_data)

    @classmethod
    def export_node(cls, node):
        return DictExporter().export(node)

    def export(self):
        return type(self).export_node(self.tree)

    def find_node(self, node_name, pos=0):
        if not node_name:
            raise Exception('Node not provided.')
        found_val = findall(
            self.tree, filter_=lambda node: node.name.lower() == node_name.lower()
            if node.name else []
        )
        # TODO: find best match here, not first one
        if found_val is not None and len(found_val) > 0:
            return found_val[pos]
        return None

    @classmethod
    def merge_trees(cls, json_list, parent_name="Source"):
        tree = cls({"name": parent_name, "children": json_list})
        return tree

    @classmethod
    def generate_tree_from_node(cls, node, max_level):
        """ 
        print all nodes to be able to
        see which ones are the ones we need
        """
        with io.StringIO() as buf, redirect_stdout(buf):
            for pre, _, node in RenderTree(node, maxlevel=max_level):
                print("%s%s" % (pre, node.name))
            return buf.getvalue()

    def pretty_print_tree(self, node_name=None, max_level=3):
        if not node_name:
            node_name = self.tree.name
        node = self.find_node(node_name)
        if not node:
            return ""
        return self.generate_tree_from_node(node, max_level=max_level)

    def graph(self, node_name=None):
        # check if not starting from center
        found_node = self.find_node(node_name)
        if found_node:
            base_node = found_node
        else:
            base_node = self.tree
        return type(self).generate_tree_graph_data(base_node)

    @classmethod
    def generate_tree_graph_data(cls, base_node):
        """For google-charts structure.
        They use 'Source'.
        """
        base = []
        for node in PreOrderIter(base_node):
            if node.parent:
                base.append(
                    [
                        node.name + " \n(" + str(getattr(node.parent, "id", 0)) + ")",
                        node.parent.name
                        + " \n("
                        + str(getattr(node.parent, "id", 0))
                        + ")",
                        len(node.children) if len(node.children) else 1,
                    ]
                )
        if base == []:
            return base
        # check if not null at first parent level
        if base[0][1] != "Source":
            base = [[base[0][1], "Source", 1]] + base
        return base

    @staticmethod
    def generate_tree_from_grouped_stats(grouped_stats):
        """For google-charts structure.
        They use 'Source'.
        """
        graph_data = []
        for key, vals in grouped_stats.items():
            graph_data += vals
            graph_data.append([key, "Source", len(vals)])
        return graph_data

    def get_tree_and_graph(self, name=None):
        """Unnecessary method, for ease of use."""
        if not name:
            name = self.tree.name
        node = self.find_node(name)
        return (
            self.pretty_print_tree(node.name).split("\n")[:-1],
            self.generate_tree_graph_data(node)
        )
