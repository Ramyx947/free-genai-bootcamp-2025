
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import VocabularyGame from "./vocabulary";

// Mock the toast functionality
jest.mock("@/hooks/use-toast", () => ({
  useToast: () => ({
    toast: jest.fn(),
  }),
}));

describe("VocabularyGame", () => {
  const renderGame = () => {
    render(
      <BrowserRouter>
        <VocabularyGame />
      </BrowserRouter>
    );
  };

  it("renders the vocabulary game", () => {
    renderGame();
    expect(screen.getByText("Vocabulary Practice")).toBeInTheDocument();
    expect(screen.getByText("Kitchen Vocabulary Game")).toBeInTheDocument();
  });

  it("starts the game when clicking start button", () => {
    renderGame();
    const startButton = screen.getByText("Start Game");
    fireEvent.click(startButton);
    expect(screen.getByPlaceholderText("Type your answer...")).toBeInTheDocument();
  });

  it("allows input and checks answers", () => {
    renderGame();
    fireEvent.click(screen.getByText("Start Game"));
    
    const input = screen.getByPlaceholderText("Type your answer...");
    fireEvent.change(input, { target: { value: "plate" } });
    
    const checkButton = screen.getByText("Check");
    fireEvent.click(checkButton);
    
    expect(screen.getByText(/Score:/)).toBeInTheDocument();
  });

  it("resets the game when clicking reset button", () => {
    renderGame();
    fireEvent.click(screen.getByText("Start Game"));
    
    const resetButton = screen.getByText("Reset Game");
    fireEvent.click(resetButton);
    
    expect(screen.getByPlaceholderText("Type your answer...")).toBeInTheDocument();
  });
});
