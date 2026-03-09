import { describe, it, expect } from "vitest";
import { algorithms } from "../data/algorithms";

describe("algorithms data", () => {
  it("exports a non-empty array of algorithms", () => {
    expect(algorithms).toBeInstanceOf(Array);
    expect(algorithms.length).toBeGreaterThan(0);
  });

  it("each algorithm has a unique id", () => {
    const ids = algorithms.map((a) => a.id);
    const uniqueIds = new Set(ids);
    expect(uniqueIds.size).toBe(ids.length);
  });

  it("each algorithm has a non-empty name", () => {
    algorithms.forEach((alg) => {
      expect(alg.name).toBeTruthy();
    });
  });

  it("each algorithm has a non-empty useCase", () => {
    algorithms.forEach((alg) => {
      expect(alg.useCase).toBeTruthy();
    });
  });

  it("each algorithm has at least one useCaseDetail", () => {
    algorithms.forEach((alg) => {
      expect(alg.useCaseDetails.length).toBeGreaterThan(0);
    });
  });

  it("each algorithm has at least one trainingField", () => {
    algorithms.forEach((alg) => {
      expect(alg.trainingFields.length).toBeGreaterThan(0);
    });
  });

  it("each algorithm has a non-empty modelFile ending in .pkl", () => {
    algorithms.forEach((alg) => {
      expect(alg.modelFile).toBeTruthy();
      expect(alg.modelFile).toMatch(/\.pkl$/);
    });
  });

  it("each algorithm's modelFile is unique", () => {
    const modelFiles = algorithms.map((a) => a.modelFile);
    const uniqueFiles = new Set(modelFiles);
    expect(uniqueFiles.size).toBe(modelFiles.length);
  });

  it("each trainingField has a name, label, type, and description", () => {
    algorithms.forEach((alg) => {
      alg.trainingFields.forEach((field) => {
        expect(field.name).toBeTruthy();
        expect(field.label).toBeTruthy();
        expect(["text", "number", "select"]).toContain(field.type);
        expect(field.description).toBeTruthy();
      });
    });
  });

  it("select trainingFields have options defined", () => {
    algorithms.forEach((alg) => {
      alg.trainingFields
        .filter((f) => f.type === "select")
        .forEach((field) => {
          expect(field.options).toBeInstanceOf(Array);
          expect((field.options ?? []).length).toBeGreaterThan(0);
        });
    });
  });

  it("includes Linear Regression algorithm", () => {
    const lr = algorithms.find((a) => a.id === "linear-regression");
    expect(lr).toBeDefined();
    expect(lr?.modelFile).toBe("linear_regression_model.pkl");
  });

  it("includes Random Forest algorithm", () => {
    const rf = algorithms.find((a) => a.id === "random-forest");
    expect(rf).toBeDefined();
    expect(rf?.modelFile).toBe("random_forest_model.pkl");
  });

  it("includes SVM algorithm", () => {
    const svm = algorithms.find((a) => a.id === "svm");
    expect(svm).toBeDefined();
    expect(svm?.modelFile).toBe("svm_model.pkl");
  });

  it("includes Decision Tree algorithm", () => {
    const dt = algorithms.find((a) => a.id === "decision-tree");
    expect(dt).toBeDefined();
    expect(dt?.modelFile).toBe("decision_tree_model.pkl");
  });

  it("includes K-Means algorithm", () => {
    const km = algorithms.find((a) => a.id === "k-means");
    expect(km).toBeDefined();
    expect(km?.modelFile).toBe("kmeans_model.pkl");
  });

  it("includes Neural Network algorithm", () => {
    const nn = algorithms.find((a) => a.id === "neural-network");
    expect(nn).toBeDefined();
    expect(nn?.modelFile).toBe("neural_network_model.pkl");
  });
});
