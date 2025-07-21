import pytest
from playwright.sync_api import Page, expect
import time

"""
注意: 这个测试需要安装Playwright并配置好pytest-playwright
安装方法:
pip install pytest-playwright
playwright install
"""

# 测试环境配置
@pytest.fixture(scope="module")
def app_url():
    """获取应用URL，支持本地开发和CI环境"""
    # 在CI环境中，可能会有不同的URL
    # 这里使用环境变量，如果没有设置则使用本地开发URL
    import os
    return os.environ.get("TEST_APP_URL", "http://localhost:3000")

# 测试用户提交目标到计划生成的完整流程
def test_goal_to_plan_workflow(page: Page, app_url: str):
    """
    测试用户从提交目标到查看生成的计划的完整流程
    
    步骤:
    1. 访问首页
    2. 填写目标输入框
    3. 提交目标
    4. 等待计划生成
    5. 验证计划已展示在页面上
    """
    # 访问应用首页
    page.goto(app_url)
    
    # 等待页面加载完成
    page.wait_for_selector("h1:has-text('自适应计划系统')")
    
    # 检查创建计划按钮是否存在并点击
    create_plan_button = page.get_by_role("button", name="创建新计划")
    expect(create_plan_button).to_be_visible()
    create_plan_button.click()
    
    # 验证目标输入表单是否出现
    goal_input = page.locator("input[placeholder*='例如: 我想在3个月内学习Python']")
    expect(goal_input).to_be_visible()
    
    # 填写目标
    goal_input.fill("我想在3个月内学习Python数据科学")
    
    # 填写时间范围（可选）
    timeframe_input = page.locator("input[placeholder*='例如: 3个月']")
    timeframe_input.fill("3个月")
    
    # 提交表单
    submit_button = page.get_by_role("button", name="创建计划")
    submit_button.click()
    
    # 等待加载状态指示器
    loading_indicator = page.locator("text=正在生成您的计划")
    expect(loading_indicator).to_be_visible(timeout=5000)  # 5秒内应该出现
    
    # 等待计划区域出现 - 增加较长的超时时间，因为后端处理可能需要时间
    plan_area = page.locator(".bg-white >> text=任务清单")
    expect(plan_area).to_be_visible(timeout=60000)  # 60秒超时
    
    # 验证计划内容
    expect(page.locator("text=Python数据科学")).to_be_visible()
    
    # 检查是否有任务项
    tasks = page.locator("li:has-text('任务')").all()
    assert len(tasks) > 0, "应至少显示一个任务项"
    
    # 验证WebSocket连接状态
    ws_status = page.locator("text=WebSocket状态: 已连接")
    expect(ws_status).to_be_visible()

# 测试提交反馈后计划调整的流程
def test_feedback_adjustment_workflow(page: Page, app_url: str):
    """
    测试用户提交反馈后系统调整计划的流程
    
    假设前一个测试已经创建了计划，这个测试专注于反馈部分
    """
    # 访问应用首页（已有计划）
    page.goto(app_url)
    
    # 等待页面加载完成，确认计划已显示
    plan_area = page.locator(".bg-white >> text=任务清单")
    expect(plan_area).to_be_visible(timeout=10000)
    
    # 找到第一个任务
    first_task = page.locator("li:has-text('任务')").first
    expect(first_task).to_be_visible()
    
    # 点击反馈按钮（假设每个任务旁边有反馈按钮）
    feedback_button = first_task.locator("button:has-text('反馈')")
    feedback_button.click()
    
    # 等待反馈对话框出现
    feedback_dialog = page.locator("div[role='dialog']:has-text('提交反馈')")
    expect(feedback_dialog).to_be_visible()
    
    # 选择反馈类型
    feedback_type = page.locator("select[name='feedbackType']")
    feedback_type.select_option("TOO_HARD")
    
    # 填写反馈内容
    comment_input = page.locator("textarea[name='comment']")
    comment_input.fill("这个任务对我来说太难了，能不能简化一些？")
    
    # 提交反馈
    submit_feedback = page.locator("button:has-text('提交')").nth(1)  # 使用nth避免与其他提交按钮混淆
    submit_feedback.click()
    
    # 等待反馈提交成功的通知
    success_message = page.locator("text=反馈已提交")
    expect(success_message).to_be_visible(timeout=5000)
    
    # 等待计划更新（可能需要较长时间）
    page.wait_for_timeout(3000)  # 等待3秒让后端处理
    
    # 检查是否有计划更新提示
    update_message = page.locator("text=计划已更新")
    expect(update_message).to_be_visible(timeout=30000)
    
    # 验证更新后的计划包含修改标记
    changelog = page.locator("text=根据您的反馈")
    expect(changelog).to_be_visible() 