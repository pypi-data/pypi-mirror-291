from abc import ABC, abstractmethod
import os
from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
import copy
from sklearn.base import TransformerMixin
import networkx as nx

from .utils import (
    leave_pair_out_cv,
    leave_group_out_cv,
    randomize_graph,
    permute_features,
)


class Dataset(ABC):
    """
    Abstract wrapper class for datasets.
    """

    @abstractmethod
    def load(self, path: str):
        """
        Loads the dataset from data.
        """
        pass

    @abstractmethod
    def save(self, path: str):
        """
        Saves the dataset to data.
        """
        pass


class DrugResponseDataset(Dataset):
    """
    Drug response dataset.
    """

    def __init__(
        self,
        response: Optional[ArrayLike] = None,
        cell_line_ids: Optional[ArrayLike] = None,
        drug_ids: Optional[ArrayLike] = None,
        predictions: Optional[ArrayLike] = None,
        dataset_name: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Initializes the drug response dataset.
        :param response: drug response values per cell line and drug
        :param cell_line_ids: cell line IDs
        :param drug_ids: drug IDs
        :param predictions: optional. Predicted drug response values per cell line and drug
        :param dataset_name: optional. Name of the dataset

        Variables:
        response: drug response values per cell line and drug
        cell_line_ids: cell line IDs
        drug_ids: drug IDs
        predictions: optional. Predicted drug response values per cell line and drug
        dataset_name: optional. Name of the dataset
        cv_splits: optional. List of DrugResponseDatasets (cross validation splits)
        """
        super(DrugResponseDataset, self).__init__()
        if response is not None:
            self.response = np.array(response)
            self.cell_line_ids = np.array(cell_line_ids)
            self.drug_ids = np.array(drug_ids)
            assert len(self.response) == len(
                self.cell_line_ids
            ), "response and cell_line_ids have different lengths"
            assert len(self.response) == len(
                self.drug_ids
            ), "response and drug_ids/cell_line_ids have different lengths"
            self.dataset_name = dataset_name
        else:
            self.response = response
            self.cell_line_ids = cell_line_ids
            self.drug_ids = drug_ids
            self.dataset_name = dataset_name

        if predictions is not None:
            self.predictions = np.array(predictions)
            assert len(self.predictions) == len(
                self.response
            ), "predictions and response have different lengths"
        else:
            self.predictions = None
        self.cv_splits = None

    def __len__(self):
        return len(self.response)

    def __str__(self):
        if len(self.response) > 3:
            string = f"DrugResponseDataset: CLs {self.cell_line_ids[:3]}...; Drugs {self.drug_ids[:3]}...; Response {self.response[:3]}..."
        else:
            string = f"DrugResponseDataset: CLs {self.cell_line_ids}; Drugs {self.drug_ids}; Response {self.response}"
        if self.predictions is not None:
            if len(self.predictions) > 3:
                string += f"; Predictions {self.predictions[:3]}..."
            else:
                string += f"; Predictions {self.predictions}"
        return string

    def load(self, path: str):
        """
        Loads the drug response dataset from data.
        """
        data = pd.read_csv(path)
        self.response = data["response"].values
        self.cell_line_ids = data["cell_line_ids"].values
        self.drug_ids = data["drug_ids"].values
        if "predictions" in data.columns:
            self.predictions = data["predictions"].values

    def save(self, path: str):
        """
        Saves the drug response dataset to data.
        """
        out = pd.DataFrame(
            {
                "cell_line_ids": self.cell_line_ids,
                "drug_ids": self.drug_ids,
                "response": self.response,
            }
        )
        if self.predictions is not None:
            out["predictions"] = self.predictions
        out.to_csv(path, index=False)

    def add_rows(self, other: "DrugResponseDataset") -> None:
        """
        Adds rows from another dataset.
        :other: other dataset
        """
        self.response = np.concatenate([self.response, other.response])
        self.cell_line_ids = np.concatenate([self.cell_line_ids, other.cell_line_ids])
        self.drug_ids = np.concatenate([self.drug_ids, other.drug_ids])

        if self.predictions is not None and other.predictions is not None:
            self.predictions = np.concatenate([self.predictions, other.predictions])

    def remove_nan_responses(self) -> None:
        """
        Removes rows with NaN values in the repsonse
        """
        mask = np.isnan(self.response)
        self.response = self.response[~mask]
        self.cell_line_ids = self.cell_line_ids[~mask]
        self.drug_ids = self.drug_ids[~mask]
        if self.predictions is not None:
            self.predictions = self.predictions[~mask]

    def shuffle(self, random_state: int = 42) -> None:
        """
        Shuffles the dataset.
        :random_state: random state
        """
        indices = np.arange(len(self.response))
        np.random.seed(random_state)
        np.random.shuffle(indices)
        self.response = self.response[indices]
        self.cell_line_ids = self.cell_line_ids[indices]
        self.drug_ids = self.drug_ids[indices]
        if self.predictions is not None:
            self.predictions = self.predictions[indices]

    def remove_drugs(self, drugs_to_remove: Union[str, list]) -> None:
        """
        Removes drugs from the dataset.
        :drugs_to_remove: name of drug or list of names of multiple drugs to remove
        """
        if isinstance(drugs_to_remove, str):
            drugs_to_remove = [drugs_to_remove]

        mask = [drug not in drugs_to_remove for drug in self.drug_ids]
        self.drug_ids = self.drug_ids[mask]
        self.cell_line_ids = self.cell_line_ids[mask]
        self.response = self.response[mask]

    def remove_cell_lines(self, cell_lines_to_remove: Union[str, list]) -> None:
        """
        Removes cell lines from the dataset.
        :cell_lines_to_remove: name of cell line or list of names of multiple cell lines to remove
        """
        if isinstance(cell_lines_to_remove, str):
            cell_lines_to_remove = [cell_lines_to_remove]

        mask = [
            cell_line not in cell_lines_to_remove for cell_line in self.cell_line_ids
        ]
        self.drug_ids = self.drug_ids[mask]
        self.cell_line_ids = self.cell_line_ids[mask]
        self.response = self.response[mask]

    def remove_rows(self, indices: ArrayLike) -> None:
        """
        Removes rows from the dataset.
        :indices: indices of rows to remove
        """
        self.drug_ids = np.delete(self.drug_ids, indices)
        self.cell_line_ids = np.delete(self.cell_line_ids, indices)
        self.response = np.delete(self.response, indices)
        if self.predictions is not None:
            self.predictions = np.delete(self.predictions, indices)

    def reduce_to(
        self, cell_line_ids: Optional[ArrayLike], drug_ids: Optional[ArrayLike]
    ) -> None:
        """
        Removes all rows which contain a cell_line not in cell_line_ids or a drug not in drug_ids
        :cell_line_ids: cell line IDs or None to keep all cell lines
        :drug_ids: drug IDs or None to keep all cell lines
        """
        if drug_ids is not None:
            self.remove_drugs(list(set(self.drug_ids) - set(drug_ids)))

        if cell_line_ids is not None:
            self.remove_cell_lines(list(set(self.cell_line_ids) - set(cell_line_ids)))

    def split_dataset(
        self,
        n_cv_splits,
        mode,
        split_validation=True,
        split_early_stopping=True,
        validation_ratio=0.1,
        random_state=42,
    ) -> List[dict]:
        """
        Splits the dataset into training, validation and test sets for crossvalidation
        :param mode: split mode (LPO=Leave-random-Pairs-Out, LCO=Leave-Cell-line-Out, LDO=Leave-Drug-Out)
        :return: training, validation and test sets
        """
        cell_line_ids = self.cell_line_ids
        drug_ids = self.drug_ids
        response = self.response

        if mode == "LPO":
            cv_splits = leave_pair_out_cv(
                n_cv_splits,
                response,
                cell_line_ids,
                drug_ids,
                split_validation,
                validation_ratio,
                random_state,
                self.dataset_name,
            )

        elif mode in ["LCO", "LDO"]:
            group = "cell_line" if mode == "LCO" else "drug"
            cv_splits = leave_group_out_cv(
                group=group,
                n_cv_splits=n_cv_splits,
                response=response,
                cell_line_ids=cell_line_ids,
                drug_ids=drug_ids,
                split_validation=split_validation,
                validation_ratio=validation_ratio,
                random_state=random_state,
                dataset_name=self.dataset_name,
            )
        else:
            raise ValueError(
                f"Unknown split mode '{mode}'. Choose from 'LPO', 'LCO', 'LDO'."
            )

        if split_validation and split_early_stopping:
            for split in cv_splits:
                validation_es, early_stopping = split_early_stopping_data(
                    split["validation"], test_mode=mode
                )
                split["validation_es"] = validation_es
                split["early_stopping"] = early_stopping
        self.cv_splits = cv_splits
        return cv_splits

    def save_splits(self, path: str) -> None:
        """
        Save cross validation splits to
        path/cv_split_0_train.csv
        path/cv_split_0_test.csv
        ...
        """
        assert (
            self.cv_splits is not None
        ), "trying to save splits, but DrugResponseDataset was not split."
        os.makedirs(path, exist_ok=True)
        for i, split in enumerate(self.cv_splits):

            for mode in [
                "train",
                "validation",
                "test",
                "validation_es",
                "early_stopping",
            ]:
                if mode in split:
                    split_path = os.path.join(path, f"cv_split_{i}_{mode}.csv")
                    split[mode].save(path=split_path)

    def load_splits(self, path: str) -> None:
        """
        Load cross validation splits from
        path/cv_split_0_train.csv
        path/cv_split_0_test.csv
        ...
        """
        files = os.listdir(path)
        files = [
            file
            for file in files
            if (file.endswith(".csv") and file.startswith("cv_split"))
        ]
        assert len(files) > 0, f"No cv split files found in {path}"

        train_splits = [file for file in files if "train" in file]
        test_splits = [file for file in files if "test" in file]

        validation_es_splits = [file for file in files if "validation_es" in file]
        validation_splits = [
            file
            for file in files
            if "validation" in file and file not in validation_es_splits
        ]
        early_stopping_splits = [file for file in files if "early_stopping" in file]

        for ds in [
            train_splits,
            test_splits,
            validation_splits,
            validation_es_splits,
            early_stopping_splits,
        ]:
            ds.sort()

        optional_splits = {
            "validation": validation_splits,
            "validation_es": validation_es_splits,
            "early_stopping": early_stopping_splits,
        }
        self.cv_splits = []

        for split_train, split_test in zip(train_splits, test_splits):
            tr_split = DrugResponseDataset(dataset_name=self.dataset_name)
            tr_split.load(os.path.join(path, split_train))

            te_split = DrugResponseDataset(dataset_name=self.dataset_name)
            te_split.load(os.path.join(path, split_test))
            self.cv_splits.append({"train": tr_split, "test": te_split})

        for mode in ["validation", "validation_es", "early_stopping"]:
            if len(optional_splits[mode]) > 0:
                for i, v_split in enumerate(optional_splits[mode]):
                    split = DrugResponseDataset(dataset_name=self.dataset_name)
                    split.load(os.path.join(path, v_split))
                    self.cv_splits[i][mode] = split

    def copy(self):
        """
        Returns a copy of the drug response dataset.
        """
        return DrugResponseDataset(
            response=copy.deepcopy(self.response),
            cell_line_ids=copy.deepcopy(self.cell_line_ids),
            drug_ids=copy.deepcopy(self.drug_ids),
            predictions=copy.deepcopy(self.predictions),
            dataset_name=self.dataset_name,
        )

    def __hash__(self):
        return hash(
            (
                self.dataset_name,
                tuple(self.cell_line_ids),
                tuple(self.drug_ids),
                tuple(self.response),
                tuple(self.predictions) if self.predictions is not None else None,
            )
        )

    def mask(self, mask: List[bool]) -> None:
        """
        Masks the dataset.
        :mask: boolean mask
        """
        self.response = self.response[mask]
        self.cell_line_ids = self.cell_line_ids[mask]
        self.drug_ids = self.drug_ids[mask]
        if self.predictions is not None:
            self.predictions = self.predictions[mask]

    def transform(self, response_transformation: TransformerMixin) -> None:
        """Apply transformation to the response data and prediction data of the dataset."""
        self.response = response_transformation.transform(
            self.response.reshape(-1, 1)
        ).squeeze()
        if self.predictions is not None:
            self.predictions = response_transformation.transform(
                self.predictions.reshape(-1, 1)
            ).squeeze()

    def fit_transform(self, response_transformation: TransformerMixin) -> None:
        """Fit and transform the response data and prediction data of the dataset."""
        response_transformation.fit(self.response.reshape(-1, 1)).squeeze()
        self.transform(response_transformation)

    def inverse_transform(self, response_transformation: TransformerMixin) -> None:
        """Inverse transform the response data and prediction data of the dataset."""
        self.response = response_transformation.inverse_transform(
            self.response.reshape(-1, 1)
        ).squeeze()
        if self.predictions is not None:
            self.predictions = response_transformation.inverse_transform(
                self.predictions.reshape(-1, 1)
            ).squeeze()


def split_early_stopping_data(
    validation_dataset: DrugResponseDataset, test_mode: str
) -> Tuple[DrugResponseDataset, DrugResponseDataset]:

    validation_dataset.shuffle(random_state=42)
    cv_v = validation_dataset.split_dataset(
        n_cv_splits=4,
        mode=test_mode,
        split_validation=False,
        split_early_stopping=False,
        random_state=42,
    )
    # take the first fold of a 4 cv as the split ie. 3/4 for validation and 1/4 for early stopping
    validation_dataset = cv_v[0]["train"]
    early_stopping_dataset = cv_v[0]["test"]
    return validation_dataset, early_stopping_dataset


class FeatureDataset(Dataset):
    """
    Class for feature datasets.
    """

    def __init__(
        self,
        features: Dict[str, Dict[str, Any]],
        meta_info: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ):
        """
        Initializes the feature dataset.
        :features: dictionary of features, key: drug ID/cell line ID, value: Dict of feature views, key: feature name, value: feature vector
        :meta_info: additional information for the views, e.g., gene names for gene expression
        """
        super(FeatureDataset, self).__init__()
        self.features = features
        self.view_names = self.get_view_names()
        if meta_info is not None:
            # assert that str of meta Dict[str, Any] is in view_names
            assert all(
                [meta_key in self.view_names for meta_key in meta_info.keys()]
            ), f"Meta keys {meta_info.keys()} not in view names {self.view_names}"
            self.meta_info = meta_info
        self.identifiers = self.get_ids()

    def save(self, path: str):
        """
        Saves the feature dataset to data.
        """
        raise NotImplementedError("save method not implemented")

    def load(self, path: str):
        """
        Loads the feature dataset from data.
        """
        raise NotImplementedError("load method not implemented")

    def randomize_features(
        self, views_to_randomize: Union[str, list], randomization_type: str
    ) -> None:
        """
        Randomizes the feature vectors.
        :views_to_randomize: name of feature view or list of names of multiple feature views to randomize. The other views are not randomized.
        :randomization_type: randomization type ('permutation', 'invariant').
        Permutation permutes the feature vectors.
        Invariant means that the randomization is done in a way that a key characteristic of the feature is preserved. In case of matrices, this is the mean and standard deviation of the feature view for this instance, for networks it is the degree distribution.
        """
        assert randomization_type in [
            "permutation",
            "invariant",
        ], f"Unknown randomization type '{randomization_type}'. Choose from 'permutation', 'invariant'."

        if isinstance(views_to_randomize, str):
            views_to_randomize = [views_to_randomize]

        if randomization_type == "permutation":
            # Permute the specified views for each entity (= cell line or drug) E.g. each cell line gets the feature vector/graph/image... of another cell line. Drawn without replacement.
            self.features = permute_features(
                features=self.features,
                views_to_permute=views_to_randomize,
                identifiers=self.identifiers,
                all_views=self.view_names,
            )

        elif randomization_type == "invariant":
            # Invariant randomization: Randomize the specified views for each entity in a way that a key characteristic of the feature is preserved. For vectors this is the mean and standard deviation the feature view for this instance, for networks the degree distribution.
            for view in views_to_randomize:
                for identifier in self.identifiers:
                    if type(self.features[identifier][view]) is np.ndarray:
                        new_features = np.random.normal(
                            self.features[identifier][view].mean(),
                            self.features[identifier][view].std(),
                            self.features[identifier][view].shape,
                        )
                    elif type(self.features[identifier][view]) is nx.Graph:
                        new_features = randomize_graph(self.features[identifier][view])

                    else:
                        raise ValueError(
                            f"No invariant randomization available for feature view type '{type(self.features[identifier][view])}'."
                        )
                    self.features[identifier][view] = new_features

    def get_ids(self):
        """
        returns drug ids of the dataset
        """
        return list(self.features.keys())

    def get_view_names(self):
        """
        returns feature view names
        """
        return list(self.features[list(self.features.keys())[0]].keys())

    def get_feature_matrix(
        self, view: str, identifiers: ArrayLike, stack: bool = True
    ) -> Union[np.ndarray, List]:
        """
        Returns the feature matrix for the given view. The feature view must be a vector or matrix.
        :param view: view name
        :param identifiers: list of identifiers (cell lines oder drugs)
        :param stack: if True, stacks the feature vectors to a matrix. If False, returns a list of features.
        :return: feature matrix
        """
        assert view in self.view_names, f"View '{view}' not in in the FeatureDataset."
        missing_identifiers = {
            id_ for id_ in identifiers if id_ not in self.identifiers
        }
        assert (
            not missing_identifiers
        ), f"{len(missing_identifiers)} of {len(np.unique(identifiers))} ids are not in the FeatureDataset. Missing ids: {missing_identifiers}"

        assert all(
            len(self.features[id_][view]) == len(self.features[identifiers[0]][view])
            for id_ in identifiers
        ), f"Feature vectors of view {view} have different lengths."

        assert all(
            type(self.features[id_][view]) is np.ndarray for id_ in identifiers
        ), f"get_feature_matrix only works for vectors or matrices. {view} is not a numpy array."
        out = [self.features[id_][view] for id_ in identifiers]
        return np.stack(out, axis=0) if stack else out

    def copy(self):
        """
        Returns a copy of the feature dataset.
        """
        return FeatureDataset(features=copy.deepcopy(self.features))

    def add_features(self, other: "FeatureDataset") -> None:
        """
        Adds features views from another dataset. Inner join (only common identifiers are kept).
        :other: other dataset
        """
        assert (
            len(set(self.view_names) & set(other.view_names)) == 0
        ), "Trying to add features but feature views overlap. FeatureDatasets should be distinct."
        self.add_meta_info(other)

        common_identifiers = set(self.identifiers).intersection(other.identifiers)
        new_features = {}
        for id_ in common_identifiers:
            new_features[id_] = {
                view: self.features[id_][view] for view in self.view_names
            }
            for view in other.view_names:
                new_features[id_][view] = other.features[id_][view]

        self.features = new_features
        self.view_names = self.get_view_names()
        self.identifiers = self.get_ids()

    def add_meta_info(self, other: "FeatureDataset") -> None:
        """
        Adds meta information to the feature dataset.
        :other: other dataset
        """
        other_meta = other.meta_info
        self.meta_info.update(other_meta)
