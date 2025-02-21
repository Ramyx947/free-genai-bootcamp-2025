
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Terms = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Terms & Conditions</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Terms of Use</CardTitle>
        </CardHeader>
        <CardContent className="prose dark:prose-invert max-w-none">
          <h2>1. Acceptance of Terms</h2>
          <p>By accessing and using Lumina, you agree to be bound by these Terms and Conditions.</p>
          
          <h2>2. Use License</h2>
          <p>Permission is granted to temporarily use this language learning application for personal, non-commercial purposes only.</p>
          
          <h2>3. Disclaimer</h2>
          <p>The materials on Lumina are provided on an 'as is' basis. Lumina makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Terms;
