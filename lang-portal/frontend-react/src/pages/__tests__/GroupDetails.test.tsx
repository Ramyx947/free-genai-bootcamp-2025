
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import GroupDetails from "../GroupDetails";

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useParams: () => ({
    id: "1"
  })
}));

describe("GroupDetails", () => {
  it("renders the group details page", () => {
    render(
      <BrowserRouter>
        <GroupDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Group Details")).toBeInTheDocument();
    expect(screen.getByText("Kitchen")).toBeInTheDocument();
  });

  it("shows breadcrumb navigation", () => {
    render(
      <BrowserRouter>
        <GroupDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Groups")).toBeInTheDocument();
    expect(screen.getByText("Kitchen")).toBeInTheDocument();
  });

  it("displays the words table", () => {
    render(
      <BrowserRouter>
        <GroupDetails />
      </BrowserRouter>
    );

    expect(screen.getByText("Romanian")).toBeInTheDocument();
    expect(screen.getByText("English")).toBeInTheDocument();
    expect(screen.getByText("Pronunciation")).toBeInTheDocument();
  });
});
