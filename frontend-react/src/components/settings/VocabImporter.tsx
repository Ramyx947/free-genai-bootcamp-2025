import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { fetchWithTimeout } from '@/api';
import { Download } from 'lucide-react';

export const VocabImporter = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const { toast } = useToast();

  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB in bytes
  
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      toast({
        title: "File too large",
        description: "Please upload a file smaller than 10MB",
        variant: "destructive"
      });
      e.target.value = ''; // Clear input
      return;
    }
    
    // Check file type
    const validTypes = [
      'application/json',
      'text/plain',
      'text/csv',
      'application/pdf'
    ];
    
    if (!validTypes.includes(file.type)) {
      toast({
        title: "Invalid file type",
        description: "Please upload a .json, .txt, .csv or .pdf file",
        variant: "destructive"
      });
      e.target.value = '';
      return;
    }
    
    setFile(file);
  };

  const handleImport = async () => {
    if (!file) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetchWithTimeout('http://localhost:5001/import', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Import failed');
      }

      toast({
        title: "Success",
        description: "Vocabulary imported successfully"
      });
      
      setFile(null);
    } catch (error) {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      setIsExporting(true);
      const response = await fetch('http://localhost:5001/export');
      
      if (!response.ok) {
        throw new Error('Export failed');
      }

      // Get filename from response headers
      const filename = response.headers
        .get('content-disposition')
        ?.split('filename=')[1] || 'vocabulary_export.json';

      // Download file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast({
        title: "Success",
        description: "Vocabulary exported successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive"
      });
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Vocabulary Tools</CardTitle>
        <CardDescription>
          Import or export vocabulary files
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between items-center">
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <Input
              type="file"
              accept=".json,.txt,.csv,.pdf"
              onChange={handleFileUpload}
            />
          </div>
          <Button
            onClick={handleExport}
            disabled={isExporting}
            variant="outline"
          >
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
        </div>
        {file && (
          <div className="flex items-center gap-2">
            <Button onClick={handleImport} disabled={isLoading}>
              Import {file.name}
            </Button>
            <Button variant="outline" onClick={() => setFile(null)}>
              Cancel
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}; 