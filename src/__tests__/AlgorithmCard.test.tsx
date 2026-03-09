import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import AlgorithmCard from "../components/AlgorithmCard";
import { algorithms } from "../data/algorithms";

const linearRegression = algorithms.find((a) => a.id === "linear-regression")!;
const randomForest = algorithms.find((a) => a.id === "random-forest")!;

describe("AlgorithmCard", () => {
  it("renders the algorithm name", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    expect(screen.getByText(linearRegression.name)).toBeInTheDocument();
  });

  it("renders the category badge", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    expect(screen.getByText(linearRegression.category)).toBeInTheDocument();
  });

  it("renders the best use case section", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    expect(screen.getByText("Bester Einsatzzweck")).toBeInTheDocument();
    expect(screen.getByText(linearRegression.useCase)).toBeInTheDocument();
  });

  it("renders all use case details", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    linearRegression.useCaseDetails.forEach((detail) => {
      expect(screen.getByText(detail)).toBeInTheDocument();
    });
  });

  it("renders the model file section with correct filename", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    expect(screen.getByText("Gespeicherte Modelldatei")).toBeInTheDocument();
    expect(screen.getByText("linear_regression_model.pkl")).toBeInTheDocument();
  });

  it("renders the training fields toggle button", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    expect(screen.getByText(/Trainingsfelder/)).toBeInTheDocument();
  });

  it("training fields are hidden by default", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    expect(
      screen.queryByTestId(`training-fields-${linearRegression.id}`)
    ).not.toBeInTheDocument();
  });

  it("expands training fields on toggle button click", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    const toggleBtn = screen.getByRole("button", { name: /Trainingsfelder/i });
    fireEvent.click(toggleBtn);
    expect(
      screen.getByTestId(`training-fields-${linearRegression.id}`)
    ).toBeInTheDocument();
  });

  it("renders training field labels when expanded", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    const toggleBtn = screen.getByRole("button", { name: /Trainingsfelder/i });
    fireEvent.click(toggleBtn);
    linearRegression.trainingFields.forEach((field) => {
      expect(screen.getByText(field.label)).toBeInTheDocument();
    });
  });

  it("collapses training fields on second toggle button click", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    const toggleBtn = screen.getByRole("button", { name: /Trainingsfelder/i });
    fireEvent.click(toggleBtn);
    fireEvent.click(toggleBtn);
    expect(
      screen.queryByTestId(`training-fields-${linearRegression.id}`)
    ).not.toBeInTheDocument();
  });

  it("each algorithm renders its own unique model file", () => {
    const { rerender } = render(<AlgorithmCard algorithm={linearRegression} />);
    expect(screen.getByText("linear_regression_model.pkl")).toBeInTheDocument();

    rerender(<AlgorithmCard algorithm={randomForest} />);
    expect(screen.getByText("random_forest_model.pkl")).toBeInTheDocument();
  });

  it("has correct aria-expanded on toggle button", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    const toggleBtn = screen.getByRole("button", { name: /Trainingsfelder/i });
    expect(toggleBtn).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(toggleBtn);
    expect(toggleBtn).toHaveAttribute("aria-expanded", "true");
  });

  it("renders select input for select-type training fields", () => {
    render(<AlgorithmCard algorithm={linearRegression} />);
    const toggleBtn = screen.getByRole("button", { name: /Trainingsfelder/i });
    fireEvent.click(toggleBtn);
    // "Y-Achsenabschnitt anpassen" is a select field in Linear Regression
    expect(
      screen.getByRole("combobox", {
        name: /Y-Achsenabschnitt anpassen/i,
      })
    ).toBeInTheDocument();
  });
});
