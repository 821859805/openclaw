#!/usr/bin/env python3
"""Generate a flowchart for SkillSnapshot caching process"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='SkillSnapshot Caching Process', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.5', ranksep='0.6', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='11')
dot.attr('edge', fontname='SimHei,Arial', fontsize='9')

# ==================== 标题 ====================
dot.node('title', '📸 SkillSnapshot 创建与缓存流程', shape='plaintext', fontsize='16', fontcolor='#1565C0')

# ==================== 数据结构 ====================
with dot.subgraph(name='cluster_structure') as c:
    c.attr(label='🗂️ 核心数据结构', style='rounded,filled', fillcolor='#ECEFF1', color='#546E7A', penwidth='2')
    
    c.node('snapshot_struct', '''SkillSnapshot {
  prompt: string          // XML格式的技能列表
  skills: Array&lt;{name, primaryEnv}&gt;
  resolvedSkills?: Skill[]
  version?: number        // 版本号
}''', shape='note', style='filled', fillcolor='#CFD8DC', fontsize='10')
    
    c.node('session_struct', '''SessionEntry {
  sessionId: string
  skillsSnapshot?: SkillSnapshot  // 缓存在这里
  ...其他会话元数据
}''', shape='note', style='filled', fillcolor='#B0BEC5', fontsize='10')

# ==================== 版本管理 ====================
with dot.subgraph(name='cluster_version') as c:
    c.attr(label='🔢 版本管理机制', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    
    c.node('global_ver', 'globalVersion\n(全局版本号)', shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    c.node('workspace_ver', 'workspaceVersions\nMap&lt;workspaceDir, version&gt;', shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    
    c.node('get_version', 'getSkillsSnapshotVersion()\n返回 max(global, workspace)', shape='box', style='rounded,filled', fillcolor='#A5D6A7')
    c.node('bump_version', 'bumpSkillsSnapshotVersion()\n版本号 = max(now, current+1)', shape='box', style='rounded,filled', fillcolor='#A5D6A7')

# ==================== 文件监控 ====================
with dot.subgraph(name='cluster_watch') as c:
    c.attr(label='👁️ 文件监控 (chokidar)', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    
    c.node('watch_init', 'ensureSkillsWatcher()\n初始化监控器', shape='box', style='rounded,filled', fillcolor='#FFECB3')
    
    c.node('watch_paths', '监控路径:\n• &lt;workspace&gt;/skills/\n• ~/.openclaw/skills/\n• extraDirs\n• plugin skills', 
           shape='note', style='filled', fillcolor='#FFE082', fontsize='10')
    
    c.node('watch_events', '监听事件:\nadd / change / unlink', shape='box', style='rounded,filled', fillcolor='#FFECB3')
    
    c.node('debounce', '防抖处理\n(默认 250ms)', shape='box', style='rounded,filled', fillcolor='#FFD54F')

# ==================== Snapshot 创建 ====================
with dot.subgraph(name='cluster_create') as c:
    c.attr(label='🔨 Snapshot 创建', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    
    c.node('build_snapshot', 'buildWorkspaceSkillSnapshot()', shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    
    c.node('load_skills', '1. loadSkillEntries()\n加载并合并 Skills', shape='box', style='rounded,filled', fillcolor='#90CAF9')
    c.node('filter_skills', '2. filterSkillEntries()\n过滤符合条件的 Skills', shape='box', style='rounded,filled', fillcolor='#90CAF9')
    c.node('format_prompt', '3. formatSkillsForPrompt()\n生成 XML 格式', shape='box', style='rounded,filled', fillcolor='#90CAF9')
    c.node('create_obj', '4. 创建 SkillSnapshot 对象\n附带 version', shape='box', style='rounded,filled', fillcolor='#64B5F6')

# ==================== 缓存流程 ====================
with dot.subgraph(name='cluster_cache') as c:
    c.attr(label='💾 缓存到会话', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    
    c.node('ensure_snapshot', 'ensureSkillSnapshot()', shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    
    c.node('check_first', '是否第一轮\n会话?', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.2')
    c.node('check_version', '版本是否\n过期?', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.2')
    c.node('check_exists', '是否已有\nSnapshot?', shape='diamond', style='filled', fillcolor='#CE93D8', width='1.2')
    
    c.node('need_rebuild', '需要重建 Snapshot', shape='box', style='rounded,filled', fillcolor='#BA68C8')
    c.node('use_cached', '使用缓存的 Snapshot', shape='box', style='rounded,filled', fillcolor='#81C784')

# ==================== 存储 ====================
with dot.subgraph(name='cluster_store') as c:
    c.attr(label='📁 持久化存储', style='rounded,filled', fillcolor='#FCE4EC', color='#C2185B', penwidth='2')
    
    c.node('update_memory', '更新内存中的\nsessionStore[sessionKey]', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('update_file', 'updateSessionStore()\n写入 JSON 文件', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('store_path', '存储位置:\n~/.openclaw/sessions.json', shape='note', style='filled', fillcolor='#F48FB1', fontsize='10')

# ==================== 使用 ====================
with dot.subgraph(name='cluster_use') as c:
    c.attr(label='🚀 运行时使用', style='rounded,filled', fillcolor='#E0F2F1', color='#00897B', penwidth='2')
    
    c.node('resolve_prompt', 'resolveSkillsPromptForRun()\n优先使用 snapshot.prompt', shape='box', style='rounded,filled', fillcolor='#B2DFDB')
    c.node('apply_env', 'applySkillEnvOverridesFromSnapshot()\n注入环境变量', shape='box', style='rounded,filled', fillcolor='#B2DFDB')
    c.node('system_prompt', '注入到系统提示词\nbuildAgentSystemPrompt()', shape='box', style='rounded,filled', fillcolor='#80CBC4')

# ==================== 触发时机 ====================
dot.node('trigger_box', '''刷新触发时机:
1. 新会话第一轮
2. snapshot.version &lt; snapshotVersion
3. 文件监控检测到变化
4. 远程节点状态变化''', shape='note', style='filled', fillcolor='#FFECB3', fontsize='10')

# ==================== 连接 ====================

# 标题
dot.edge('title', 'snapshot_struct', style='invis')

# 数据结构关系
dot.edge('snapshot_struct', 'session_struct', label='  存储于  ', style='dashed', color='#9E9E9E')

# 版本管理
dot.edge('global_ver', 'get_version', penwidth='1.5')
dot.edge('workspace_ver', 'get_version', penwidth='1.5')
dot.edge('bump_version', 'global_ver', label='  更新  ', color='#4CAF50')
dot.edge('bump_version', 'workspace_ver', label='  更新  ', color='#4CAF50')

# 文件监控
dot.edge('watch_init', 'watch_paths', penwidth='1.5')
dot.edge('watch_paths', 'watch_events', penwidth='1.5')
dot.edge('watch_events', 'debounce', penwidth='1.5')
dot.edge('debounce', 'bump_version', label='  触发  ', penwidth='2', color='#FF9800')

# Snapshot 创建
dot.edge('build_snapshot', 'load_skills', penwidth='1.5')
dot.edge('load_skills', 'filter_skills', penwidth='1.5')
dot.edge('filter_skills', 'format_prompt', penwidth='1.5')
dot.edge('format_prompt', 'create_obj', penwidth='1.5')

# 缓存流程
dot.edge('ensure_snapshot', 'check_first', penwidth='1.5')
dot.edge('check_first', 'need_rebuild', label=' 是 ', color='#E91E63')
dot.edge('check_first', 'check_exists', label=' 否 ', color='#9E9E9E')
dot.edge('check_exists', 'check_version', label=' 是 ', color='#9E9E9E')
dot.edge('check_exists', 'need_rebuild', label=' 否 ', color='#E91E63')
dot.edge('check_version', 'need_rebuild', label=' 是 ', color='#E91E63')
dot.edge('check_version', 'use_cached', label=' 否 ', color='#4CAF50')

# 重建 -> 创建
dot.edge('need_rebuild', 'build_snapshot', penwidth='2', color='#1976D2')
dot.edge('create_obj', 'update_memory', penwidth='1.5')

# 存储
dot.edge('update_memory', 'update_file', penwidth='1.5')
dot.edge('update_file', 'store_path', style='dashed', color='#9E9E9E')

# 使用
dot.edge('use_cached', 'resolve_prompt', penwidth='1.5')
dot.edge('create_obj', 'resolve_prompt', penwidth='1.5', style='dashed')
dot.edge('resolve_prompt', 'apply_env', penwidth='1.5')
dot.edge('apply_env', 'system_prompt', penwidth='1.5')

# 版本检查
dot.edge('get_version', 'check_version', style='dashed', color='#4CAF50')

# Render
output_path = '/workspace/skill_snapshot_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
