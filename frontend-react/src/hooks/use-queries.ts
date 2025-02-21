import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import { WordGroup } from '@/types/group';
import { useToast } from '@/hooks/use-toast';

// Dashboard
export const useDashboard = () => {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: api.getDashboard,
  });
};

// Words
export const useWords = () => {
  return useQuery({
    queryKey: ['words'],
    queryFn: api.getWords,
  });
};

export const useWord = (id: number) => {
  return useQuery({
    queryKey: ['words', id],
    queryFn: () => api.getWord(id),
  });
};

// Groups
export const useGroups = () => {
  const { toast } = useToast();
  
  return useQuery({
    queryKey: ['groups'],
    queryFn: api.getGroups,
    onError: (error) => {
      toast({
        title: 'Error',
        description: 'Failed to fetch groups. Please try again.',
        variant: 'destructive',
      });
    },
  });
};

export const useCreateGroup = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.createGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] });
    },
  });
}; 