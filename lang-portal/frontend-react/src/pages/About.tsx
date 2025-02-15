
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Info } from "lucide-react";

const About = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">About Lumina</h1>
      
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0">
          <CardTitle>Our Mission</CardTitle>
          <Info className="h-5 w-5 text-muted-foreground" />
        </CardHeader>
        <CardContent className="prose dark:prose-invert max-w-none">
          <p>
            Lumina is a modern Romanian language learning platform designed to make
            language acquisition engaging, effective, and accessible to everyone.
          </p>
          
          <h2>Why Lumina?</h2>
          <p>
            Our platform combines interactive study activities, comprehensive vocabulary
            management, and progress tracking to create a complete learning experience.
            Whether you're a beginner or looking to enhance your Romanian language
            skills, Lumina provides the tools you need to succeed.
          </p>
          
          <h2>Contact Us</h2>
          <p>
            For any inquiries or support needs, please visit our Support page or
            submit your feedback through our Feedback form. We're here to help you
            on your language learning journey.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default About;
