
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { CustomBreadcrumb } from "../custom-breadcrumb";

describe("CustomBreadcrumb", () => {
  const mockItems = [
    { label: "Home", path: "/" },
    { label: "Words", path: "/words" },
    { label: "Word Details" },
  ];

  it("renders all breadcrumb items", () => {
    render(
      <BrowserRouter>
        <CustomBreadcrumb items={mockItems} />
      </BrowserRouter>
    );

    mockItems.forEach((item) => {
      expect(screen.getByText(item.label)).toBeInTheDocument();
    });
  });

  it("renders the first item with a back arrow", () => {
    render(
      <BrowserRouter>
        <CustomBreadcrumb items={mockItems} />
      </BrowserRouter>
    );

    const firstItem = screen.getByText(mockItems[0].label);
    const backArrow = firstItem.parentElement?.querySelector("svg");
    expect(backArrow).toBeInTheDocument();
  });

  it("renders the last item as non-clickable", () => {
    render(
      <BrowserRouter>
        <CustomBreadcrumb items={mockItems} />
      </BrowserRouter>
    );

    const lastItem = screen.getByText(mockItems[mockItems.length - 1].label);
    expect(lastItem.closest("a")).not.toBeInTheDocument();
  });
});
