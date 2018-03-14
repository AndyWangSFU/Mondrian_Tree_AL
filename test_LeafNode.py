import unittest
from LeafNode import LeafNode

class test_LeafNode(unittest.TestCase):

    '''Unit testing for LeafNode'''

    def setUp(self):
        LeafNode.leaf_ids = 0
        self.test_leaf_empty = LeafNode()
        self.test_leaf_good = LeafNode(
            labelled_index=[1,2,3,4], 
            unlabelled_index=[5,6,7,8,9,10], 
            linear_dims=[[0,1], [0,1]])
        self.test_leaf_neg = LeafNode(
            labelled_index=[1,2,3,4], 
            unlabelled_index=[5,6,7,8,9,10], 
            linear_dims=[[-2,-1], [-2,-1]])
        self.test_leaf_mixed = LeafNode(
            labelled_index=[1,2,3,4], 
            unlabelled_index=[5,6,7,8,9,10], 
            linear_dims=[[-1,1], [-1,1]])

    # Testing the leaf ids

    # def test_leaf_id(self):
    #     self.assertEqual(self.test_leaf_empty.leaf_id,1)
    #     self.assertEqual(self.test_leaf_good.leaf_id,2)

    # Testing the subtree_linear_dim method

    def test_dim_length_good(self):
        self.assertEqual(self.test_leaf_good.subtree_linear_dim, 2)

    def test_dim_length_neg(self):
        self.assertEqual(self.test_leaf_neg.subtree_linear_dim, 2)

    def test_dim_length_mixed(self):
        self.assertEqual(self.test_leaf_mixed.subtree_linear_dim, 4)

    def test_dim_length_empty(self):
        self.assertEqual(self.test_leaf_empty.subtree_linear_dim, 0)

    # Testing the pick_new_points method

    def test_pick_new_points_good(self):
        self.assertEqual(self.test_leaf_good.pick_new_points(1, set_seed=1),[6])
        self.assertEqual(self.test_leaf_good.pick_new_points(2, set_seed=1),[7,5])

    def test_pick_new_points_good_all(self):
        self.assertEqual(self.test_leaf_good.pick_new_points(6, set_seed=1),[6,9,5,10,8,7])

    def test_pick_new_points_empty(self):
        with self.assertRaises(ValueError):
            self.test_leaf_empty.pick_new_points(1)

    def test_pick_new_points_self_update_true(self):
        self.test_leaf_good.pick_new_points(1, set_seed=1)
        self.assertEqual(self.test_leaf_good.labelled_index,[1,2,3,4,6])
        self.assertEqual(self.test_leaf_good.unlabelled_index,[5,7,8,9,10])

    def test_pick_new_points_self_update_false(self):
        self.test_leaf_good.pick_new_points(1, self_update = False, set_seed=1)
        self.assertEqual(self.test_leaf_good.labelled_index,[1,2,3,4])
        self.assertEqual(self.test_leaf_good.unlabelled_index,[5,6,7,8,9,10])

    def test_make_labelled_not_in_unlabelled(self):
        with self.assertRaises(ValueError):
            self.test_leaf_empty.make_labelled(1)

    def test_make_labelled_in_unlabelled(self):
        self.test_leaf_good.make_labelled(5)
        self.assertTrue(5 not in self.test_leaf_good.unlabelled_index)
        self.assertTrue(5 in self.test_leaf_good.labelled_index)

    # Used to detect tricky mutable default arguments error. DEFAULT TO NONE AND DEAL WITH 
    # IT IN THE FUNCTION

    # def test_spillover(self):
    #     leaf_one = LeafNode()
    #     leaf_three = LeafNode()
    #     leaf_one.labelled_index = [1,2]
    #     leaf_two = LeafNode()
    #     print(leaf_one.labelled_index)
    #     print(leaf_two.labelled_index)
    #     print(leaf_three.labelled_index)

    # def test_spillover_2(self):
    #     leaf_one = LeafNode()
    #     leaf_three = LeafNode()
    #     leaf_one.extend_labelled_index([1,2])
    #     leaf_two = LeafNode()
    #     print(leaf_one.labelled_index)
    #     print(leaf_two.labelled_index)
    #     print(leaf_three.labelled_index)

    # def test_spillover_3(self):
    #     leaf_one = LeafNode()
    #     leaf_three = LeafNode()
    #     leaf_one.labelled_index.extend([1,2])
    #     leaf_two = LeafNode()
    #     print(leaf_one.labelled_index)
    #     print(leaf_two.labelled_index)
    #     print(leaf_three.labelled_index)

    # def test_spillover_4(self):
    #     leaf_one = LeafNode()
    #     leaf_three = LeafNode()
    #     leaf_one.labelled_index.append(3)
    #     leaf_two = LeafNode()
    #     print(leaf_one.labelled_index)
    #     print(leaf_two.labelled_index)
    #     print(leaf_three.labelled_index)




if __name__ == '__main__':
    unittest.main()