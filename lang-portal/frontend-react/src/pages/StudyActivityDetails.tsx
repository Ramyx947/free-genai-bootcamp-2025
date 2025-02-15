
import { useParams, Link, useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { CustomBreadcrumb } from "@/components/ui/custom-breadcrumb";

const StudyActivityDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const breadcrumbItems = [
    { label: "Study Activities", path: "/study-activities" },
    { label: "Adventure MUD" },
  ];

  const handleLaunchActivity = () => {
    navigate("/study-activities/vocabulary");
  };

  return (
    <div className="space-y-6">
      <CustomBreadcrumb items={breadcrumbItems} />
      
      <h1 className="text-3xl font-bold tracking-tight">Study Activity Details</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Activity Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="aspect-video bg-muted rounded-lg"></div>
            <h2 className="text-2xl font-semibold">Adventure MUD</h2>
            <p className="text-muted-foreground">
              An interactive text adventure game that helps you learn Romanian through
              immersive storytelling and contextual learning.
            </p>
            <Button onClick={handleLaunchActivity}>
              <Play className="mr-2 h-4 w-4" />
              Launch Activity
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Sessions</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Group</TableHead>
                  <TableHead>Start Time</TableHead>
                  <TableHead>Reviews</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell colSpan={3} className="text-center text-muted-foreground">
                    No sessions found for this activity
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default StudyActivityDetails;
