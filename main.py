import pandas as pd
import numpy as np


class TreeNode:
    def __init__(self, name, occur, parent_node):
        self.name = name
        self.count = occur
        self.node_link = None
        self.parent = parent_node
        self.children = {}

    # Count Increment
    def increment(self, occur):
        self.count += occur

    # Tree Display
    def display(self, ind=1):
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.display(ind + 1)


test_set = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'], ['I2', 'I3'],
            ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]


def fp_tree_build(dataset, iceberg_condition):
    # def counts_dataset(dataset):
    #     merged_dataset = []
    #     for entry in dataset:
    #         for items in entry:
    #             merged_dataset.append(items)
    #     unique, counts = np.unique(merged_dataset, return_counts=True)
    #     sort_table = dict(zip(unique, counts))
    #     sequence_table = list(set(sorted(sort_table.values())))
    #     return sort_table, sequence_table
    #
    # def tree_build(dataset, ib_cd):
    #     pass
    #
    # st_table, seq_table = counts_dataset(dataset)
    # # print(st_table, seq_table)
    # for search_value in seq_table:
    #     for keys, values in st_table.items():
    #         if values == search_value:
    #             print(keys)

    def create_tree(dataset, ib_cd):
        item_table = {}
        for entry in dataset:  # First search, get accumulated supports
            for item in entry:
                item_table[item] = item_table.get(item, 0) + dataset[entry]
                # item_table = {item: support}
        for c in list(item_table):  # Delete entries not satisfied with iceberg condition
            if item_table[c] < ib_cd:
                del item_table[c]
        freq_item_set = set(item_table.keys())  # Save frequent items
        for k in item_table:  # Save count and pointer
            item_table[k] = [item_table[k], None]
            # item_table = {item: [support, None]}
        # print(freq_item_set, item_table)
        ret_tree = TreeNode('null', 1, None)
        for entry, count in dataset.items():
            local = {}
            for item in entry:
                if item in freq_item_set:
                    local[item] = item_table[item][0]
            if len(local) > 0:
                ordered_items = [i[0] for i in sorted(local.items(), key=lambda p: p[1], reverse=True)]
                update_tree(ordered_items, ret_tree, item_table, count)
        return ret_tree, item_table

    def update_tree(items, in_tree, item_table, count):
        if items[0] in in_tree.children:
            in_tree.children[items[0]].increment(count)
        else:
            in_tree.children[items[0]] = TreeNode(items[0], count, in_tree)
            if item_table[items[0]][1] is None:
                item_table[items[0]][1] = in_tree.children[items[0]]
            else:
                update_pointer(item_table[items[0]][1], in_tree.children[items[0]])
        if len(items) > 1:
            update_tree(items[1::], in_tree.children[items[0]], item_table, count)

    def update_pointer(node_to_test, target_node):
        while node_to_test.node_link is not None:
            node_to_test = node_to_test.node_link
        node_to_test.node_link = target_node

    def create_init_set(dataset):
        data_dic = {}
        for entry in dataset:
            data_dic[frozenset(entry)] = 0
        for entry in dataset:
            data_dic[frozenset(entry)] += 1
        # print(data_dic)
        # for entry in data_dic:
        #     if entry in np.array(dataset) - np.array(set(dataset)):
        #         data_dic[frozenset(entry)] += 1
        return data_dic

    df = pd.read_csv(
        '//Users/keweiwang/Google_Drive/Stony_Brook_University/Courses/589_Learning_Systems/Project1/Cryotherapy.csv',
        delimiter=",")
    basic = df.to_dict(orient='list')
    feature = list(basic.keys())
    del basic['age']
    del basic['Time']
    del basic['Area']
    # print(feature)
    dataset = list(basic.values())
    dataset = np.transpose(dataset).tolist()
    dataset = create_init_set(dataset)
    # print(dataset)

    tree, table = create_tree(dataset, 0)
    tree.display()


fp_tree_build(test_set, 0)