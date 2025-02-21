import { render, screen, fireEvent, act } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import VocabularyGame from '../vocabulary-game';
import { toast } from "@/hooks/use-toast";

// Mock the toast function
jest.mock("@/hooks/use-toast", () => ({
  useToast: () => ({ toast: jest.fn() }),
  toast: jest.fn()
}));

const renderWithRouter = (component: React.ReactElement, initialState = {}) => {
  return render(
    <MemoryRouter initialEntries={[{ pathname: '/study-activities/vocabulary/1', state: initialState }]}>
      <Routes>
        <Route path="/study-activities/vocabulary/:id" element={component} />
      </Routes>
    </MemoryRouter>
  );
};

describe('VocabularyGame', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders default breadcrumb from study activities', () => {
    renderWithRouter(<VocabularyGame />);
    
    expect(screen.getByText('Study Activities')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary Practice')).toBeInTheDocument();
  });

  it('renders breadcrumb when coming from Words page', () => {
    renderWithRouter(<VocabularyGame />, { source: 'words' });
    
    expect(screen.getByText('Words')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary Practice')).toBeInTheDocument();
  });

  it('renders breadcrumb when coming from Groups page', () => {
    renderWithRouter(<VocabularyGame />, { source: 'groups' });
    
    expect(screen.getByText('Word Groups')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary Practice')).toBeInTheDocument();
  });

  it('shows correct toast message for correct answer', async () => {
    renderWithRouter(<VocabularyGame />);
    
    // Start the game
    const startButton = screen.getByText('Start Practice');
    fireEvent.click(startButton);

    // Type correct answer
    const input = screen.getByPlaceholderText(/Type the English translation/i);
    fireEvent.change(input, { target: { value: 'plate' } });
    
    // Submit answer
    const checkButton = screen.getByText('Check Answer');
    fireEvent.click(checkButton);

    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({
        title: "Correct!",
        variant: "default",
        duration: 5000
      })
    );
  });

  it('shows error toast message for incorrect answer', async () => {
    renderWithRouter(<VocabularyGame />);
    
    // Start the game
    const startButton = screen.getByText('Start Practice');
    fireEvent.click(startButton);

    // Type incorrect answer
    const input = screen.getByPlaceholderText(/Type the English translation/i);
    fireEvent.change(input, { target: { value: 'wrong' } });
    
    // Submit answer
    const checkButton = screen.getByText('Check Answer');
    fireEvent.click(checkButton);

    expect(toast).toHaveBeenCalledWith(
      expect.objectContaining({
        title: "Incorrect",
        variant: "destructive",
        duration: 5000
      })
    );
  });
});
