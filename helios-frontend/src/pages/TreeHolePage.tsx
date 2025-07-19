import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Heart, MessageCircle, Share2, MoreHorizontal } from 'lucide-react';
import { Button } from '../components/common/Button';

interface TreeHolePost {
  id: string;
  content: string;
  timestamp: Date;
  likes: number;
  comments: number;
  isLiked: boolean;
  mood?: 'happy' | 'sad' | 'thoughtful' | 'grateful';
}

export const TreeHolePage: React.FC = () => {
  const [newPost, setNewPost] = useState('');
  const [posts] = useState<TreeHolePost[]>([
    {
      id: '1',
      content: '今天完成了一个重要的项目里程碑，感觉整个世界都明亮了起来。有时候，坚持真的会看到曙光。',
      timestamp: new Date(Date.now() - 3600000),
      likes: 12,
      comments: 3,
      isLiked: false,
      mood: 'happy',
    },
    {
      id: '2',
      content: '深夜思考：我们总是在追求更多，却忘记了珍惜已经拥有的。今晚的月光很美，提醒我要活在当下。',
      timestamp: new Date(Date.now() - 7200000),
      likes: 24,
      comments: 7,
      isLiked: true,
      mood: 'thoughtful',
    },
  ]);

  const moodColors = {
    happy: 'text-yellow-400',
    sad: 'text-blue-400',
    thoughtful: 'text-purple-400',
    grateful: 'text-green-400',
  };

  return (
    <div className="h-full overflow-y-auto bg-helios-bg">
      {/* 页面头部 */}
      <div className="p-6 border-b border-helios-border">
        <h1 className="text-2xl font-light text-helios-text-primary mb-2">
          树洞
        </h1>
        <p className="text-helios-text-secondary">
          一个安全的空间，分享您的想法与感受
        </p>
      </div>

      {/* 发布区域 */}
      <div className="p-6 border-b border-helios-border">
        <div className="card">
          <textarea
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
            placeholder="此刻的想法..."
            className="w-full bg-transparent text-helios-text-primary placeholder-helios-text-tertiary resize-none focus:outline-none"
            rows={3}
          />
          <div className="flex items-center justify-between mt-4">
            <div className="flex gap-2">
              {Object.entries(moodColors).map(([mood, color]) => (
                <button
                  key={mood}
                  className={`p-2 rounded-lg hover:bg-helios-bg transition-colors ${color}`}
                  title={mood}
                >
                  <div className="w-5 h-5 rounded-full bg-current opacity-60" />
                </button>
              ))}
            </div>
            <Button
              variant="primary"
              size="sm"
              disabled={!newPost.trim()}
            >
              发布
            </Button>
          </div>
        </div>
      </div>

      {/* 帖子列表 */}
      <div className="p-6 space-y-6">
        {posts.map((post, index) => (
          <motion.article
            key={post.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card"
          >
            {/* 帖子头部 */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-helios-accent-primary bg-opacity-20 rounded-full" />
                <div>
                  <p className="text-sm text-helios-text-primary">匿名用户</p>
                  <p className="text-xs text-helios-text-tertiary">
                    {formatRelativeTime(post.timestamp)}
                  </p>
                </div>
              </div>
              {post.mood && (
                <div className={`${moodColors[post.mood]}`}>
                  <div className="w-4 h-4 rounded-full bg-current opacity-60" />
                </div>
              )}
            </div>

            {/* 帖子内容 */}
            <p className="text-helios-text-primary mb-4 leading-relaxed">
              {post.content}
            </p>

            {/* 互动按钮 */}
            <div className="flex items-center gap-6 pt-4 border-t border-helios-border">
              <button
                className={`flex items-center gap-2 transition-colors ${
                  post.isLiked 
                    ? 'text-helios-accent-primary' 
                    : 'text-helios-text-secondary hover:text-helios-text-primary'
                }`}
              >
                <Heart size={18} fill={post.isLiked ? 'currentColor' : 'none'} />
                <span className="text-sm">{post.likes}</span>
              </button>
              
              <button className="flex items-center gap-2 text-helios-text-secondary hover:text-helios-text-primary transition-colors">
                <MessageCircle size={18} />
                <span className="text-sm">{post.comments}</span>
              </button>
              
              <button className="text-helios-text-secondary hover:text-helios-text-primary transition-colors">
                <Share2 size={18} />
              </button>
              
              <button className="ml-auto text-helios-text-secondary hover:text-helios-text-primary transition-colors">
                <MoreHorizontal size={18} />
              </button>
            </div>
          </motion.article>
        ))}
      </div>
    </div>
  );
};

function formatRelativeTime(date: Date): string {
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}天前`;
  if (hours > 0) return `${hours}小时前`;
  if (minutes > 0) return `${minutes}分钟前`;
  return '刚刚';
} 