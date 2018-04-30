import unittest
import math
import random
import warnings
import utils

import numpy as np

from Mondrian_Tree import Mondrian_Tree
from LeafNode import LeafNode


class test_Mondrian_Tree(unittest.TestCase):

    # TODO: Run tests with inputing data with numpy arrays

    def setUp(self):

        self.d = 3
        self.a = 1
        self.linear_dims = [[0,1]]*self.d
        self.mt1 = Mondrian_Tree(self.linear_dims)

        self.n_points = 100
        self.n_labelled = 20
        random.seed(123)
        self.labels = [random.random() for i in range(self.n_labelled)]
        self.labelled_indices = range(self.n_labelled)
        self.data = []
        random.seed(1)
        for i in range(self.n_points):
            point = []
            for j in range(self.d):
                point.append(random.random())
            self.data.append(point)

    ###########################################

    # Basic life time updating tests

    def test_update_first_life_time_0p1(self):
        temp = Mondrian_Tree([[0,1]]*5)
        temp.update_life_time(0.1,set_seed=1)
        self.assertEqual(temp._num_leaves,3)

    def test_update_first_life_time_0p5(self):
        temp = Mondrian_Tree([[0,1]]*5)
        temp.update_life_time(0.5,set_seed=1)
        self.assertEqual(temp._num_leaves,8)

    def test_update_first_life_time_1(self):
        temp = Mondrian_Tree([[0,1]]*5)
        temp.update_life_time(1,set_seed=1)
        self.assertEqual(temp._num_leaves,36)

    def test_update_life_time_tuned(self):

        self.mt1.update_life_time(self.a * self.n_labelled**(1/(2+self.d) - 1),set_seed=1)
        self.assertEqual(self.mt1._num_leaves,2)

    def test__test_point(self):
        with self.assertRaises(ValueError):
            self.mt1._test_point([])
            self.mt1._test_point([1,2,3,4,5])
        with self.assertRaises(TypeError):
            self.mt1._test_point(1)
            self.mt1._test_point({})
            self.mt1._test_point('abc')

        good_point = [1]*self.d
        self.assertEqual(good_point, self.mt1._test_point(good_point))
        self.assertEqual(good_point, self.mt1._test_point(np.array(good_point)))

    ###########################################

    # Testing input data

    def test_input_data_empty_root(self):
        self.mt1.input_data([],[],[])
        self.assertEqual(self.mt1._num_points,0)

    def test_input_data_empty(self):
        lbda = 1
        self.mt1.update_life_time(lbda, set_seed=1)
        self.mt1.input_data([],[],[])
        self.assertEqual(self.mt1._num_points,0)

    def test_input_data_root_no_labels(self):
        self.mt1.input_data([[0]*self.d],[],[])
        self.assertEqual(self.mt1._num_points,1)
        self.assertEqual(self.mt1.labels,[None])
        self.assertEqual(self.mt1._root.unlabelled_index,[0])
        self.assertEqual(self.mt1._root.labelled_index,[])

    def test_input_data_root_labels(self):
        self.mt1.input_data([[0]*self.d],[0],[3.141])
        self.assertEqual(self.mt1._num_points,1)
        self.assertEqual(self.mt1.labels,[3.141])
        self.assertEqual(self.mt1._root.unlabelled_index,[])
        self.assertEqual(self.mt1._root.labelled_index,[0])

    def test_input_data(self):
        lbda = 0.5
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        self.assertEqual(self.mt1._num_points,self.n_points)
        self.assertEqual(self.mt1._num_labelled,self.n_labelled)
        
        self.mt1.make_full_leaf_list()
        for node in self.mt1._full_leaf_list:
            # print(len(node.labelled_index), len(node.unlabelled_index))

            linear_dims = node.linear_dims
            for ind in node.labelled_index:
                point = self.mt1.points[ind]
                for dim in range(self.d):
                    # print(linear_dims[dim][0], point[dim], linear_dims[dim][1])
                    self.assertTrue(point[dim] >= linear_dims[dim][0])
                    self.assertTrue(point[dim] <= linear_dims[dim][1])

            for ind in node.unlabelled_index:
                point = self.mt1.points[ind]
                for dim in range(self.d):
                    # print(linear_dims[dim][0], point[dim], linear_dims[dim][1])
                    self.assertTrue(point[dim] >= linear_dims[dim][0])
                    self.assertTrue(point[dim] <= linear_dims[dim][1])

    def test_update_life_time_with_data(self):
        lbda = 0.5
        lbda2 = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        # print(self.mt1._num_points)

        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.update_life_time(lbda2, set_seed=100)
        # print(self.mt1._num_points)

        self.mt1.make_full_leaf_list()
        for node in self.mt1._full_leaf_list:
            # print(len(node.labelled_index), len(node.unlabelled_index))

            linear_dims = node.linear_dims
            for ind in node.labelled_index:
                point = self.mt1.points[ind]
                for dim in range(self.d):
                    # print(linear_dims[dim][0], point[dim], linear_dims[dim][1])
                    self.assertTrue(point[dim] >= linear_dims[dim][0])
                    self.assertTrue(point[dim] <= linear_dims[dim][1])

            for ind in node.unlabelled_index:
                point = self.mt1.points[ind]
                for dim in range(self.d):
                    # print(linear_dims[dim][0], point[dim], linear_dims[dim][1])
                    self.assertTrue(point[dim] >= linear_dims[dim][0])
                    self.assertTrue(point[dim] <= linear_dims[dim][1])

    def test_input_data_with_numpy(self):
        lbda = 0.5
        self.mt1.update_life_time(lbda, set_seed=100)
        np_data = np.array(self.data)
        # print(np_data)
        np_labels = np.array(self.labels)
        self.mt1.input_data(np_data, self.labelled_indices, np_labels)

        self.assertEqual(self.mt1._num_points,self.n_points)
        self.assertEqual(self.mt1._num_labelled,self.n_labelled)
        
        self.mt1.make_full_leaf_list()
        for node in self.mt1._full_leaf_list:
            # print(len(node.labelled_index), len(node.unlabelled_index))

            linear_dims = node.linear_dims
            for ind in node.labelled_index:
                point = self.mt1.points[ind]
                for dim in range(self.d):
                    # print(linear_dims[dim][0], point[dim], linear_dims[dim][1])
                    self.assertTrue(point[dim] >= linear_dims[dim][0])
                    self.assertTrue(point[dim] <= linear_dims[dim][1])

            for ind in node.unlabelled_index:
                point = self.mt1.points[ind]
                for dim in range(self.d):
                    # print(linear_dims[dim][0], point[dim], linear_dims[dim][1])
                    self.assertTrue(point[dim] >= linear_dims[dim][0])
                    self.assertTrue(point[dim] <= linear_dims[dim][1])


    def test_label_point_root(self):
        val = 1
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.label_point(self.n_labelled, val)
        self.assertEqual(self.mt1.labels[self.n_labelled],val)
        self.assertEqual(self.mt1._num_labelled, self.n_labelled + 1)
        leaf = self.mt1._root.leaf_for_point(self.data[self.n_labelled])
        self.assertTrue(self.n_labelled in leaf.labelled_index)

    def test_label_point_empty(self):
        with self.assertRaises(RuntimeError):
            self.mt1.label_point(1,1)

    def test_label_point_too_big(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        with self.assertRaises(ValueError):
            self.mt1.label_point(self.n_points+1,1)

    def test_label_point(self):
        val = 1
        lbda = 0.5
        seed = 1
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.label_point(self.n_labelled, val)
        self.assertEqual(self.mt1.labels[self.n_labelled],val)
        self.assertEqual(self.mt1._num_labelled, self.n_labelled + 1)
        leaf = self.mt1._root.leaf_for_point(self.data[self.n_labelled])
        # print(leaf.labelled_index)
        self.assertTrue(self.n_labelled in leaf.labelled_index)

    def test_add_data_point_bad(self):
        with self.assertRaises(TypeError):
            self.mt1.add_data_point(1)

    def test_add_data_point_empty(self):
        self.mt1.add_data_point([1]*self.d)
        self.assertEqual([[1]*self.d], self.mt1.points)
        self.assertEqual([None], self.mt1.labels)
        self.assertEqual(self.mt1._root.unlabelled_index,[0])
        self.assertEqual(self.mt1._root.labelled_index,[])

    def test_add_data_point_empty_2(self):
        self.mt1.add_data_point([1]*self.d,2)
        self.assertEqual([[1]*self.d], self.mt1.points)
        self.assertEqual([2], self.mt1.labels)
        self.assertEqual(self.mt1._root.unlabelled_index,[])
        self.assertEqual(self.mt1._root.labelled_index,[0])

    def test_add_data_point(self):
        lbda = 0.5
        seed = 1
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.update_life_time(lbda, set_seed=seed)

        self.mt1.add_data_point([1]*self.d)
        self.assertEqual(self.data + [[1]*self.d], self.mt1.points)
        self.assertEqual(self.labels + [None] * (self.n_points - self.n_labelled) + 
            [None], self.mt1.labels)
        leaf = self.mt1._root.leaf_for_point([1]*self.d)
        self.assertEqual(leaf.unlabelled_index[-1],self.n_points)
        self.assertEqual(len(self.mt1.points), self.mt1._num_points)

    def test_add_data_point_labelled(self):
        lbda = 0.5
        seed = 1
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.update_life_time(lbda, set_seed=seed)

        self.mt1.add_data_point([1]*self.d,1)
        self.assertEqual(self.data + [[1]*self.d], self.mt1.points)
        self.assertEqual(self.labels + [None] * (self.n_points - self.n_labelled) + 
            [1], self.mt1.labels)
        leaf = self.mt1._root.leaf_for_point([1]*self.d)
        self.assertEqual(leaf.labelled_index[-1],self.n_points)
        self.assertEqual(len(self.mt1.points), self.mt1._num_points)
        self.assertEqual(self.n_labelled + 1, self.mt1._num_labelled)

    ###########################################

    # Testing make leaf list 

    def test_make_full_leaf_list_root(self):
        self.mt1.make_full_leaf_list()
        self.assertEqual(len(self.mt1._full_leaf_list),1)

    def test_make_full_leaf_list(self):
        lbda = 1
        self.mt1.update_life_time(lbda,set_seed=1)
        self.mt1.make_full_leaf_list()
        # print(len(self.mt1._full_leaf_list))
        # for node in self.mt1._full_leaf_list:
        #     print(node.leaf_id)
        self.assertEqual(len(self.mt1._full_leaf_list),self.mt1._num_leaves)

    # Testing calculating leaf variances

    def test_make_full_leaf_var_list_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_var_list()
        self.assertEqual(utils.unbiased_var(self.labels), self.mt1._full_leaf_var_list[0])

    def test_make_full_leaf_var_list_empty(self):
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_var_list()
        self.assertEqual(0, self.mt1._full_leaf_var_list[0])

    def test_make_full_leaf_var_list(self):
        lbda = 0.5
        self.mt1.update_life_time(lbda, set_seed=100)

        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_var_list()

        for i, node in enumerate(self.mt1._full_leaf_list):
            node_labels = [self.mt1.labels[x] for x in node.labelled_index]
            # print(node_labels)
            if len(node_labels) != 0:
                temp_mean = sum(node_labels)/len(node_labels)
                # print(temp_mean)
                temp_var = 1/(len(node_labels)-1) * sum([(x-temp_mean)**2 for x in node_labels])
                self.assertTrue(abs(self.mt1._full_leaf_var_list[i] - temp_var) < 1e-9)
            else:
                self.assertEqual(self.mt1._full_leaf_var_list[i],0)

    # Testing calculating leaf mean

    def test_make_full_leaf_mean_list_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_mean_list()
        self.assertEqual(sum(self.labels)/self.n_labelled, self.mt1._full_leaf_mean_list[0])

    def test_make_full_leaf_mean_list_empty(self):
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_mean_list()
        self.assertEqual(0, self.mt1._full_leaf_mean_list[0])

    def test_make_full_leaf_mean_list(self):
        lbda = 0.5
        self.mt1.update_life_time(lbda, set_seed=100)

        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_mean_list()

        for i, node in enumerate(self.mt1._full_leaf_list):
            node_labels = [self.mt1.labels[x] for x in node.labelled_index]
            # print(node_labels)
            if len(node_labels) != 0:
                temp_mean = sum(node_labels)/len(node_labels)
                # print(temp_mean)
                self.assertTrue(abs(self.mt1._full_leaf_mean_list[i] - temp_mean) < 1e-9)
            else:
                self.assertEqual(self.mt1._full_leaf_mean_list[i],0)

    # Testing calculating leaf marginal probabilities

    def test_make_full_leaf_marginal_list_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_marginal_list()
        self.assertEqual(1, self.mt1._full_leaf_marginal_list[0])

    def test_make_full_leaf_marginal_list_empty(self):
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_marginal_list()
        self.assertEqual(0, self.mt1._full_leaf_marginal_list[0])

    def test_make_full_leaf_marginal_list(self):
        lbda = 0.5
        self.mt1.update_life_time(lbda, set_seed=100)

        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.make_full_leaf_list()
        self.mt1.make_full_leaf_marginal_list()

        for i, node in enumerate(self.mt1._full_leaf_list):
            node_points = (
                [self.mt1.points[x] for x in node.labelled_index]+
                [self.mt1.points[x] for x in node.unlabelled_index])
            # print(node_labels)
            temp_marginal = len(node_points)/self.mt1._num_points
            self.assertTrue(abs(self.mt1._full_leaf_marginal_list[i] - temp_marginal) < 1e-9)

    ###########################################

    # Testing using predict and get_point_in_same_leaf

    def test_predict_and_get_point_in_same_leaf_bad_input(self):
        with self.assertRaises(TypeError):
            self.mt1.predict(1)
            self.mt1.get_points_in_same_leaf(1)

    def test_predict_and_get_point_in_same_leaf_bad_input_2(self):
        with self.assertRaises(TypeError):
            self.mt1.predict('abc')
            self.mt1.get_points_in_same_leaf('abc')

    def test_predict_and_get_point_in_same_leaf_bad_length(self):
        with self.assertRaises(ValueError):
            self.mt1.predict([])
            self.mt1.get_points_in_same_leaf([])

    def test_predict_empty(self):
        with self.assertWarns(UserWarning):
            self.mt1.predict([0.5]*self.d)

    def test_predict_no_leaf_list(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_point = []
        for j in range(self.d):
            new_point.append(random.random())
        pred = self.mt1.predict(new_point)
        # print(pred)

        node = self.mt1._root.leaf_for_point(new_point)
        vals = [self.labels[x] for x in node.labelled_index]
        # print(len(vals))
        self.assertEqual(pred, sum(vals)/len(vals))

    def test_predict_leaf_list(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_point = []
        for j in range(self.d):
            new_point.append(random.random())
        pred = self.mt1.predict(new_point)
        # print(pred)

        node = self.mt1._root.leaf_for_point(new_point)
        vals = [self.labels[x] for x in node.labelled_index]
        # print(len(vals))
        self.assertEqual(pred, sum(vals)/len(vals))

    def test_predict_leaf_list_numpy(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_point = []
        for j in range(self.d):
            new_point.append(random.random())
        pred = self.mt1.predict(new_point)
        # print(pred)

        node = self.mt1._root.leaf_for_point(np.array(new_point))
        vals = [self.labels[x] for x in node.labelled_index]
        # print(len(vals))
        self.assertEqual(pred, sum(vals)/len(vals))

    def test_predict_multi_values(self):
        num_preds = 10
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_points = []
        for i in range(num_preds):
            new_point = []
            for j in range(self.d):
                new_point.append(random.random())
            new_points.append(new_point)
        preds = self.mt1.predict(new_points)
        # print(pred)

        check_preds = []
        for i in range(num_preds):

            node = self.mt1._root.leaf_for_point(np.array(new_points[i]))
            vals = [self.labels[x] for x in node.labelled_index]
            check_preds.append(sum(vals)/len(vals))
        # print(len(vals))
        self.assertAlmostEqual(preds, check_preds)

    def test_get_point_in_same_leaf_labelled(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_point = []
        for j in range(self.d):
            new_point.append(random.random())
        labelled_list = self.mt1.get_points_in_same_leaf(new_point)

        node = self.mt1._root.leaf_for_point(new_point)
        self.assertEqual(labelled_list,node.labelled_index)

    def test_get_point_in_same_leaf_unlabelled(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_point = []
        for j in range(self.d):
            new_point.append(random.random())
        unlabelled_list = self.mt1.get_points_in_same_leaf(new_point, 'unlabelled')

        node = self.mt1._root.leaf_for_point(new_point)
        self.assertEqual(unlabelled_list,node.unlabelled_index)

    def test_get_point_in_same_leaf_bad_list_name(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=100)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)

        random.seed(seed)
        new_point = []
        for j in range(self.d):
            new_point.append(random.random())
        with self.assertWarns(UserWarning):
            labelled_list = self.mt1.get_points_in_same_leaf(new_point, 'neither')

        node = self.mt1._root.leaf_for_point(new_point)
        self.assertEqual(labelled_list,node.labelled_index)

    ###########################################


    # Testing theoretical bounds

    def test_expected_split_bound(self):
        reps = 100
        tot = 0
        lbda = 5
        d = 3
        for i in range(reps):
            temp = Mondrian_Tree([[0,1]]*d)
            temp.update_life_time(lbda,set_seed=i)
            tot += temp._num_leaves - 1
        # print(tot/reps, ((1+lbda)*math.exp(1))**d)
        self.assertTrue(tot/reps< ((1+lbda)*math.exp(1))**d)


    def test_expected_cell_diameter_bounds(self):
        tot = 0
        lbda = 5
        self.mt1.update_life_time(lbda, set_seed=1)
        self.mt1.make_full_leaf_list()
        for node in self.mt1._full_leaf_list:
            tot += node.calculate_cell_l2_diameter()**2

        # print(tot/len(self.mt1._full_leaf_list), 4*self.d/lbda**2)
        self.assertTrue(tot/len(self.mt1._full_leaf_list) < 4*self.d/lbda**2)

    def test_probabilistic_cell_diameter_bounds(self):
        lbda = 5
        deltas = [0.1,0.2,0.3,0.4,0.5,1,1.5]
        self.mt1.update_life_time(lbda, set_seed=1)
        self.mt1.make_full_leaf_list()
        # print(len(self.mt1._full_leaf_list))
        for delta in deltas:
            tot = 0
            for node in self.mt1._full_leaf_list:
                tot += int(node.calculate_cell_l2_diameter() > delta)

            # print(tot/len(self.mt1._full_leaf_list), 
            #     self.d * (1+ (lbda * delta)/math.sqrt(self.d))*
            #     math.exp(-lbda * delta/math.sqrt(self.d)))
            self.assertTrue(tot/len(self.mt1._full_leaf_list) < 
                self.d * (1+ (lbda * delta)/math.sqrt(self.d))*
                math.exp(-lbda * delta/math.sqrt(self.d)))

    def test_limit_number_of_leaves(self):
        # n_values = [1,10,100,1000,10000,100000]
        if False:
            n_values = [1,10,100,1000]
            d_values = [1,3,5,10,20,50]
            seed = 1
            for d_val in d_values:
                test_tree = Mondrian_Tree([[0,1]]*d_val)
                print('d = {}'.format(d_val))
                for n_val in n_values:
                    test_tree.update_life_time(n_val**(1/(2+d_val)) - 1, set_seed=seed+n_val + d_val)
                    print(n_val, test_tree._num_leaves, test_tree._num_leaves/n_val)



    ###########################################

    # Testing data driven default values for prediction and active learning variance

    def test_set_default_pred_global_mean_empty(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.make_full_leaf_list()
        self.mt1.prediction_default_value = 1
        self.mt1.set_default_pred_global_mean()
        self.assertEqual(self.mt1.prediction_default_value, 0)

    def test_set_default_pred_global_mean(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.set_default_pred_global_mean()
        self.assertEqual(self.mt1.prediction_default_value, sum(self.labels)/self.n_labelled)

    def test_al_set_default_var_global_var_empty(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.make_full_leaf_list()
        self.mt1.al_default_var = 1
        self.mt1.al_set_default_var_global_var()
        self.assertEqual(self.mt1.al_default_var, 0)

    def test_al_set_default_var_global_var(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.make_full_leaf_list()
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_set_default_var_global_var()
        self.assertEqual(self.mt1.al_default_var, utils.unbiased_var(self.labels))

    ###########################################

    # Testing active learning parts

    def test_al_calculate_leaf_proportions_empty_root(self):
        with self.assertWarns(UserWarning):
            self.mt1.al_calculate_leaf_proportions()
        self.assertEqual(self.mt1._al_proportions, [1])

    def test_al_calculate_leaf_proportions_empty(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        with self.assertWarns(UserWarning):
            self.mt1.al_calculate_leaf_proportions()
        self.assertEqual(self.mt1._al_proportions, [1/self.mt1._num_leaves]*self.mt1._num_leaves)

    def test_al_calculate_leaf_proportions_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.assertEqual(self.mt1._al_proportions, [1])

    def test_al_calculate_leaf_proportions(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        temp_prop_list = []
        for i, node in enumerate(self.mt1._full_leaf_list):
            node_points = [x for x in node.labelled_index] + [x for x in node.unlabelled_index]
            # print(len(node_points))
            # print(self.mt1._full_leaf_marginal_list[i])
            if len(node_points) != 0:
                temp_var = utils.unbiased_var([self.labels[x] for x in node.labelled_index])
                # print(self.mt1._al_proportions[i])
                # print(math.sqrt(temp_var * (len(node_labels)/self.n_points)))
                temp_prop_list.append(math.sqrt(temp_var * (len(node_points)/self.n_points)))
                
            else:
                self.assertEqual(self.mt1._al_proportions[i],0)

        normalizer = sum(temp_prop_list)
        temp_prop_list = [x/normalizer for x in temp_prop_list]
        # print(temp_prop_list)
        for i, val in enumerate(temp_prop_list):
            # print(val, self.mt1._al_proportions[i])
            self.assertTrue(abs(self.mt1._al_proportions[i] - val) < 1e-9)

    def test_al_calculate_leaf_number_new_labels_empty(self):
        with self.assertRaises(ValueError):
            self.mt1.al_calculate_leaf_number_new_labels(1)

    def test_al_calculate_leaf_number_new_labels_too_many_labelled(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        with self.assertRaises(ValueError):
            self.mt1.al_calculate_leaf_number_new_labels(1)

    def test_al_calculate_leaf_number_new_labels_too_few_points(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        with self.assertRaises(ValueError):
            self.mt1.al_calculate_leaf_number_new_labels(101)

    def test_al_calculate_leaf_number_new_labels_bad_round_by(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        with self.assertRaises(ValueError):
            self.mt1.al_calculate_leaf_number_new_labels(21,round_by = 'bad')

    def test_al_calculate_leaf_number_new_labels_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.mt1.al_calculate_leaf_number_new_labels(21)
        self.assertEqual(self.mt1._al_leaf_number_new_labels,[1])

    def test_al_calculate_leaf_number_new_labels_single(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        with self.assertWarns(UserWarning):
            self.mt1.al_calculate_leaf_number_new_labels(21)
        # print(self.mt1._al_leaf_number_new_labels)
        self.assertEqual(sum(self.mt1._al_leaf_number_new_labels),1)
        
        # for i, node in enumerate(self.mt1._full_leaf_list):
        #     curr_num = len(node.labelled_index)
        #     tot_num = curr_num + self.mt1._al_leaf_number_new_labels[i]
        #     print(self.mt1._al_leaf_number_new_labels[i],tot_num, self.mt1._al_proportions[i])

    def test_al_calculate_leaf_number_new_labels_many(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.mt1.al_calculate_leaf_number_new_labels(40)
        # print(self.mt1._al_leaf_number_new_labels)
        self.assertEqual(sum(self.mt1._al_leaf_number_new_labels),20)

        # for i, node in enumerate(self.mt1._full_leaf_list):
        #     curr_num = len(node.labelled_index)
        #     tot_num = curr_num + self.mt1._al_leaf_number_new_labels[i]
        #     print(self.mt1._al_leaf_number_new_labels[i],tot_num, self.mt1._al_proportions[i])

    # def test_al_calculate_leaf_number_new_labels_incomplete(self):
          # This is always a possible source of weird behaviour... Keep thinking about these heurisitcs
    #     self.assertTrue(False, 'Do more testing for this function. Both auto and visual. '
    #         'And read the function code for more bugs.')

    def test_al_calculate_point_probabilities_proportions_empty(self):
        with self.assertWarns(UserWarning):
            self.mt1.al_calculate_leaf_proportions()
            self.mt1.al_calculate_point_probabilities_proportions()
        self.assertEqual(self.mt1._al_point_weights_proportional,[])

    def test_al_calculate_point_probabilities_proportions_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.mt1.al_calculate_point_probabilities_proportions()
        self.assertEqual(self.mt1._al_point_weights_proportional,
            [None] * 20 + [1/(self.n_points - self.n_labelled)] * 
            (self.n_points - self.n_labelled))

    def test_al_calculate_point_probabilities_proportions(self):
        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.mt1.al_calculate_point_probabilities_proportions()
        for i, node in enumerate(self.mt1._full_leaf_list):
            tot = 0
            for ind in node.unlabelled_index:
                tot += self.mt1._al_point_weights_proportional[ind]

            self.assertTrue(abs(tot - self.mt1._al_proportions[i]) < 1e-9)

    def test_al_calculate_point_probabilities_adjustment_empty(self):
        with self.assertWarns(UserWarning):
            self.mt1.al_calculate_leaf_proportions()
            self.mt1.al_calculate_point_probabilities_adjustment(1)
        self.assertEqual(self.mt1._al_point_weights_adjustment,[])

    def test_al_calculate_point_probabilities_adjustment_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.mt1.al_calculate_point_probabilities_adjustment(21)
        for val in self.mt1._al_point_weights_adjustment:
            if val is not None:  
                self.assertAlmostEqual(val,1/(self.n_points - self.n_labelled))

    def test_al_calculate_point_probabilities_adjustment(self):

        # TODO: Try and improve this test. It passing is not very informative

        lbda = 0.5
        seed = 1
        self.mt1.update_life_time(lbda, set_seed=seed)
        self.mt1.input_data(self.data, self.labelled_indices, self.labels)
        self.mt1.al_calculate_leaf_proportions()
        self.mt1.al_calculate_point_probabilities_adjustment(21)
        self.assertAlmostEqual(sum([x for x in self.mt1._al_point_weights_adjustment if x]),1)

        # for val in self.mt1._al_point_weights_adjustment:
        #     if not None:
        #         print(val)

    ###########################################

    # Checking reasonable performance of tree

    def test_constant_value_performance_root(self):
        self.mt1.input_data(self.data, self.labelled_indices, [1]*self.n_labelled)
        self.assertEqual(self.mt1.predict([0.5]*self.d),1)

    def test_constant_value_performance(self):
        seed = 1
        self.mt1.input_data(self.data, self.labelled_indices, [1]*self.n_labelled)
        self.mt1.update_life_time(0.5,set_seed=seed)
        self.assertEqual(self.mt1.predict([0.5]*self.d),1)

    def test_OLS_noiseless_better_than_mean(self):
        seed = 1
        labs = []
        for i in self.data[:self.n_labelled]:
            labs.append(sum(i))
        self.mt1.input_data(self.data, self.labelled_indices, labs)
        self.mt1.update_life_time(0.5,set_seed=seed)
        self.mt1.make_full_leaf_list()
        # for i, node  in enumerate(self.mt1._full_leaf_list):
        #     print(len(node.labelled_index))
        test_labs = []
        for i in self.data[self.n_labelled:]:
            test_labs.append(sum(i))
        test_mean = sum(test_labs) / len(test_labs)
        SST = 0
        SSE = 0

        for point in self.data[self.n_labelled:]:
            SST += (sum(point) - test_mean)**2
            SSE += (sum(point) - self.mt1.predict(point))**2

        # print(SST, SSE)
        self.assertTrue(SST > SSE)

    def test_OLS_better_than_mean(self):
        seed = 1
        std = 0.1
        labs = []
        for i in self.data[:self.n_labelled]:
            val = sum(i) + random.normalvariate(0,std)
            # print(sum(i),val)
            labs.append(val)
        self.mt1.input_data(self.data, self.labelled_indices, labs)
        self.mt1.update_life_time(0.5,set_seed=seed)
        self.mt1.make_full_leaf_list()
        # for i, node  in enumerate(self.mt1._full_leaf_list):
        #     print(len(node.labelled_index))
        test_labs = []
        for i in self.data[self.n_labelled:]:
            test_labs.append(sum(i) + random.normalvariate(0,std))
        test_mean = sum(test_labs) / len(test_labs)
        SST = 0
        SSE = 0

        for point in self.data[self.n_labelled:]:
            SST += (sum(point) - test_mean)**2
            SSE += (sum(point) - self.mt1.predict(point))**2

        # print(SST, SSE)
        self.assertTrue(SST > SSE)

if __name__ == '__main__':
    unittest.main()