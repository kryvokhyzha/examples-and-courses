import math

import numpy as np
import torch
from catboost.datasets import msrank_10k
from sklearn.preprocessing import StandardScaler

from typing import List


class ListNet(torch.nn.Module):
    def __init__(self, num_input_features, hidden_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.model = torch.nn.Sequential(
            torch.nn.Linear(num_input_features, self.hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(self.hidden_dim, 1),
        )

    def forward(self, input_1):
        logits = self.model(input_1)
        return logits


class Solution:
    def __init__(self, n_epochs: int = 5, listnet_hidden_dim: int = 30,
                 lr: float = 0.001, ndcg_top_k: int = 10):
        self._prepare_data()
        self.num_input_features = self.X_train.shape[1]
        self.ndcg_top_k = ndcg_top_k
        self.n_epochs = n_epochs

        self.model = self._create_model(
            self.num_input_features, listnet_hidden_dim)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

    def _get_data(self) -> List[np.ndarray]:
        train_df, test_df = msrank_10k()

        X_train = train_df.drop([0, 1], axis=1).values
        y_train = train_df[0].values
        query_ids_train = train_df[1].values.astype(int)

        X_test = test_df.drop([0, 1], axis=1).values
        y_test = test_df[0].values
        query_ids_test = test_df[1].values.astype(int)

        return [X_train, y_train, query_ids_train, X_test, y_test, query_ids_test]

    def _prepare_data(self) -> None:
        (X_train, y_train, self.query_ids_train,
            X_test, y_test, self.query_ids_test) = self._get_data()

        X_train = self._scale_features_in_query_groups(
            X_train, self.query_ids_train)
        X_test = self._scale_features_in_query_groups(
            X_test, self.query_ids_train)

        self.X_train = torch.FloatTensor(X_train)
        self.X_test = torch.FloatTensor(X_test)

        self.ys_train = torch.FloatTensor(y_train)
        self.ys_test = torch.FloatTensor(y_test)

    def _scale_features_in_query_groups(self, inp_feat_array: np.ndarray,
                                        inp_query_ids: np.ndarray) -> np.ndarray:
        for cur_id in np.unique(inp_query_ids):
            mask = inp_query_ids == cur_id
            tmp_array = inp_feat_array[mask]
            scaler = StandardScaler()
            inp_feat_array[mask] = scaler.fit_transform(tmp_array)

        return inp_feat_array

    def _create_model(self, listnet_num_input_features: int,
                      listnet_hidden_dim: int) -> torch.nn.Module:
        torch.manual_seed(0)
        net = ListNet(num_input_features=listnet_num_input_features,
                      hidden_dim=listnet_hidden_dim)
        return net

    def fit(self) -> List[float]:
        metrics = []
        for epoch_no in range(1, self.n_epochs + 1):
            self._train_one_epoch()
            ep_metric = self._eval_test_set()
            metrics.append(ep_metric)
        return metrics

    def save_model(self, path='listnet_lec3.pth'):
        f = open(path, 'wb')
        torch.save(self.model.state_dict, f)

    def load_model(self, path='listnet_lec3.pth'):
        f = open(path, 'rb')
        state_dict = torch.load(f)
        self.model.load_state_dict(state_dict)

    def _calc_loss(self, batch_ys: torch.FloatTensor,
                   batch_pred: torch.FloatTensor) -> torch.FloatTensor:
        P_y_i = torch.softmax(batch_ys, dim=0)
        P_z_i = torch.softmax(batch_pred, dim=0)
        return -torch.sum(P_y_i * torch.log(P_z_i/P_y_i))

    def _train_one_epoch(self):
        self.model.train()
        for cur_id in np.unique(self.query_ids_train):
            mask_train = self.query_ids_train == cur_id
            batch_X = self.X_train[mask_train]
            batch_ys = self.ys_train[mask_train]

            self.optimizer.zero_grad()
            batch_pred = self.model(batch_X).reshape(-1, )
            batch_loss = self._calc_loss(batch_ys, batch_pred)
            batch_loss.backward(retain_graph=True)
            self.optimizer.step()

    def _eval_test_set(self) -> float:
        with torch.no_grad():
            self.model.eval()
            ndcgs = []
            for cur_id in np.unique(self.query_ids_test):
                mask = self.query_ids_test == cur_id
                X_test_tmp = self.X_test[mask]
                valid_pred = self.model(X_test_tmp)
                ndcg_score = self._ndcg_k(
                    self.ys_test[mask], valid_pred, self.ndcg_top_k)
                if np.isnan(ndcg_score):
                    ndcgs.append(0)
                    continue
                ndcgs.append(ndcg_score)
            return np.mean(ndcgs)

    def _ndcg_k(self, ys_true, ys_pred, ndcg_top_k) -> float:
        def dcg(ys_true, ys_pred):
            _, argsort = torch.sort(ys_pred, descending=True, dim=0)
            argsort = argsort[:ndcg_top_k]
            ys_true_sorted = ys_true[argsort]
            ret = 0
            for i, l in enumerate(ys_true_sorted, 1):
                ret += (2 ** l - 1) / math.log2(1 + i)
            return ret
        ideal_dcg = dcg(ys_true, ys_true)
        pred_dcg = dcg(ys_true, ys_pred)
        return (pred_dcg / ideal_dcg).item()


