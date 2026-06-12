"use client";

import { useRouter, usePathname } from "next/navigation";
import {
  Home,
  Map,
  Database,
  BarChart3,
  Filter,
  Heart,
  TrendingUp,
  Settings,
} from "lucide-react";

const menuItems = [
  { id: "dashboard", label: "首页", icon: Home, path: "/" },
  { id: "opportunities", label: "机会地图", icon: Map, path: "/" },
  { id: "stocks", label: "股票池", icon: Database, path: "/" },
  { id: "industry", label: "行业分析", icon: BarChart3, path: "/" },
  { id: "screener", label: "策略筛选", icon: Filter, path: "/screener" },
  { id: "watchlist", label: "我的关注", icon: Heart, path: "/" },
  { id: "backtest", label: "回测表现", icon: TrendingUp, path: "/" },
  { id: "settings", label: "设置", icon: Settings, path: "/" },
];

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();

  return (
    <aside className="w-16 bg-cfa-card border-r border-cfa-border flex flex-col items-center py-4">
      {/* Logo */}
      <div className="w-10 h-10 bg-cfa-accent rounded-xl flex items-center justify-center mb-6">
        <span className="text-white font-bold text-sm">CFA</span>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.path || (item.path !== "/" && pathname.startsWith(item.path));
          return (
            <button
              key={item.id}
              onClick={() => router.push(item.path)}
              className={`w-10 h-10 rounded-xl flex items-center justify-center transition-all ${
                isActive
                  ? "bg-cfa-accent/20 text-cfa-accent"
                  : "text-cfa-muted hover:text-cfa-text hover:bg-cfa-border"
              }`}
              title={item.label}
            >
              <Icon className="w-5 h-5" />
            </button>
          );
        })}
      </nav>

      {/* User Avatar */}
      <div className="mt-auto">
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cfa-accent to-purple-500 flex items-center justify-center">
          <span className="text-xs font-medium text-white">I</span>
        </div>
      </div>
    </aside>
  );
}
