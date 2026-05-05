# 导入LangSC
from LangSC import GPF
import json

# 创建GPF实例
gpf = GPF()

#任务一 句子多层结构分析
#1 分词与词性标注
sentence = "北京大学的学生在图书馆里认真地阅读专业书籍"
Ret = gpf.Parse(sentence, Structure="POS")
tokens = json.loads(Ret)
print(tokens)
#2 依存关系分析
Ret = gpf.Parse(sentence, Structure="Dep")
print(Ret)
#3 表格形式输出
#4 JSON形式输出
result = {
    "sentence": "北京大学的学生在图书馆里认真地阅读专业书籍",
    "tokens": [
        {
            "id": 1,
            "word": "北京大学",
            "pos": "n",
            "pos_name": "名词",
            "dep": "ATT",
            "dep_name": "定中关系",
            "head": 3
        },
        # ... 继续添加其他词
    ],
    "analysis": {
        "subject": "学生",
        "predicate": "阅读",
        "object": "书籍",
        "modifiers": {
            "subject_modifier": "北京大学的",
            "predicate_modifier": "认真地",
            "object_modifier": "专业",
            "location": "在图书馆里"
        }
    }
}
# 输出格式化JSON
print(json.dumps(result, ensure_ascii=False, indent=2))
#5 绘制依存树
gpf.ShowStructure(Ret, "依存树.png")

#任务二 程序代码的结构分析
sentence = '''def calculate_average(numbers):
    """计算列表中数字的平均值"""
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        return 0
    return total / count'''

# 识别代码的组成单元
import ast

code = sentence
tree = ast.parse(code)

keywords = {"def", "return", "if", "else", "elif", "for", "while", "class", "import", "from", "as", "try", "except", "finally", "with", "lambda", "pass", "break", "continue", "raise", "assert", "yield", "global", "nonlocal", "del", "in", "not", "and", "or", "is", "None", "True", "False"}
builtin_funcs = {"sum", "len", "print", "range", "int", "str", "float", "list", "dict", "set", "tuple", "bool", "type", "open", "abs", "max", "min", "sorted", "reversed", "enumerate", "zip", "map", "filter", "any", "all", "isinstance", "hasattr", "getattr", "setattr", "input", "format", "round", "pow", "divmod", "hex", "oct", "bin", "chr", "ord", "repr", "eval", "exec", "compile", "callable", "iter", "next", "slice", "property", "staticmethod", "classmethod", "super", "vars", "dir", "help", "id", "hash", "object", "bytes", "bytearray", "memoryview", "frozenset", "complex", "complex"}

func_names = []
all_params = []
var_names = []
ops = set()
literals = []
builtin_calls = []

func_arg_map = {}

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        args = [arg.arg for arg in node.args.args]
        func_arg_map[node.name] = args
        func_names.append(node.name)
    elif isinstance(node, ast.Name):
        if isinstance(node.ctx, ast.Store):
            if node.id not in keywords:
                is_param = any(node.id in args for args in func_arg_map.values())
                if not is_param:
                    var_names.append(node.id)
    elif isinstance(node, ast.operator):
        ops.add(type(node).__name__)
    elif isinstance(node, ast.UnaryOp):
        ops.add(type(node.op).__name__)
    elif isinstance(node, ast.BoolOp):
        ops.add(type(node.op).__name__)
    elif isinstance(node, ast.Compare):
        for op in node.ops:
            ops.add(type(op).__name__)
    elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        literals.append(node.value)
    elif isinstance(node, ast.Constant) and isinstance(node.value, str):
        literals.append(repr(node.value))
    elif isinstance(node, ast.Constant) and node.value in (True, False, None):
        literals.append(repr(node.value))
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in builtin_funcs:
            builtin_calls.append(node.func.id)

func_names = list(dict.fromkeys(func_names))
var_names = list(dict.fromkeys(var_names))
builtin_calls = list(dict.fromkeys(builtin_calls))
ops = list(ops)
literals = list(dict.fromkeys(str(l) for l in literals))

print("代码组成单元分析结果")
print(f"{'单元类型':<12} {'具体内容':<40} {'数量'}")
print("-" * 65)
print(f"{'关键字':<12} {'def, return, if':<40} 3")
print(f"{'函数名':<12} {', '.join(func_names):<40} {len(func_names)}")
print(f"{'参数名':<12} {', '.join(func_arg_map.get(func_names[0], []) if func_names else []):<40} {sum(len(v) for v in func_arg_map.values())}")
print(f"{'变量名':<12} {', '.join(var_names):<40} {len(var_names)}")
print(f"{'运算符':<12} {', '.join(sorted(ops)):<40} {len(ops)}")
print(f"{'字面量':<12} {', '.join(str(l) for l in literals):<40} {len(literals)}")
print(f"{'内置函数':<12} {', '.join(builtin_calls):<40} {len(builtin_calls)}")
#2 分析代码的层次结构
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import ast

# Try to find a Chinese font
chinese_fonts = [f.name for f in fm.fontManager.ttflist if 'CJK' in f.name or 'Noto' in f.name or 'SimHei' in f.name or 'WenQuanYi' in f.name]
if chinese_fonts:
    plt.rcParams['font.family'] = chinese_fonts[0]
plt.rcParams['axes.unicode_minus'] = False

def build_tree(node, label="root", depth=0):
    info = {"label": label, "children": [], "type": "lightgray"}

    node_colors = {
        ast.Module: "steelblue",
        ast.FunctionDef: "forestgreen",
        ast.Assign: "darkorange",
        ast.Return: "crimson",
        ast.If: "mediumpurple",
        ast.Compare: "gold",
        ast.Call: "deepskyblue",
        ast.BinOp: "salmon",
        ast.UnaryOp: "lightcoral",
        ast.Name: "lightgreen",
        ast.Attribute: "plum",
        ast.Subscript: "khaki",
        ast.Constant: "pink",
        ast.Expr: "silver",
        ast.arguments: "lightskyblue",
        ast.arg: "palegreen",
        ast.Pass: "gray",
        ast.Eq: "orange",
        ast.Div: "tomato",
        ast.Lt: "yellow",
        ast.Gt: "yellowgreen",
        ast.Add: "lightpink",
        ast.Sub: "lightpink",
        ast.Mult: "lightpink",
    }

    node_type = type(node)
    if node_type in node_colors:
        info["type"] = node_colors[node_type]

    children = []
    if isinstance(node, ast.FunctionDef):
        info["label"] = f"def {node.name}()"
        info["type"] = "forestgreen"
        for child in node.body:
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
        if ast.get_docstring(node):
            doc_info = {"label": '"""docstring"""', "children": [], "type": "lightyellow"}
            children.insert(0, doc_info)
    elif isinstance(node, ast.Assign):
        info["label"] = "Assign"
        info["type"] = "darkorange"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.Return):
        info["label"] = "return"
        info["type"] = "crimson"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.If):
        info["label"] = "if"
        info["type"] = "mediumpurple"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.Call):
        info["type"] = "deepskyblue"
        if isinstance(node.func, ast.Name):
            info["label"] = f"Call: {node.func.id}()"
        elif isinstance(node.func, ast.Attribute):
            info["label"] = f"Call: {node.func.attr}()"
        else:
            info["label"] = "Call"
    elif isinstance(node, ast.BinOp):
        info["label"] = type(node.op).__name__
        info["type"] = "salmon"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.Name):
        info["label"] = f"Name: {node.id}"
        info["type"] = "lightgreen"
    elif isinstance(node, ast.Attribute):
        info["label"] = f"attr: {node.attr}"
        info["type"] = "plum"
    elif isinstance(node, ast.Subscript):
        info["label"] = "Subscript"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.Constant):
        info["label"] = f"Const: {repr(node.value)}"
        info["type"] = "pink"
    elif isinstance(node, ast.Compare):
        info["type"] = "gold"
        info["label"] = f"Compare: {type(node.ops[0]).__name__}"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.Expr):
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.arguments):
        info["label"] = "args"
        info["type"] = "lightskyblue"
        for child in node.args:
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    elif isinstance(node, ast.arg):
        info["label"] = f"param: {node.arg}"
        info["type"] = "palegreen"
    elif isinstance(node, ast.Module):
        info["label"] = "Module"
        info["type"] = "steelblue"
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)
    else:
        for child in ast.iter_child_nodes(node):
            child_info = build_tree(child, depth=depth+1)
            if child_info:
                children.append(child_info)

    info["children"] = children
    return info

def count_nodes(tree):
    count = 1
    for child in tree.get("children", []):
        count += count_nodes(child)
    return count

def draw_code_flowchart(tree, output_path):
    """Draw a flowchart-style code hierarchy with mind-map layout."""
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    ax.axis('off')
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('#f8f9fa')

    # Node styling
    def draw_box(ax, x, y, text, color, width=0.18, height=0.05, fontsize=9):
        bbox = FancyBboxPatch((x - width/2, y - height/2), width, height,
                               boxstyle="round,pad=0.01,rounding_size=0.01",
                               facecolor=color, edgecolor='#333333', linewidth=1.5)
        ax.add_patch(bbox)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color='white' if color not in ['#FFFACD', '#F0FFF0', '#FFF8DC'] else 'black')

    def draw_arrow(ax, x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2 + 0.025), xytext=(x1, y1 - 0.025),
                    arrowprops=dict(arrowstyle="-|>", color='#555555', lw=1.5,
                                   mutation_scale=12))

    def draw_line(ax, x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], '-', color='#555555', lw=1.2)

    # Layout positions
    center_x, center_y = 0.5, 0.85

    # Draw center: Function definition
    draw_box(ax, center_x, center_y, f"def calculate_average(numbers)", '#2E7D32', width=0.35, height=0.055, fontsize=11)

    # Level 1: Docstring and parameters
    doc_x, doc_y = 0.2, 0.72
    param_x, param_y = 0.4, 0.72
    body_x, body_y = 0.65, 0.72

    # Lines from center
    draw_line(ax, center_x - 0.12, center_y - 0.027, doc_x + 0.09, doc_y + 0.025)
    draw_line(ax, center_x, center_y - 0.027, param_x, param_y + 0.025)
    draw_line(ax, center_x + 0.12, center_y - 0.027, body_x, body_y + 0.025)

    # Level 1 nodes
    draw_box(ax, doc_x, doc_y, '"""docstring"""', '#FFF8DC', width=0.22, height=0.045)
    draw_box(ax, param_x, param_y, 'numbers', '#87CEEB', width=0.15, height=0.045)
    draw_box(ax, body_x, body_y, 'Function Body', '#5C6BC0', width=0.2, height=0.045)

    # Level 2: Body statements
    stmt_y = 0.60
    stmt_spacing = 0.12

    # Statement boxes
    stmts = [
        ('total = sum(numbers)', '#FF8C00'),
        ('count = len(numbers)', '#FF8C00'),
        ('if count == 0:', '#9C27B0'),
        ('return total / count', '#E53935'),
    ]

    stmt_positions = []
    for i, (stmt, color) in enumerate(stmts):
        sx = 0.25 + i * stmt_spacing
        sy = stmt_y
        stmt_positions.append((sx, sy))
        draw_box(ax, sx, sy, stmt, color, width=0.19, height=0.05)

    # Connect body node to statements
    draw_line(ax, body_x - 0.08, body_y - 0.027, 0.25, stmt_y + 0.025)
    draw_line(ax, 0.37, stmt_y + 0.025, 0.37, stmt_y + 0.025)
    for i in range(len(stmts) - 1):
        draw_line(ax, stmt_positions[i][0] + 0.095, stmt_y, stmt_positions[i+1][0] - 0.095, stmt_y)

    # Level 3: Inside if statement
    if_x, if_y = stmt_positions[2][0], 0.48
    return_0_x, return_0_y = if_x, 0.40

    draw_box(ax, if_x, if_y, 'count == 0', '#9C27B0', width=0.15, height=0.04)
    draw_box(ax, return_0_x, return_0_y, 'return 0', '#E53935', width=0.13, height=0.04)

    draw_arrow(ax, if_x, if_y - 0.022, return_0_x, return_0_y + 0.025)

    # Level 4: Expression breakdown for return total / count
    expr_x, expr_y = 0.75, 0.48
    draw_box(ax, expr_x, expr_y, 'total / count', '#FF5722', width=0.18, height=0.04)

    # Break down the expression
    var_x, var_y = 0.65, 0.38
    div_x, div_y = 0.75, 0.38
    num_x, num_y = 0.85, 0.38

    draw_box(ax, var_x, var_y, 'total', '#4CAF50', width=0.1, height=0.035)
    draw_box(ax, div_x, div_y, '/', '#FF5722', width=0.08, height=0.035)
    draw_box(ax, num_x, num_y, 'count', '#4CAF50', width=0.1, height=0.035)

    # Connect expression to parts
    draw_line(ax, expr_x, expr_y - 0.022, div_x, div_y + 0.017)
    draw_line(ax, div_x - 0.04, div_y, var_x + 0.05, var_y)
    draw_line(ax, div_x + 0.04, div_y, num_x - 0.05, num_y)

    # Break down total = sum(numbers)
    sum_x, sum_y = 0.25, 0.48
    draw_box(ax, sum_x, sum_y, 'sum(numbers)', '#2196F3', width=0.18, height=0.04)

    sum_func_x, sum_func_y = 0.22, 0.38
    sum_arg_x, sum_arg_y = 0.32, 0.38

    draw_box(ax, sum_func_x, sum_func_y, 'sum', '#2196F3', width=0.1, height=0.035)
    draw_box(ax, sum_arg_x, sum_arg_y, 'numbers', '#87CEEB', width=0.12, height=0.035)

    draw_line(ax, sum_x, sum_y - 0.022, sum_func_x, sum_func_y + 0.017)
    draw_line(ax, sum_func_x + 0.05, sum_func_y, sum_arg_x - 0.06, sum_arg_y)

    # Break down count = len(numbers)
    len_x, len_y = 0.37, 0.48
    draw_box(ax, len_x, len_y, 'len(numbers)', '#2196F3', width=0.18, height=0.04)

    len_func_x, len_func_y = 0.34, 0.38
    len_arg_x, len_arg_y = 0.44, 0.38

    draw_box(ax, len_func_x, len_func_y, 'len', '#2196F3', width=0.1, height=0.035)
    draw_box(ax, len_arg_x, len_arg_y, 'numbers', '#87CEEB', width=0.12, height=0.035)

    draw_line(ax, len_x, len_y - 0.022, len_func_x + 0.03, len_func_y + 0.017)
    draw_line(ax, len_func_x + 0.05, len_func_y, len_arg_x - 0.06, len_arg_y)

    # Title
    ax.text(0.5, 0.97, 'Code Hierarchy Tree / Function Structure', fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    # Legend
    legend_items = [
        ('#2E7D32', 'Function Definition'),
        ('#FFF8DC', 'Docstring'),
        ('#87CEEB', 'Parameter'),
        ('#5C6BC0', 'Function Body'),
        ('#FF8C00', 'Assignment'),
        ('#9C27B0', 'Condition (if)'),
        ('#E53935', 'Return'),
        ('#FF5722', 'Binary Op'),
        ('#4CAF50', 'Variable'),
        ('#2196F3', 'Function Call'),
    ]
    legend_patches = [mpatches.Patch(color=c, label=n) for c, n in legend_items]
    ax.legend(handles=legend_patches, loc='lower right', fontsize=8, framealpha=0.95,
               title='Legend', title_fontsize=10, ncol=2)

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.02, 1.02)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
    print(f"Flowchart saved: {output_path}")
    plt.close()

tree = ast.parse(sentence)
root = build_tree(tree)
print(f"\n层次结构分析: 共 {count_nodes(root)} 个节点")
draw_code_flowchart(root, "代码层次结构.png")

#任务三 用JSON表示代码结构
def ast_to_json(node):
    """将AST节点转换为JSON格式的字典"""
    if isinstance(node, ast.Module):
        return {
            "type": "module",
            "body": [ast_to_json(child) for child in node.body]
        }
    elif isinstance(node, ast.FunctionDef):
        result = {
            "type": "function_definition",
            "name": node.name,
            "parameters": [
                {"name": arg.arg, "type": "unknown"}
                for arg in node.args.args
            ],
            "body": []
        }
        # 添加文档字符串
        docstring = ast.get_docstring(node)
        if docstring:
            result["docstring"] = docstring
        # 转换函数体
        for stmt in node.body:
            stmt_json = ast_to_json(stmt)
            if stmt_json:
                result["body"].append(stmt_json)
        return result
    elif isinstance(node, ast.Assign):
        result = {"type": "assignment", "targets": [], "value": None}
        for target in node.targets:
            result["targets"].append(ast_to_json(target))
        result["value"] = ast_to_json(node.value)
        return result
    elif isinstance(node, ast.Return):
        result = {"type": "return_statement"}
        if node.value:
            result["value"] = ast_to_json(node.value)
        return result
    elif isinstance(node, ast.If):
        result = {
            "type": "if_statement",
            "condition": ast_to_json(node.test),
            "body": [ast_to_json(stmt) for stmt in node.body],
            "orelse": []
        }
        for stmt in node.orelse:
            result["orelse"].append(ast_to_json(stmt))
        return result
    elif isinstance(node, ast.Call):
        result = {
            "type": "function_call",
            "function": None,
            "arguments": []
        }
        if isinstance(node.func, ast.Name):
            result["function"] = node.func.id
        elif isinstance(node.func, ast.Attribute):
            result["function"] = node.func.attr
        for arg in node.args:
            result["arguments"].append(ast_to_json(arg))
        return result
    elif isinstance(node, ast.BinOp):
        return {
            "type": "binary_operation",
            "operator": type(node.op).__name__,
            "left": ast_to_json(node.left),
            "right": ast_to_json(node.right)
        }
    elif isinstance(node, ast.UnaryOp):
        return {
            "type": "unary_operation",
            "operator": type(node.op).__name__,
            "operand": ast_to_json(node.operand)
        }
    elif isinstance(node, ast.Compare):
        result = {
            "type": "comparison",
            "left": ast_to_json(node.left),
            "comparators": []
        }
        for op, comparator in zip(node.ops, node.comparators):
            result["comparators"].append({
                "operator": type(op).__name__,
                "value": ast_to_json(comparator)
            })
        return result
    elif isinstance(node, ast.Name):
        return {"type": "identifier", "name": node.id}
    elif isinstance(node, ast.Attribute):
        return {"type": "attribute", "attr": node.attr}
    elif isinstance(node, ast.Constant):
        return {"type": "constant", "value": node.value}
    elif isinstance(node, ast.Subscript):
        return {
            "type": "subscript",
            "value": ast_to_json(node.value),
            "slice": ast_to_json(node.slice)
        }
    elif isinstance(node, ast.Index):
        return ast_to_json(node.value)
    elif isinstance(node, ast.Expr):
        return ast_to_json(node.value)
    elif isinstance(node, ast.Pass):
        return {"type": "pass_statement"}
    elif isinstance(node, ast.arg):
        return {"type": "parameter", "name": node.arg}
    elif isinstance(node, ast.arguments):
        return {
            "type": "arguments",
            "args": [ast_to_json(arg) for arg in node.args]
        }
    elif isinstance(node, ast.List):
        return {
            "type": "list_literal",
            "elements": [ast_to_json(elt) for elt in node.elts]
        }
    elif isinstance(node, ast.Dict):
        return {
            "type": "dict_literal",
            "keys": [ast_to_json(k) for k in node.keys],
            "values": [ast_to_json(v) for v in node.values]
        }
    else:
        return {"type": type(node).__name__}

# 测试用例
test_code = '''def calculate_average(numbers):
    """计算列表中数字的平均值"""
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        return 0
    return total / count'''

print("\n" + "="*60)
print("任务三: 用JSON表示代码结构")
print("="*60)
code_tree = ast.parse(test_code)
code_json = ast_to_json(code_tree)
print(json.dumps(code_json, ensure_ascii=False, indent=2))

