#!/usr/bin/env python3
"""Generate a flowchart for SkillCommandSpec matching process"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='SkillCommandSpec Matching', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.5', ranksep='0.6', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='11')
dot.attr('edge', fontname='SimHei,Arial', fontsize='9')

# ==================== 标题 ====================
dot.node('title', '🔍 SkillCommandSpec 查找匹配流程', shape='plaintext', fontsize='16', fontcolor='#1565C0')

# ==================== 第一阶段：构建命令规格列表 ====================
with dot.subgraph(name='cluster_build') as c:
    c.attr(label='📋 第一阶段: 构建 SkillCommandSpec[]', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    
    c.node('load_entries', 'loadSkillEntries()\n加载并合并 Skills', shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('filter_eligible', 'filterSkillEntries()\n过滤符合条件的 Skills', shape='box', style='rounded,filled', fillcolor='#90CAF9')
    c.node('filter_invocable', '过滤 userInvocable !== false\n只保留可调用的 Skills', shape='box', style='rounded,filled', fillcolor='#64B5F6')
    
    c.node('reserved_names', '获取保留命令名\n/new, /reset, /status...', shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    
    c.node('sanitize', 'sanitizeSkillCommandName()\n规范化名称 (小写+连字符)', shape='box', style='rounded,filled', fillcolor='#42A5F5')
    c.node('dedupe', 'resolveUniqueSkillCommandName()\n去重 (冲突时加后缀 _2, _3...)', shape='box', style='rounded,filled', fillcolor='#42A5F5')
    
    c.node('build_spec', '''构建 SkillCommandSpec {
  name: "weather"         // 命令名
  skillName: "weather"    // 原始 skill 名
  description: "..."      // 描述 (max 100字符)
  dispatch?: { kind, toolName, argMode }
}''', shape='note', style='filled', fillcolor='#1E88E5', fontcolor='white', fontsize='9')

# ==================== 第二阶段：用户输入解析 ====================
with dot.subgraph(name='cluster_input') as c:
    c.attr(label='💬 第二阶段: 用户输入解析', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    
    c.node('user_input', '用户发送消息\n例: "/weather 北京"', shape='ellipse', style='filled', fillcolor='#FFECB3')
    c.node('check_slash', '是否以 / 开头?', shape='diamond', style='filled', fillcolor='#FFE082', width='1.2')
    c.node('not_command', '不是命令\n交给 LLM 处理', shape='box', style='rounded,filled', fillcolor='#FFCDD2')
    
    c.node('regex_parse', '''正则解析:
/^\/([^\\s]+)(?:\\s+([\\s\\S]+))?$/
提取: commandName, args''', shape='box', style='rounded,filled', fillcolor='#FFD54F', fontsize='10')
    
    c.node('check_skill_cmd', 'commandName === "skill"?', shape='diamond', style='filled', fillcolor='#FFE082', width='1.2')

# ==================== 第三阶段：查找匹配 ====================
with dot.subgraph(name='cluster_match') as c:
    c.attr(label='🎯 第三阶段: 查找匹配', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    
    # /skill <name> 路径
    c.node('skill_syntax', '/skill &lt;name&gt; [args] 语法\n再次解析提取 skillName', shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    c.node('find_skill_cmd', 'findSkillCommand()\n多策略匹配', shape='box', style='rounded,filled', fillcolor='#A5D6A7')
    
    # 直接 /<name> 路径
    c.node('direct_syntax', '/&lt;name&gt; [args] 语法\n直接使用 commandName', shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    c.node('direct_find', 'skillCommands.find()\nname === commandName', shape='box', style='rounded,filled', fillcolor='#A5D6A7')

# ==================== 匹配策略 ====================
with dot.subgraph(name='cluster_strategy') as c:
    c.attr(label='🔄 findSkillCommand() 匹配策略', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    
    c.node('normalize_input', 'normalizeSkillCommandLookup()\n输入规范化: 小写 + 空格/下划线→连字符', shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    
    c.node('match1', '策略1: entry.name === input\n(小写精确匹配)', shape='box', style='rounded,filled', fillcolor='#CE93D8')
    c.node('match2', '策略2: entry.skillName === input\n(原始名小写匹配)', shape='box', style='rounded,filled', fillcolor='#CE93D8')
    c.node('match3', '策略3: normalize(name) === normalize(input)\n(规范化后匹配)', shape='box', style='rounded,filled', fillcolor='#CE93D8')
    c.node('match4', '策略4: normalize(skillName) === normalize(input)\n(规范化后匹配)', shape='box', style='rounded,filled', fillcolor='#BA68C8')
    
    c.node('match_result', '返回第一个匹配的\nSkillCommandSpec', shape='box', style='rounded,filled', fillcolor='#9C27B0', fontcolor='white')

# ==================== 结果处理 ====================
with dot.subgraph(name='cluster_result') as c:
    c.attr(label='📤 返回结果', style='rounded,filled', fillcolor='#FCE4EC', color='#C2185B', penwidth='2')
    
    c.node('found', '找到匹配', shape='diamond', style='filled', fillcolor='#F48FB1', width='1')
    c.node('return_match', '''返回 {
  command: SkillCommandSpec,
  args: "北京"  // 可选参数
}''', shape='note', style='filled', fillcolor='#F8BBD9', fontsize='10')
    c.node('return_null', '返回 null\n非 Skill 命令', shape='box', style='rounded,filled', fillcolor='#FFCDD2')

# ==================== 示例 ====================
dot.node('example', '''匹配示例:
输入: "/weather 北京"
  → commandName: "weather"
  → 匹配: SkillCommandSpec { name: "weather" }
  → 返回: { command: {...}, args: "北京" }

输入: "/skill my-skill hello"
  → commandName: "skill"
  → skillName: "my-skill" 
  → 匹配: SkillCommandSpec { skillName: "my-skill" }
  → 返回: { command: {...}, args: "hello" }

输入: "/my_skill test" (下划线)
  → normalize: "my-skill"
  → 匹配: normalize(entry.name) === "my-skill"
''', shape='note', style='filled', fillcolor='#E0F7FA', fontsize='9')

# ==================== 连接 ====================

# 构建阶段
dot.edge('title', 'load_entries', style='invis')
dot.edge('load_entries', 'filter_eligible', penwidth='1.5')
dot.edge('filter_eligible', 'filter_invocable', penwidth='1.5')
dot.edge('reserved_names', 'sanitize', style='dashed', color='#9E9E9E')
dot.edge('filter_invocable', 'sanitize', penwidth='1.5')
dot.edge('sanitize', 'dedupe', penwidth='1.5')
dot.edge('dedupe', 'build_spec', penwidth='1.5')

# 用户输入
dot.edge('user_input', 'check_slash', penwidth='1.5')
dot.edge('check_slash', 'not_command', label=' 否 ', color='#E57373')
dot.edge('check_slash', 'regex_parse', label=' 是 ', color='#81C784')
dot.edge('regex_parse', 'check_skill_cmd', penwidth='1.5')

# 分支
dot.edge('check_skill_cmd', 'skill_syntax', label=' 是 ', color='#FF9800')
dot.edge('check_skill_cmd', 'direct_syntax', label=' 否 ', color='#2196F3')

# /skill 路径
dot.edge('skill_syntax', 'find_skill_cmd', penwidth='1.5')
dot.edge('find_skill_cmd', 'normalize_input', penwidth='1.5', color='#7B1FA2')

# 直接路径
dot.edge('direct_syntax', 'direct_find', penwidth='1.5')
dot.edge('direct_find', 'found', penwidth='1.5')

# 匹配策略
dot.edge('normalize_input', 'match1', penwidth='1.5')
dot.edge('match1', 'match2', label=' 未匹配 ', color='#9E9E9E', style='dashed')
dot.edge('match2', 'match3', label=' 未匹配 ', color='#9E9E9E', style='dashed')
dot.edge('match3', 'match4', label=' 未匹配 ', color='#9E9E9E', style='dashed')
dot.edge('match1', 'match_result', label=' 匹配 ', color='#4CAF50')
dot.edge('match2', 'match_result', label=' 匹配 ', color='#4CAF50')
dot.edge('match3', 'match_result', label=' 匹配 ', color='#4CAF50')
dot.edge('match4', 'match_result', label=' 匹配 ', color='#4CAF50')
dot.edge('match_result', 'found', penwidth='1.5')

# 结果
dot.edge('found', 'return_match', label=' 是 ', color='#4CAF50')
dot.edge('found', 'return_null', label=' 否 ', color='#E57373')
dot.edge('match4', 'return_null', label=' 未匹配 ', color='#E57373', style='dashed')

# Render
output_path = '/workspace/skill_command_match_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
