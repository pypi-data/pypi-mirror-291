import grpc
from pryvx import pryvx_pb2
from pryvx import pryvx_pb2_grpc
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import IsolationForest
import requests
import pickle

class Client:

    @staticmethod
    def train_logistic_regression(X, y):
        """
        Trains a logistic regression model using the provided features and target labels.
        
        Parameters:
        X (pd.DataFrame or np.ndarray): Features for training.
        y (pd.Series or np.ndarray): Target labels.

        Returns:
        LogisticRegression: Trained logistic regression model.
        """
        model = LogisticRegression()
        model.fit(X, y)
        return model
    

    @staticmethod
    def train_linear_regression(X, y):
        model = LinearRegression()
        model.fit(X, y)
        return model
    

    @staticmethod
    def train_iosolation_forest(X):
        model = IsolationForest()
        model.fit(X)
        return model
    
    
    @staticmethod
    def send_model_to_server(trained_model, PROJECT_ID, COLLABORATOR_ID, CLIENT_SECRET_KEY):
        # Serialize the model parameters using pickle
        serialized_params = pickle.dumps(trained_model)

        # Headers containing project_id, collaborator_id and client_key
        headers = {
            "projectId": PROJECT_ID,
            "collaboratorId": COLLABORATOR_ID,
            "clientSecretKey": CLIENT_SECRET_KEY,
        }

        # endpoint
        url = "https://api.pryvx.com/send-params"

        response = requests.post(url, data=serialized_params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()
        else:
            # Print an error message if the request failed
            return "Error:", response.text


def train(features, labels):
    model = LogisticRegression()
    model.fit(features, labels)

    serialized_model = pickle.dumps(model)

    return serialized_model


def send_params(serialized_model, connection_url):

    with grpc.insecure_channel(connection_url) as channel:
        stub = pryvx_pb2_grpc.ModelServiceStub(channel)

        model_params = pryvx_pb2.ModelParams(params=serialized_model)

        response = stub.SendModelParams(model_params)

        return "Model Params sent to server"


