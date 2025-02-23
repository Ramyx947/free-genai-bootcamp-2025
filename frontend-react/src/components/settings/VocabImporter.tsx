import { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

export const VocabImporter = () => {
  const [file, setFile] = useState<File | null>(null);
  const { toast } = useToast();

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
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
      return;
    }
    
    setFile(file);
  };

  const handleImport = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5001/import', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Import failed');

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
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Import Vocabulary</CardTitle>
        <CardDescription>
          Import vocabulary from JSON, TXT, CSV or PDF files
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid w-full max-w-sm items-center gap-1.5">
          <Input
            type="file"
            accept=".json,.txt,.csv,.pdf"
            onChange={handleFileUpload}
          />
        </div>
        {file && (
          <div className="flex items-center gap-2">
            <Button onClick={handleImport}>
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