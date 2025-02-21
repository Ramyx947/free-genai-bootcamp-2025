
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Settings from '../Settings';

describe('Settings Component', () => {
  it('renders settings page with all sections', () => {
    render(<Settings />);
    
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Appearance & Language')).toBeInTheDocument();
    expect(screen.getByText('Reset History')).toBeInTheDocument();
  });

  it('toggles dark mode when switch is clicked', () => {
    render(<Settings />);
    
    const darkModeSwitch = screen.getByRole('switch', { name: /dark mode/i });
    fireEvent.click(darkModeSwitch);
    
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    
    fireEvent.click(darkModeSwitch);
    expect(document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('handles language toggle', () => {
    render(<Settings />);
    
    const languageSwitch = screen.getByRole('switch', { name: /language/i });
    fireEvent.click(languageSwitch);
  });

  it('shows reset confirmation dialog when reset button is clicked', async () => {
    render(<Settings />);
    
    const resetButton = screen.getByRole('button', { name: /reset history/i });
    fireEvent.click(resetButton);
    
    expect(screen.getByText('Are you absolutely sure?')).toBeInTheDocument();
    expect(screen.getByText(/This action cannot be undone/i)).toBeInTheDocument();
  });

  it('enables reset confirmation button only with correct text', async () => {
    render(<Settings />);
    
    // Open dialog
    fireEvent.click(screen.getByRole('button', { name: /reset history/i }));
    
    // Find the confirmation input and reset button
    const input = screen.getByLabelText(/Type "reset me" to confirm:/i);
    const confirmButton = screen.getByRole('button', { name: /reset/i });
    
    // Initially disabled
    expect(confirmButton).toBeDisabled();
    
    // Type incorrect text
    await userEvent.type(input, 'wrong text');
    expect(confirmButton).toBeDisabled();
    
    // Clear and type correct text
    await userEvent.clear(input);
    await userEvent.type(input, 'reset me');
    expect(confirmButton).not.toBeDisabled();
  });
});
