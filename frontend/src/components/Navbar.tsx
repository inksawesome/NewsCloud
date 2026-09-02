"use client";

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { Gem, LogOut, User as UserIcon } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <motion.nav 
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="bg-white/80 backdrop-blur-md shadow-sm border-b px-4 py-3 sticky top-0 z-50"
    >
      <div className="max-w-4xl mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold text-indigo-600 flex items-center gap-2 tracking-tight">
          NewsCloud
        </Link>
        <div className="flex items-center gap-4">
          <Link href="/leaderboard" className="text-sm text-gray-600 hover:text-blue-600 font-medium">
            Leaderboard
          </Link>
          {user ? (
            <div className="flex items-center gap-4 border-l pl-4">
              <div className="flex items-center gap-1 text-amber-500 font-bold bg-amber-50 px-2 py-1 rounded">
                <Gem size={16} />
                <span>{user.gem_score}</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-700">
                <UserIcon size={16} />
                <span className="font-medium">{user.username}</span>
              </div>
              <button 
                onClick={logout}
                className="text-gray-500 hover:text-red-500"
                title="Logout"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 border-l pl-4">
              <Link href="/login" className="text-sm font-medium text-gray-600 hover:text-blue-600">
                Login
              </Link>
              <Link href="/signup" className="text-sm font-medium bg-blue-600 text-white px-3 py-1.5 rounded-md hover:bg-blue-700">
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </div>
    </motion.nav>
  );
}
