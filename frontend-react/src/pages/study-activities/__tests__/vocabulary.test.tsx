
import { render, screen } from '@testing-library/react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import VocabularyPractice from '../vocabulary';

const renderWithRouter = (component: React.ReactElement, initialState = {}) => {
  return render(
    <MemoryRouter initialEntries={[{ pathname: '/study-activities/vocabulary', state: initialState }]}>
      {component}
    </MemoryRouter>
  );
};

describe('VocabularyPractice', () => {
  it('renders default breadcrumb from study activities', () => {
    renderWithRouter(<VocabularyPractice />);
    
    expect(screen.getByText('Study Activities')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary Practice')).toBeInTheDocument();
  });

  it('renders breadcrumb when coming from Words page', () => {
    renderWithRouter(<VocabularyPractice />, { source: 'words' });
    
    expect(screen.getByText('Words')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary Practice')).toBeInTheDocument();
  });

  it('renders breadcrumb when coming from Groups page', () => {
    renderWithRouter(<VocabularyPractice />, { source: 'groups' });
    
    expect(screen.getByText('Word Groups')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary Practice')).toBeInTheDocument();
  });

  it('filters groups based on wordGroups from state', () => {
    renderWithRouter(<VocabularyPractice />, { 
      source: 'words',
      wordGroups: ['Core Verbs']
    });
    
    expect(screen.getByText('Core Verbs')).toBeInTheDocument();
    expect(screen.queryByText('Kitchen')).not.toBeInTheDocument();
  });
});
