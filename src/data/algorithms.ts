export interface TrainingField {
  name: string;
  label: string;
  type: "text" | "number" | "select";
  options?: string[];
  defaultValue?: string | number;
  description: string;
}

export interface Algorithm {
  id: string;
  name: string;
  category: string;
  useCase: string;
  useCaseDetails: string[];
  trainingFields: TrainingField[];
  modelFile: string;
}

export const algorithms: Algorithm[] = [
  {
    id: "linear-regression",
    name: "Lineare Regression",
    category: "Regression",
    useCase: "Vorhersage kontinuierlicher Werte bei linearen Zusammenhängen",
    useCaseDetails: [
      "Hauspreisvorhersage basierend auf Fläche und Lage",
      "Umsatzprognose anhand von Marketingausgaben",
      "Temperaturvorhersage aus historischen Wetterdaten",
    ],
    trainingFields: [
      {
        name: "target_column",
        label: "Zielvariable",
        type: "text",
        defaultValue: "price",
        description: "Spaltenname der vorherzusagenden Variablen",
      },
      {
        name: "feature_columns",
        label: "Merkmalspalten",
        type: "text",
        defaultValue: "size,rooms,location",
        description: "Kommagetrennte Liste der Eingabespalten",
      },
      {
        name: "test_size",
        label: "Testgröße",
        type: "number",
        defaultValue: 0.2,
        description: "Anteil der Daten für den Testdatensatz (0.0–1.0)",
      },
      {
        name: "fit_intercept",
        label: "Y-Achsenabschnitt anpassen",
        type: "select",
        options: ["true", "false"],
        defaultValue: "true",
        description: "Ob ein Y-Achsenabschnitt berechnet werden soll",
      },
    ],
    modelFile: "linear_regression_model.pkl",
  },
  {
    id: "random-forest",
    name: "Random Forest",
    category: "Ensemble",
    useCase:
      "Klassifikation und Regression mit hoher Genauigkeit und Robustheit",
    useCaseDetails: [
      "Kreditrisikobeurteilung in der Finanzbranche",
      "Krankheitsdiagnose aus medizinischen Messwerten",
      "Betrugserkennung in Transaktionsdaten",
    ],
    trainingFields: [
      {
        name: "target_column",
        label: "Zielvariable",
        type: "text",
        defaultValue: "label",
        description: "Spaltenname der vorherzusagenden Variablen",
      },
      {
        name: "feature_columns",
        label: "Merkmalspalten",
        type: "text",
        defaultValue: "feature1,feature2,feature3",
        description: "Kommagetrennte Liste der Eingabespalten",
      },
      {
        name: "n_estimators",
        label: "Anzahl Entscheidungsbäume",
        type: "number",
        defaultValue: 100,
        description: "Anzahl der Bäume im Wald",
      },
      {
        name: "max_depth",
        label: "Maximale Tiefe",
        type: "number",
        defaultValue: 10,
        description: "Maximale Tiefe jedes Entscheidungsbaums",
      },
      {
        name: "test_size",
        label: "Testgröße",
        type: "number",
        defaultValue: 0.2,
        description: "Anteil der Daten für den Testdatensatz (0.0–1.0)",
      },
    ],
    modelFile: "random_forest_model.pkl",
  },
  {
    id: "svm",
    name: "Support Vector Machine (SVM)",
    category: "Klassifikation",
    useCase:
      "Klassifikation bei hochdimensionalen Daten und klarer Klassentrennung",
    useCaseDetails: [
      "Bilderkennung und Gesichtserkennung",
      "Textklassifikation und Spam-Erkennung",
      "Bioinformatik: Klassifikation von Genexpressionsdaten",
    ],
    trainingFields: [
      {
        name: "target_column",
        label: "Zielvariable",
        type: "text",
        defaultValue: "class",
        description: "Spaltenname der Zielklasse",
      },
      {
        name: "feature_columns",
        label: "Merkmalspalten",
        type: "text",
        defaultValue: "feature1,feature2",
        description: "Kommagetrennte Liste der Eingabespalten",
      },
      {
        name: "kernel",
        label: "Kernel-Funktion",
        type: "select",
        options: ["rbf", "linear", "poly", "sigmoid"],
        defaultValue: "rbf",
        description: "Kernel-Typ für die Transformation des Merkmalsraums",
      },
      {
        name: "C",
        label: "Regularisierungsparameter C",
        type: "number",
        defaultValue: 1.0,
        description: "Stärke der Regularisierung (kleinere Werte = stärkere Regularisierung)",
      },
      {
        name: "test_size",
        label: "Testgröße",
        type: "number",
        defaultValue: 0.2,
        description: "Anteil der Daten für den Testdatensatz (0.0–1.0)",
      },
    ],
    modelFile: "svm_model.pkl",
  },
  {
    id: "decision-tree",
    name: "Entscheidungsbaum",
    category: "Klassifikation",
    useCase:
      "Interpretierbare Klassifikation und Regression mit transparenten Entscheidungsregeln",
    useCaseDetails: [
      "Medizinische Diagnose mit nachvollziehbaren Entscheidungspfaden",
      "Kundenklassifikation für Marketing-Kampagnen",
      "Qualitätskontrolle in der Fertigung",
    ],
    trainingFields: [
      {
        name: "target_column",
        label: "Zielvariable",
        type: "text",
        defaultValue: "label",
        description: "Spaltenname der Zielklasse",
      },
      {
        name: "feature_columns",
        label: "Merkmalspalten",
        type: "text",
        defaultValue: "feature1,feature2,feature3",
        description: "Kommagetrennte Liste der Eingabespalten",
      },
      {
        name: "max_depth",
        label: "Maximale Tiefe",
        type: "number",
        defaultValue: 5,
        description: "Maximale Tiefe des Entscheidungsbaums",
      },
      {
        name: "criterion",
        label: "Trennkriterium",
        type: "select",
        options: ["gini", "entropy", "log_loss"],
        defaultValue: "gini",
        description: "Funktion zur Bewertung der Trennqualität",
      },
      {
        name: "test_size",
        label: "Testgröße",
        type: "number",
        defaultValue: 0.2,
        description: "Anteil der Daten für den Testdatensatz (0.0–1.0)",
      },
    ],
    modelFile: "decision_tree_model.pkl",
  },
  {
    id: "k-means",
    name: "K-Means Clustering",
    category: "Clustering",
    useCase:
      "Unüberwachte Gruppierung ähnlicher Datenpunkte ohne vorherige Klassenlabels",
    useCaseDetails: [
      "Kundensegmentierung für personalisiertes Marketing",
      "Bildkomprimierung durch Farbquantisierung",
      "Anomalieerkennung in Netzwerkdaten",
    ],
    trainingFields: [
      {
        name: "feature_columns",
        label: "Merkmalspalten",
        type: "text",
        defaultValue: "feature1,feature2",
        description: "Kommagetrennte Liste der zu clusternden Spalten",
      },
      {
        name: "n_clusters",
        label: "Anzahl Cluster (k)",
        type: "number",
        defaultValue: 3,
        description: "Anzahl der zu bildenden Gruppen",
      },
      {
        name: "max_iter",
        label: "Maximale Iterationen",
        type: "number",
        defaultValue: 300,
        description: "Maximale Anzahl von Iterationen des Algorithmus",
      },
      {
        name: "init",
        label: "Initialisierungsmethode",
        type: "select",
        options: ["k-means++", "random"],
        defaultValue: "k-means++",
        description: "Methode zur Initialisierung der Cluster-Zentren",
      },
    ],
    modelFile: "kmeans_model.pkl",
  },
  {
    id: "neural-network",
    name: "Neuronales Netzwerk (MLP)",
    category: "Deep Learning",
    useCase:
      "Erkennung komplexer, nichtlinearer Muster in großen Datensätzen",
    useCaseDetails: [
      "Sprachverarbeitung und maschinelle Übersetzung",
      "Bilderkennung und Computer Vision",
      "Zeitreihenvorhersage bei volatilen Daten",
    ],
    trainingFields: [
      {
        name: "target_column",
        label: "Zielvariable",
        type: "text",
        defaultValue: "label",
        description: "Spaltenname der vorherzusagenden Variablen",
      },
      {
        name: "feature_columns",
        label: "Merkmalspalten",
        type: "text",
        defaultValue: "feature1,feature2,feature3",
        description: "Kommagetrennte Liste der Eingabespalten",
      },
      {
        name: "hidden_layers",
        label: "Versteckte Schichten",
        type: "text",
        defaultValue: "128,64,32",
        description: "Kommagetrennte Neuronenanzahl je versteckter Schicht",
      },
      {
        name: "activation",
        label: "Aktivierungsfunktion",
        type: "select",
        options: ["relu", "tanh", "sigmoid", "identity"],
        defaultValue: "relu",
        description: "Aktivierungsfunktion der versteckten Neuronen",
      },
      {
        name: "learning_rate",
        label: "Lernrate",
        type: "number",
        defaultValue: 0.001,
        description: "Schrittgröße bei der Gewichtsanpassung",
      },
      {
        name: "max_iter",
        label: "Maximale Epochen",
        type: "number",
        defaultValue: 200,
        description: "Maximale Anzahl an Trainingsdurchläufen",
      },
      {
        name: "test_size",
        label: "Testgröße",
        type: "number",
        defaultValue: 0.2,
        description: "Anteil der Daten für den Testdatensatz (0.0–1.0)",
      },
    ],
    modelFile: "neural_network_model.pkl",
  },
];
