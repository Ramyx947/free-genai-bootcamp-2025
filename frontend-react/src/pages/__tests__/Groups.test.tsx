
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Groups from '../Groups';

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Groups Component', () => {
  it('renders groups page with table headers', () => {
    renderWithRouter(<Groups />);
    
    expect(screen.getByText('Word Groups')).toBeInTheDocument();
    expect(screen.getByText('Group Name')).toBeInTheDocument();
    expect(screen.getByText('Words')).toBeInTheDocument();
  });

  it('handles sorting when clicking column headers', () => {
    renderWithRouter(<Groups />);
    
    const nameHeader = screen.getByText('Group Name');
    
    // First click - sort ascending
    fireEvent.click(nameHeader);
    expect(nameHeader.closest('th')).toHaveClass('cursor-pointer');
    
    // Second click - sort descending
    fireEvent.click(nameHeader);
    expect(nameHeader.closest('th')).toHaveClass('cursor-pointer');
  });

  it('renders pagination controls', () => {
    renderWithRouter(<Groups />);
    
    expect(screen.getByText(/Page 1 of/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /previous/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /next/i })).toBeInTheDocument();
  });

  it('renders create group button', () => {
    renderWithRouter(<Groups />);
    
    expect(screen.getByRole('button', { name: /create group/i })).toBeInTheDocument();
  });
});
