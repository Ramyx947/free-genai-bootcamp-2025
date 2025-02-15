
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const Support = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Help & Support</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Frequently Asked Questions</CardTitle>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>How do I start learning?</AccordionTrigger>
              <AccordionContent>
                Navigate to the Study Activities page and choose an activity that interests you. Click the Launch button to begin your learning session.
              </AccordionContent>
            </AccordionItem>
            
            <AccordionItem value="item-2">
              <AccordionTrigger>How do I track my progress?</AccordionTrigger>
              <AccordionContent>
                Your learning progress is automatically tracked in the Sessions page. You can view detailed statistics about your completed sessions and performance.
              </AccordionContent>
            </AccordionItem>
            
            <AccordionItem value="item-3">
              <AccordionTrigger>How do I manage word groups?</AccordionTrigger>
              <AccordionContent>
                Visit the Word Groups page to create and manage your custom word collections. You can add words to groups and use these groups in your study activities.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </CardContent>
      </Card>
    </div>
  );
};

export default Support;
