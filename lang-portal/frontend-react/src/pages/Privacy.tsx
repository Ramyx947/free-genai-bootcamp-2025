
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Privacy = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Privacy Policy</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Privacy Policy</CardTitle>
        </CardHeader>
        <CardContent className="prose dark:prose-invert max-w-none">
          <h2>1. Information Collection</h2>
          <p>We collect information that you provide directly to us when using Lumina, including learning progress and preferences.</p>
          
          <h2>2. Use of Information</h2>
          <p>The information we collect is used to provide and improve our language learning services, and to personalize your learning experience.</p>
          
          <h2>3. Data Storage</h2>
          <p>Your data is stored locally and is not shared with third parties. No personal information is required to use the application at this stage.</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Privacy;
