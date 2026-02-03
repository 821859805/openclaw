#!/usr/bin/env python3
"""Generate a flowchart for Skill creation process"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Skill Creation Process', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.6', ranksep='0.7', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='12')
dot.attr('edge', fontname='SimHei,Arial', fontsize='10')

# Start node
dot.node('start', '🚀 用户请求创建 Skill', shape='ellipse', style='filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')

# Step 1: Understanding
with dot.subgraph(name='cluster_step1') as c:
    c.attr(label='📋 第1步: 理解需求', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    c.node('s1_ask', '询问功能范围\n和使用场景', shape='box', style='rounded,filled', fillcolor='#FFECB3')
    c.node('s1_collect', '收集具体示例\n确认触发条件', shape='box', style='rounded,filled', fillcolor='#FFECB3')
    c.node('s1_check', '需求清晰?', shape='diamond', style='filled', fillcolor='#FFE082', width='1.2', height='0.8')

# Step 2: Planning
with dot.subgraph(name='cluster_step2') as c:
    c.attr(label='📐 第2步: 规划资源', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    c.node('s2_analyze', '分析使用场景', shape='box', style='rounded,filled', fillcolor='#E1BEE7')
    c.node('s2_plan', '确定资源类型\nscripts / references / assets', shape='box', style='rounded,filled', fillcolor='#E1BEE7')

# Step 3: Initialize
with dot.subgraph(name='cluster_step3') as c:
    c.attr(label='⚙️ 第3步: 初始化 Skill', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    c.node('s3_init', '运行 init_skill.py\n生成模板目录结构', shape='box', style='rounded,filled', fillcolor='#C8E6C9')

# Step 4: Edit
with dot.subgraph(name='cluster_step4') as c:
    c.attr(label='✏️ 第4步: 编辑 Skill', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    c.node('s4_scripts', '实现 scripts/\n并测试', shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('s4_refs', '编写 references/\n添加 assets/', shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('s4_skillmd', '完善 SKILL.md\n(frontmatter + body)', shape='box', style='rounded,filled', fillcolor='#BBDEFB')
    c.node('s4_need', '需要用户\n提供资源?', shape='diamond', style='filled', fillcolor='#90CAF9', width='1.2', height='0.8')

# Step 5: Package
with dot.subgraph(name='cluster_step5') as c:
    c.attr(label='📦 第5步: 打包 Skill', style='rounded,filled', fillcolor='#FCE4EC', color='#C2185B', penwidth='2')
    c.node('s5_pkg', '运行 package_skill.py', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('s5_valid', '验证通过?', shape='diamond', style='filled', fillcolor='#F48FB1', width='1.2', height='0.8')
    c.node('s5_fix', '修复错误', shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('s5_done', '生成 .skill 文件\n交付给用户', shape='box', style='rounded,filled', fillcolor='#F8BBD9')

# Step 6: Iterate
with dot.subgraph(name='cluster_step6') as c:
    c.attr(label='🔄 第6步: 迭代', style='rounded,filled', fillcolor='#ECEFF1', color='#546E7A', penwidth='2')
    c.node('s6_test', '用户测试 Skill', shape='box', style='rounded,filled', fillcolor='#CFD8DC')
    c.node('s6_need', '需要改进?', shape='diamond', style='filled', fillcolor='#B0BEC5', width='1.2', height='0.8')

# End node
dot.node('end', '✅ 完成', shape='ellipse', style='filled', fillcolor='#C8E6C9', color='#388E3C', penwidth='2')

# Edges - Main flow
dot.edge('start', 's1_ask', penwidth='1.5')
dot.edge('s1_ask', 's1_collect', penwidth='1.5')
dot.edge('s1_collect', 's1_check', penwidth='1.5')
dot.edge('s1_check', 's1_ask', label=' 否 ', color='#E57373', fontcolor='#C62828', penwidth='1.5', style='dashed')
dot.edge('s1_check', 's2_analyze', label=' 是 ', color='#81C784', fontcolor='#2E7D32', penwidth='1.5')

dot.edge('s2_analyze', 's2_plan', penwidth='1.5')
dot.edge('s2_plan', 's3_init', penwidth='1.5')

dot.edge('s3_init', 's4_scripts', penwidth='1.5')
dot.edge('s4_scripts', 's4_refs', penwidth='1.5')
dot.edge('s4_refs', 's4_skillmd', penwidth='1.5')
dot.edge('s4_skillmd', 's4_need', penwidth='1.5')
dot.edge('s4_need', 's4_scripts', label=' 是 ', color='#E57373', fontcolor='#C62828', penwidth='1.5', style='dashed')
dot.edge('s4_need', 's5_pkg', label=' 否 ', color='#81C784', fontcolor='#2E7D32', penwidth='1.5')

dot.edge('s5_pkg', 's5_valid', penwidth='1.5')
dot.edge('s5_valid', 's5_fix', label=' 否 ', color='#E57373', fontcolor='#C62828', penwidth='1.5', style='dashed')
dot.edge('s5_fix', 's5_pkg', penwidth='1.5', style='dashed')
dot.edge('s5_valid', 's5_done', label=' 是 ', color='#81C784', fontcolor='#2E7D32', penwidth='1.5')

dot.edge('s5_done', 's6_test', penwidth='1.5')
dot.edge('s6_test', 's6_need', penwidth='1.5')
dot.edge('s6_need', 's4_scripts', label=' 是 ', color='#E57373', fontcolor='#C62828', penwidth='1.5', style='dashed')
dot.edge('s6_need', 'end', label=' 否 ', color='#81C784', fontcolor='#2E7D32', penwidth='1.5')

# Render
output_path = '/workspace/skill_creation_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
