import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report

data = pd.read_csv(r"ar41_for_ulb.csv", delimiter=';')

# Drop rows where any of the elements is NAN
data = data.dropna()

# Data Preprocessing
# Assuming 'timestamps_UTC' is the timestamp column
data['timestamps_UTC'] = pd.to_datetime(data['timestamps_UTC'])

# Select relevant features (assuming you want to detect anomalies in temperature, pressure, and RPM)
selected_features = ['RS_E_InAirTemp_PC1', 'RS_E_InAirTemp_PC2', 'RS_E_OilPress_PC1', 'RS_E_OilPress_PC2', 'RS_E_RPM_PC1', 'RS_E_RPM_PC2']

# Create a subset of the data with selected features
data_subset = data[selected_features]

# Data Preprocessing
scaler = StandardScaler()
data_subset_scaled = scaler.fit_transform(data_subset)

# Isolation Forest
iso_forest = IsolationForest(contamination=0.05, random_state=0)
iso_forest.fit(data_subset_scaled)

# One-Class SVM
one_class_svm = OneClassSVM(nu=0.05)
one_class_svm.fit(data_subset_scaled)

# Elliptic Envelope
elliptic_envelope = EllipticEnvelope(contamination=0.05)
elliptic_envelope.fit(data_subset_scaled)

# Ensemble method using VotingClassifier
voting_classifier = VotingClassifier(estimators=[
    ('Isolation Forest', iso_forest),
    ('One-Class SVM', one_class_svm),
    ('Elliptic Envelope', elliptic_envelope)
], voting='hard')

# Fit the ensemble model
voting_classifier.fit(data_subset_scaled)

# Predict anomalies using the ensemble model
anomaly_predictions = voting_classifier.predict(data_subset_scaled)

# Append the anomaly predictions to the original DataFrame
data['Anomaly'] = anomaly_predictions

# Print the classification report to assess the performance of the ensemble model
print(classification_report(data['Anomaly'], np.ones(len(data))))

# You can further fine-tune the models and explore other anomaly detection methods based on your specific dataset and requirements.
