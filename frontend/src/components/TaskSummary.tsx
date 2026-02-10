import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Calendar, Flag, Tag } from 'lucide-react';

interface TaskSummaryProps {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  tags?: string[];
  dueDate?: string;
  completed?: boolean;
}

export function TaskSummary({ 
  title, 
  description, 
  priority, 
  tags, 
  dueDate, 
  completed 
}: TaskSummaryProps) {
  const getPriorityVariant = (priority: string | undefined) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return 'destructive';
      case 'medium':
        return 'default';
      case 'low':
        return 'secondary';
      default:
        return 'secondary';
    }
  };

  const getPriorityIcon = (priority: string | undefined) => {
    switch (priority?.toLowerCase()) {
      case 'high':
        return <Flag className="h-3 w-3 mr-1" />;
      case 'medium':
        return <Flag className="h-3 w-3 mr-1 opacity-70" />;
      case 'low':
        return <Flag className="h-3 w-3 mr-1 opacity-40" />;
      default:
        return <Flag className="h-3 w-3 mr-1" />;
    }
  };

  return (
    <Card className="mt-2 w-full max-w-md">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardTitle className={`text-lg ${completed ? 'line-through text-gray-500' : ''}`}>
            {title}
          </CardTitle>
          {priority && (
            <Badge variant={getPriorityVariant(priority)}>
              {getPriorityIcon(priority)}
              {priority}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {description && (
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">{description}</p>
        )}
        
        <div className="flex flex-wrap gap-2 mt-2">
          {tags && tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {tags.map((tag, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  <Tag className="h-2.5 w-2.5 mr-1" />
                  {tag}
                </Badge>
              ))}
            </div>
          )}
          
          {dueDate && (
            <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
              <Calendar className="h-3 w-3 mr-1" />
              {new Date(dueDate).toLocaleDateString()}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}