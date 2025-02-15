
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import StudyActivityDetails from "../StudyActivityDetails";

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useParams: () => ({
    id: "1"
  }),
  useNavigate: () => jest.fn()
}));

describe("StudyActivityDetails", () => {
  it("renders the study activity details page", () => {
    render(
      <BrowserRouter>
        <StudyActivityDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Study Activity Details")).toBeInTheDocument();
    expect(screen.getByText("Activity Information")).toBeInTheDocument();
    expect(screen.getByText("Recent Sessions")).toBeInTheDocument();
  });

  it("shows breadcrumb navigation", () => {
    render(
      <BrowserRouter>
        <StudyActivityDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Study Activities")).toBeInTheDocument();
    expect(screen.getByText("Adventure MUD")).toBeInTheDocument();
  });

  it("displays the launch activity button", () => {
    render(
      <BrowserRouter>
        <StudyActivityDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Launch Activity")).toBeInTheDocument();
  });
});
