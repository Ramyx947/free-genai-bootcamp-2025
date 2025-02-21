
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import WordDetails from "../WordDetails";

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useParams: () => ({
    id: "1"
  })
}));

describe("WordDetails", () => {
  it("renders the word details page", () => {
    render(
      <BrowserRouter>
        <WordDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Word Details")).toBeInTheDocument();
    expect(screen.getByText("Word Information")).toBeInTheDocument();
    expect(screen.getByText("Practice Statistics")).toBeInTheDocument();
  });

  it("shows breadcrumb navigation", () => {
    render(
      <BrowserRouter>
        <WordDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Words")).toBeInTheDocument();
    expect(screen.getByText("Word Details")).toBeInTheDocument();
  });
});
