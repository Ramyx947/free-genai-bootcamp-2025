
import { ErrorHandler } from '@/lib/errors';

export const handleApiError = async () => {
  try {
    // Your API call or operation here
    throw new Error('API failed');
  } catch (error) {
    ErrorHandler.handleError(error);
  }
};

// Or create a specific error
export const handleValidationError = () => {
  const error = ErrorHandler.createError('VALIDATION_ERROR', {
    field: 'email',
    value: 'invalid-email'
  });
  ErrorHandler.handleError(error);
};
