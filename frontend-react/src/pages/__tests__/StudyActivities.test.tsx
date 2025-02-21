
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import StudyActivities from "../StudyActivities";

describe("StudyActivities", () => {
  it("renders study activities page", () => {
    render(
      <BrowserRouter>
        <StudyActivities />
      </BrowserRouter>
    );

    expect(screen.getByText("Study Activities")).toBeInTheDocument();
    expect(screen.getByText("Vocabulary Practice")).toBeInTheDocument();
    expect(screen.getByText("Reading Comprehension")).toBeInTheDocument();
    expect(screen.getByText("Grammar Exercises")).toBeInTheDocument();
  });

  it("renders activity descriptions", () => {
    render(
      <BrowserRouter>
        <StudyActivities />
      </BrowserRouter>
    );

    expect(screen.getByText("Practice new vocabulary with interactive exercises")).toBeInTheDocument();
    expect(screen.getByText("Improve your reading skills with Romanian texts")).toBeInTheDocument();
    expect(screen.getByText("Practice Romanian grammar with structured exercises")).toBeInTheDocument();
  });
});
