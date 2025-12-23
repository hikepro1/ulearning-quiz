import json
import re

def clean_html_tags(text):
    """清除HTML标签"""
    if not text:
        return ""
    # 简单的HTML标签清除
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def check_answers(json_file_path):
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 获取题目列表
    questions = data.get('result', [])
    
    # 遍历所有题目
    for i, question in enumerate(questions, 1):
        question_id = question.get('questionID', '未知ID')
        total_score = question.get('score', 0)
        student_answer = question.get('studentAnswer')
        question_type = question.get('type', 1)
        
        print(f"第{i}题 (ID:{question_id}):")
        
        # 获取学生答案内容
        answer_content = student_answer.get('answer', '')
        student_score = student_answer.get('score', 0)
        
        # 处理选择题（type=1）
        if question_type == 1 and answer_content:
            choice_items = question.get('choiceItemList', [])
            
            if choice_items and len(choice_items) >= 4:
                # 将ABCD映射到选项
                option_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
                
                if answer_content in option_mapping:
                    option_index = option_mapping[answer_content]
                    if option_index < len(choice_items):
                        option_title = choice_items[option_index].get('title', '')
                        clean_title = clean_html_tags(option_title).strip()
                        print(f"  学生答案：{answer_content} - {clean_title}")
                else:
                    print(f"  学生答案：{answer_content} (非标准选项)")
            else:
                print(f"  学生答案：{answer_content} (无选项列表)")
        else:
            # 非选择题或填空题
            print(f"  学生答案：{answer_content}")
        
        # 对比分数
        if student_score == total_score:
            print(f"  答题状态：回答正确")
        else:
            print(f"  答题状态：回答错误 ({student_score}/{total_score})")
        
        print()

# 使用示例
if __name__ == "__main__":
    json_file_path = "示例文件.json"

    check_answers(json_file_path)
