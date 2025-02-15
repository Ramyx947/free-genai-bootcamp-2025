
import { Link, useNavigate } from "react-router-dom";
import { ArrowDown, ArrowUp, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { WordGroup, SortField, SortOrder } from "@/types/group";

interface GroupsTableProps {
  groups: WordGroup[];
  sortField: SortField;
  sortOrder: SortOrder;
  onSort: (field: SortField) => void;
  onPractice?: (groupId: number) => void;  // Added this line
}

export const GroupsTable = ({
  groups,
  sortField,
  sortOrder,
  onSort,
  onPractice
}: GroupsTableProps) => {
  const navigate = useNavigate();
  
  const renderSortIcon = (field: SortField) => {
    if (field !== sortField) return null;
    return sortOrder === 'asc' ? (
      <ArrowUp className="ml-1 h-4 w-4 inline" />
    ) : (
      <ArrowDown className="ml-1 h-4 w-4 inline" />
    );
  };

  const handlePracticeClick = (groupId: number) => {
    if (onPractice) {
      onPractice(groupId);
    } else {
      navigate(`/study-activities/vocabulary/${groupId}`);
    }
  };

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead 
            className="cursor-pointer hover:bg-muted/50 pl-6"
            onClick={() => onSort('name')}
          >
            Group Name {renderSortIcon('name')}
          </TableHead>
          <TableHead 
            className="cursor-pointer hover:bg-muted/50"
            onClick={() => onSort('wordCount')}
          >
            Words {renderSortIcon('wordCount')}
          </TableHead>
          <TableHead className="text-right pr-6">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {groups.map((group) => (
          <TableRow key={group.id}>
            <TableCell data-label="Group Name" className="pl-6">
              <Link to={`/groups/${group.id}`} className="hover:underline">
                {group.name}
              </Link>
            </TableCell>
            <TableCell data-label="Words">
              {group.wordCount}
            </TableCell>
            <TableCell data-label="Actions" className="text-right pr-6">
              <Button
                onClick={() => handlePracticeClick(group.id)}
                className="bg-purple-600 hover:bg-purple-700 text-white dark:bg-purple-500 dark:hover:bg-purple-600"
                size="sm"
              >
                <Play className="mr-2 h-4 w-4" />
                Practice
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
