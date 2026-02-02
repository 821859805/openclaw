#!/usr/bin/env python3
"""Generate a flowchart for Skill requirement understanding process"""

from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Skill Requirement Understanding', format='png')
dot.attr(rankdir='TB', splines='polyline', nodesep='0.5', ranksep='0.6', dpi='150')
dot.attr('node', fontname='SimHei,Arial', fontsize='11')
dot.attr('edge', fontname='SimHei,Arial', fontsize='9')

# ==================== 开始 ====================
dot.node('start', '🎯 用户请求创建 Skill\n(例如: "帮我创建一个图片编辑skill")', 
         shape='ellipse', style='filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')

# ==================== 初始评估 ====================
with dot.subgraph(name='cluster_init') as c:
    c.attr(label='📋 初始评估', style='rounded,filled', fillcolor='#FFF8E1', color='#FFA000', penwidth='2')
    
    c.node('check_clear', '需求是否已经\n足够清晰?', shape='diamond', style='filled', fillcolor='#FFE082', width='1.3')
    c.node('skip_step', '跳过理解需求步骤\n直接进入规划阶段', shape='box', style='rounded,filled', fillcolor='#C8E6C9')

# ==================== 收集信息阶段 ====================
with dot.subgraph(name='cluster_collect') as c:
    c.attr(label='🔍 信息收集循环', style='rounded,filled', fillcolor='#E8F5E9', color='#388E3C', penwidth='2')
    
    c.node('init_context', '初始化上下文\n- 用户原始请求\n- 已知信息列表\n- 待确认问题列表', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9')
    
    c.node('select_question', '选择最重要的\n待确认问题', shape='box', style='rounded,filled', fillcolor='#A5D6A7')
    
    c.node('ask_user', '向用户提问\n(每次1-2个问题)', shape='parallelogram', style='filled', fillcolor='#81C784')
    
    c.node('wait_response', '等待用户回复', shape='box', style='rounded,filled', fillcolor='#A5D6A7')
    
    c.node('parse_response', '解析用户回复\n提取关键信息', shape='box', style='rounded,filled', fillcolor='#A5D6A7')
    
    c.node('update_context', '更新上下文\n- 添加新信息\n- 标记已解答问题\n- 发现新问题', 
           shape='box', style='rounded,filled', fillcolor='#C8E6C9')

# ==================== 问题类型 ====================
with dot.subgraph(name='cluster_questions') as c:
    c.attr(label='❓ 核心问题类型', style='rounded,filled', fillcolor='#F3E5F5', color='#7B1FA2', penwidth='2')
    
    c.node('q_func', '功能范围问题\n"支持哪些功能?\n编辑、旋转、裁剪?"', 
           shape='note', style='filled', fillcolor='#E1BEE7', fontsize='10')
    c.node('q_examples', '使用场景问题\n"能给一些具体的\n使用示例吗?"', 
           shape='note', style='filled', fillcolor='#E1BEE7', fontsize='10')
    c.node('q_trigger', '触发条件问题\n"用户说什么话\n会触发这个skill?"', 
           shape='note', style='filled', fillcolor='#E1BEE7', fontsize='10')
    c.node('q_output', '预期输出问题\n"期望的输出\n是什么格式?"', 
           shape='note', style='filled', fillcolor='#E1BEE7', fontsize='10')

# ==================== 完整性检查 ====================
with dot.subgraph(name='cluster_validate') as c:
    c.attr(label='✅ 完整性检查', style='rounded,filled', fillcolor='#E3F2FD', color='#1976D2', penwidth='2')
    
    c.node('check_complete', '信息是否完整?', shape='diamond', style='filled', fillcolor='#90CAF9', width='1.3')
    
    c.node('check_func', '功能范围明确?', shape='diamond', style='filled', fillcolor='#BBDEFB', width='1.1')
    c.node('check_examples', '有具体示例?', shape='diamond', style='filled', fillcolor='#BBDEFB', width='1.1')
    c.node('check_trigger', '触发条件清晰?', shape='diamond', style='filled', fillcolor='#BBDEFB', width='1.1')

# ==================== 生成假设示例 ====================
with dot.subgraph(name='cluster_generate') as c:
    c.attr(label='💡 生成假设示例', style='rounded,filled', fillcolor='#FCE4EC', color='#C2185B', penwidth='2')
    
    c.node('need_generate', '用户未提供\n足够示例?', shape='diamond', style='filled', fillcolor='#F48FB1', width='1.2')
    c.node('generate_examples', 'Agent 生成假设示例\n"我想象用户可能会说:\n- 移除这张图片的红眼\n- 旋转这张图片90度"', 
           shape='box', style='rounded,filled', fillcolor='#F8BBD9')
    c.node('validate_examples', '请用户确认/修正\n假设示例', shape='parallelogram', style='filled', fillcolor='#F8BBD9')

# ==================== 输出 ====================
with dot.subgraph(name='cluster_output') as c:
    c.attr(label='📝 输出需求文档', style='rounded,filled', fillcolor='#E0F2F1', color='#00897B', penwidth='2')
    
    c.node('compile_req', '汇总需求信息', shape='box', style='rounded,filled', fillcolor='#B2DFDB')
    c.node('req_doc', '需求文档:\n- Skill名称\n- 功能列表\n- 使用场景示例\n- 触发条件\n- 预期输出格式', 
           shape='note', style='filled', fillcolor='#80CBC4', fontsize='10')

dot.node('end', '✅ 进入第2步: 规划资源', 
         shape='ellipse', style='filled', fillcolor='#C8E6C9', color='#388E3C', penwidth='2')

# ==================== 连接 ====================

# 开始到初始评估
dot.edge('start', 'check_clear', penwidth='1.5')
dot.edge('check_clear', 'skip_step', label=' 是 ', color='#81C784', fontcolor='#2E7D32')
dot.edge('check_clear', 'init_context', label=' 否 ', color='#FF9800', fontcolor='#E65100')
dot.edge('skip_step', 'end', penwidth='1.5')

# 信息收集循环
dot.edge('init_context', 'select_question', penwidth='1.5')
dot.edge('select_question', 'ask_user', penwidth='1.5')

# 问题类型连接（虚线表示选择其一）
dot.edge('select_question', 'q_func', style='dashed', color='#9C27B0')
dot.edge('select_question', 'q_examples', style='dashed', color='#9C27B0')
dot.edge('select_question', 'q_trigger', style='dashed', color='#9C27B0')
dot.edge('select_question', 'q_output', style='dashed', color='#9C27B0')

dot.edge('ask_user', 'wait_response', penwidth='1.5')
dot.edge('wait_response', 'parse_response', penwidth='1.5')
dot.edge('parse_response', 'update_context', penwidth='1.5')
dot.edge('update_context', 'check_complete', penwidth='1.5')

# 完整性检查
dot.edge('check_complete', 'check_func', penwidth='1.5')
dot.edge('check_func', 'check_examples', label=' ✓ ', color='#81C784')
dot.edge('check_func', 'select_question', label=' ✗ ', color='#E57373', style='dashed')
dot.edge('check_examples', 'check_trigger', label=' ✓ ', color='#81C784')
dot.edge('check_examples', 'need_generate', label=' ✗ ', color='#E57373')
dot.edge('check_trigger', 'compile_req', label=' ✓ ', color='#81C784')
dot.edge('check_trigger', 'select_question', label=' ✗ ', color='#E57373', style='dashed')

# 生成假设示例
dot.edge('need_generate', 'generate_examples', label=' 是 ', color='#E91E63')
dot.edge('need_generate', 'select_question', label=' 否 ', color='#E57373', style='dashed')
dot.edge('generate_examples', 'validate_examples', penwidth='1.5')
dot.edge('validate_examples', 'update_context', penwidth='1.5')

# 输出
dot.edge('compile_req', 'req_doc', penwidth='1.5')
dot.edge('req_doc', 'end', penwidth='1.5')

# Render
output_path = '/workspace/skill_requirement_flowchart'
dot.render(output_path, cleanup=True)
print(f"Flowchart saved to: {output_path}.png")
