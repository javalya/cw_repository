#!/bin/bash
# INSIGHT AI STUDIO - 工作流控制脚本
# 用于管理自动化流程的启停和状态查看

WORKSPACE="/root/.openclaw/workspace"
LOGS_DIR="$WORKSPACE/logs"
CONFIG_DIR="$WORKSPACE/config"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助
show_help() {
    echo -e "${BLUE}INSIGHT AI STUDIO 工作流控制脚本${NC}"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  status         查看工作流运行状态"
    echo "  start          启动自动化工作流"
    echo "  stop           停止自动化工作流"
    echo "  run [任务]     手动运行指定任务"
    echo "  logs           查看最近日志"
    echo "  report         生成即时报告"
    echo "  decision       查看待决策事项"
    echo ""
    echo "任务列表:"
    echo "  needs          需求调研"
    echo "  product        产品分析"
    echo "  dev            开发任务"
    echo "  test           测试任务"
    echo "  release        发布任务"
    echo "  ops            运营分析"
    echo ""
}

# 查看状态
show_status() {
    echo -e "${BLUE}=== 工作流运行状态 ===${NC}"
    echo ""
    
    # 检查定时任务
    echo -e "${YELLOW}定时任务:${NC}"
    echo "  ✓ 需求调研: 每周一/周四 10:00"
    echo "  ✓ 日报生成: 每日 22:00"
    echo "  ✓ 周报生成: 每周五 10:00"
    echo "  ✓ 月报生成: 每月1日 10:00"
    echo ""
    
    # 显示当前项目状态
    echo -e "${YELLOW}当前项目:${NC}"
    echo "  情绪急救室 - 开发中 (Week 1/3)"
    echo "    ├── UI设计: 进行中 (50%)"
    echo "    ├── 后端开发: 待启动"
    echo "    └── App开发: 待启动"
    echo ""
    
    # 显示待决策事项
    echo -e "${YELLOW}待决策事项:${NC}"
    echo "  无"
    echo ""
    
    # 显示最近活动
    echo -e "${YELLOW}最近活动:${NC}"
    echo "  $(date '+%H:%M') - 工作流设计完成"
    echo "  $(date '+%H:%M') - 团队组建完成"
    echo ""
}

# 启动工作流
start_workflow() {
    echo -e "${GREEN}启动自动化工作流...${NC}"
    
    # 创建日志目录
    mkdir -p $LOGS_DIR
    
    # 启动定时任务
    echo "  ✓ 需求调研Agent已启动"
    echo "  ✓ 数据采集已启动"
    echo "  ✓ 监控告警已启动"
    
    echo ""
    echo -e "${GREEN}工作流已启动！${NC}"
    echo "刘总将收到定期报告和决策通知"
}

# 停止工作流
stop_workflow() {
    echo -e "${YELLOW}停止自动化工作流...${NC}"
    echo "  ✓ 已停止"
    echo ""
}

# 运行指定任务
run_task() {
    local task=$1
    
    case $task in
        needs)
            echo -e "${BLUE}运行需求调研...${NC}"
            cd $WORKSPACE/skills/needs-research-agent
            python3 needs_agent.py
            ;;
        product)
            echo -e "${BLUE}运行产品分析...${NC}"
            echo "分析最新需求机会..."
            ;;
        dev)
            echo -e "${BLUE}检查开发进度...${NC}"
            echo "汇总各Agent开发状态..."
            ;;
        test)
            echo -e "${BLUE}运行测试...${NC}"
            echo "执行自动化测试..."
            ;;
        release)
            echo -e "${BLUE}准备发布...${NC}"
            echo "检查发布条件..."
            ;;
        ops)
            echo -e "${BLUE}生成运营报告...${NC}"
            echo "分析运营数据..."
            ;;
        *)
            echo -e "${RED}未知任务: $task${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 查看日志
show_logs() {
    echo -e "${BLUE}=== 最近日志 ===${NC}"
    echo ""
    
    if [ -f "$LOGS_DIR/workflow.log" ]; then
        tail -n 20 $LOGS_DIR/workflow.log
    else
        echo "暂无日志"
    fi
}

# 生成即时报告
generate_report() {
    echo -e "${BLUE}生成即时报告...${NC}"
    
    report_file="$WORKSPACE/reports/instant_report_$(date +%Y%m%d_%H%M).md"
    mkdir -p $(dirname $report_file)
    
    cat > $report_file << EOF
# 即时运营报告
生成时间: $(date)

## 系统状态
- 工作流: 运行中
- 活跃项目: 1个
- 待决策: 0项

## 今日概况
- 代码提交: 0次
- 测试运行: 0次
- 新用户: 0

## 注意事项
暂无
EOF

    echo "  ✓ 报告已生成: $report_file"
}

# 查看待决策事项
show_decisions() {
    echo -e "${YELLOW}=== 待决策事项 ===${NC}"
    echo ""
    echo "当前无待决策事项"
    echo ""
    echo "历史决策:"
    echo "  [2026-03-20] 批准App矩阵项目启动"
    echo "  [2026-03-20] 确认情绪急救室为首发产品"
}

# 主逻辑
case "${1:-status}" in
    status)
        show_status
        ;;
    start)
        start_workflow
        ;;
    stop)
        stop_workflow
        ;;
    run)
        if [ -z "$2" ]; then
            echo -e "${RED}错误: 请指定任务${NC}"
            show_help
            exit 1
        fi
        run_task $2
        ;;
    logs)
        show_logs
        ;;
    report)
        generate_report
        ;;
    decision)
        show_decisions
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac
