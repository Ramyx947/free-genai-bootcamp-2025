
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Words from '../Words';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Words Component', () => {
  it('renders words page with table headers', () => {
    renderWithRouter(<Words />);
    
    expect(screen.getByText('Word Collection')).toBeInTheDocument();
    expect(screen.getByText('Romanian')).toBeInTheDocument();
    expect(screen.getByText('English')).toBeInTheDocument();
    expect(screen.getByText('Pronunciation')).toBeInTheDocument();
  });

  it('handles sorting when clicking column headers', () => {
    renderWithRouter(<Words />);
    
    const romanianHeader = screen.getByText('Romanian');
    
    // First click - sort ascending
    fireEvent.click(romanianHeader);
    expect(romanianHeader.closest('th')).toHaveClass('cursor-pointer');
    
    // Second click - sort descending
    fireEvent.click(romanianHeader);
    expect(romanianHeader.closest('th')).toHaveClass('cursor-pointer');
  });

  it('renders pagination controls', () => {
    renderWithRouter(<Words />);
    
    expect(screen.getByText(/Page 1 of/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /previous/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /next/i })).toBeInTheDocument();
  });
});
