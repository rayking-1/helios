import React from 'react';
import { motion } from 'framer-motion';
import { Trophy, Target, Flame, Zap } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import { Challenge } from '../types';

export const ChallengePage: React.FC = () => {
  const { challenges, updateChallengeProgress } = useAppStore();

  const categoryIcons = {
    productivity: <Zap className="text-helios-accent-primary" />,
    wellness: <Flame className="text-helios-accent-warning" />,
    learning: <Target className="text-helios-accent-secondary" />,
    creativity: <Trophy className="text-helios-accent-success" />,
  };

  const mockChallenges: Challenge[] = [
    {
      id: '1',
      title: '深度专注大师',
      description: '连续7天每天完成至少2小时的深度专注时间',
      category: 'productivity',
      progress: 3,
      targetValue: 7,
      unit: '天',
      reward: { points: 100, badge: 'focus-master' },
    },
    {
      id: '2',
      title: '知识探索者',
      description: '本月阅读5本书籍或完成10小时的学习',
      category: 'learning',
      progress: 2,
      targetValue: 5,
      unit: '本',
      reward: { points: 150, badge: 'knowledge-seeker' },
    },
  ];

  return (
    <div className="h-full overflow-y-auto bg-helios-bg p-6">
      {/* 页面标题 */}
      <div className="mb-8">
        <h1 className="text-2xl font-light text-helios-text-primary mb-2">
          挑战
        </h1>
        <p className="text-helios-text-secondary">
          通过完成挑战，解锁成就，成为更好的自己
        </p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard title="总积分" value="450" icon={<Trophy />} color="text-helios-accent-primary" />
        <StatCard title="连续天数" value="7" icon={<Flame />} color="text-helios-accent-warning" />
        <StatCard title="完成挑战" value="12" icon={<Target />} color="text-helios-accent-success" />
        <StatCard title="当前等级" value="Lv.3" icon={<Zap />} color="text-helios-accent-secondary" />
      </div>

      {/* 挑战列表 */}
      <div className="space-y-6">
        <section>
          <h2 className="text-lg font-medium text-helios-text-primary mb-4">
            进行中的挑战
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockChallenges.map((challenge) => (
              <ChallengeCard
                key={challenge.id}
                challenge={challenge}
                icon={categoryIcons[challenge.category]}
              />
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-lg font-medium text-helios-text-primary mb-4">
            可用挑战
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* 更多挑战卡片 */}
          </div>
        </section>
      </div>
    </div>
  );
};

const StatCard: React.FC<{
  title: string;
  value: string;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, icon, color }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className="card text-center"
  >
    <div className={`inline-flex p-3 rounded-lg bg-helios-card mb-3 ${color}`}>
      {icon}
    </div>
    <h3 className="text-2xl font-light text-helios-text-primary">{value}</h3>
    <p className="text-sm text-helios-text-secondary">{title}</p>
  </motion.div>
);

const ChallengeCard: React.FC<{
  challenge: Challenge;
  icon: React.ReactNode;
}> = ({ challenge, icon }) => {
  const progressPercentage = (challenge.progress / challenge.targetValue) * 100;

  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="card"
    >
      <div className="flex items-start gap-4 mb-4">
        <div className="p-2 bg-helios-card rounded-lg">
          {icon}
        </div>
        <div className="flex-1">
          <h3 className="font-medium text-helios-text-primary">{challenge.title}</h3>
          <p className="text-sm text-helios-text-secondary mt-1">
            {challenge.description}
          </p>
        </div>
      </div>

      {/* 进度条 */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-helios-text-secondary">
            {challenge.progress} / {challenge.targetValue} {challenge.unit}
          </span>
          <span className="text-helios-accent-primary">
            {Math.round(progressPercentage)}%
          </span>
        </div>
        <div className="h-2 bg-helios-border rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-helios-accent-primary to-helios-accent-secondary"
            initial={{ width: 0 }}
            animate={{ width: `${progressPercentage}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>
      </div>

      {/* 奖励 */}
      <div className="flex items-center justify-between mt-4 pt-4 border-t border-helios-border">
        <span className="text-sm text-helios-text-secondary">奖励</span>
        <div className="flex items-center gap-2">
          <Trophy size={16} className="text-helios-accent-warning" />
          <span className="text-sm font-medium text-helios-text-primary">
            +{challenge.reward.points} 积分
          </span>
        </div>
      </div>
    </motion.div>
  );
}; 