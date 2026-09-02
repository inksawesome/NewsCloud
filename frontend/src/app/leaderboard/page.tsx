"use client";

import { Gem, Trophy, Medal } from 'lucide-react';
import { motion } from 'framer-motion';

const MOCK_LEADERBOARD = [
  { rank: 1, username: 'fact_checker_99', gems: 142 },
  { rank: 2, username: 'news_hound', gems: 89 },
  { rank: 3, username: 'truth_seeker', gems: 76 },
  { rank: 4, username: 'user1', gems: 4 },
  { rank: 5, username: 'anon_reader', gems: 1 },
];

export default function LeaderboardPage() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto"
    >
      <div className="text-center mb-10">
        <motion.h1 
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          className="text-4xl font-extrabold text-slate-900 mb-4 flex items-center justify-center gap-3 tracking-tight"
        >
          <Trophy className="text-yellow-500 drop-shadow-sm" size={40} />
          Global Leaderboard
        </motion.h1>
        <p className="text-lg text-slate-600">Top contributors combatting misinformation</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="px-6 py-4 font-semibold text-slate-700">Rank</th>
              <th className="px-6 py-4 font-semibold text-slate-700">User</th>
              <th className="px-6 py-4 font-semibold text-slate-700 text-right">GEMs Earned</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {MOCK_LEADERBOARD.map((user, idx) => (
              <motion.tr 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                key={user.rank} 
                className="hover:bg-slate-50 transition-colors"
              >
                <td className="px-6 py-4">
                  {user.rank === 1 ? (
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-yellow-100 text-yellow-700 font-bold shadow-sm">
                      1
                    </div>
                  ) : user.rank === 2 ? (
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-slate-200 text-slate-700 font-bold shadow-sm">
                      2
                    </div>
                  ) : user.rank === 3 ? (
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-amber-100 text-amber-800 font-bold shadow-sm">
                      3
                    </div>
                  ) : (
                    <div className="flex items-center justify-center w-8 h-8 font-medium text-slate-500">
                      {user.rank}
                    </div>
                  )}
                </td>
                <td className="px-6 py-4 font-medium text-slate-900">
                  {user.username}
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="inline-flex items-center gap-1 bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full font-bold">
                    <Gem size={16} />
                    {user.gems}
                  </div>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}
