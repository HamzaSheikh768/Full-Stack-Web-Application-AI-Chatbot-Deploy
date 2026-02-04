'use client';

import React, { useState } from 'react';
import { LogOut, User, Mail } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { useAuth } from '@/contexts/AuthContext';

const ProfileDropdown = () => {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    setIsOpen(false);
  };

  if (!user) {
    return null;
  }

  // Get initials from user name
  const getInitials = (name: string) => {
    if (!name) return '?';
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .substring(0, 2);
  };

  return (
    <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="relative h-8 w-8 rounded-full overflow-hidden border border-gray-300 dark:border-gray-600 hover:bg-accent"
          aria-label="Profile menu"
        >
          <Avatar className="h-8 w-8">
            <AvatarImage
              src={user.avatar || user.image || ''}
              alt={user.name || user.email || 'User avatar'}
              className="object-cover"
            />
            <AvatarFallback className="bg-primary/10 text-primary text-xs font-medium">
              {getInitials((user.name || user.first_name || user.last_name || user.email || '').toString())}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        align="end"
        className="w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-2 mt-2"
      >
        <div className="p-2">
          <div className="flex items-center space-x-3 mb-2">
            <Avatar className="h-8 w-8">
              <AvatarImage
                src={user.avatar || user.image || ''}
                alt={user.name || user.email || 'User avatar'}
                className="object-cover"
              />
              <AvatarFallback className="bg-primary/10 text-primary text-xs font-medium">
                {getInitials((user.name || user.first_name || user.last_name || user.email || '').toString())}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                {user.name || `${user.first_name || ''} ${user.last_name || ''}`.trim() || 'User'}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                {user.email}
              </p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-200 dark:border-gray-700 my-1"></div>

        <DropdownMenuItem
          onClick={handleLogout}
          className="flex items-center cursor-pointer p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700"
        >
          <LogOut className="h-4 w-4 mr-2 text-gray-500 dark:text-gray-400" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-200">Logout</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default ProfileDropdown;