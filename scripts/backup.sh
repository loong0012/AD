#!/bin/bash
# 阿尔兹海默症诊断系统 - 数据备份脚本
# 支持自动备份到本地和远程存储

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${BLUE}[SUCCESS]${NC} $1"
}

# 配置变量
BACKUP_DIR=${BACKUP_DIR:-./backups}
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
HOSTNAME=$(hostname)

# 创建备份目录
create_backup_dirs() {
    mkdir -p $BACKUP_DIR
    mkdir -p $BACKUP_DIR/{database,results,reports,uploads,logs}
    log_info "备份目录已创建: $BACKUP_DIR"
}

# 备份数据库
backup_database() {
    log_info "开始备份数据库..."

    if [ -f alzheimer.db ]; then
        DB_BACKUP_FILE="$BACKUP_DIR/database/alzheimer.db.$TIMESTAMP"
        cp alzheimer.db $DB_BACKUP_FILE

        # 备份wal和shm文件（如果存在）
        if [ -f alzheimer.db-wal ]; then
            cp alzheimer.db-wal $BACKUP_DIR/database/alzheimer.db-wal.$TIMESTAMP
        fi
        if [ -f alzheimer.db-shm ]; then
            cp alzheimer.db-shm $BACKUP_DIR/database/alzheimer.db-shm.$TIMESTAMP
        fi

        log_success "数据库备份完成: $DB_BACKUP_FILE"
    else
        log_warn "数据库文件不存在，跳过数据库备份"
    fi
}

# 备份诊断结果
backup_results() {
    log_info "开始备份诊断结果..."

    if [ -d ./results ]; then
        RESULTS_BACKUP_FILE="$BACKUP_DIR/results/results.$TIMESTAMP.tar.gz"
        tar -czf $RESULTS_BACKUP_FILE ./results 2>/dev/null || true
        log_success "诊断结果备份完成: $RESULTS_BACKUP_FILE"
    else
        log_warn "诊断结果目录不存在，跳过备份"
    fi
}

# 备份报告
backup_reports() {
    log_info "开始备份报告..."

    if [ -d ./reports ]; then
        REPORTS_BACKUP_FILE="$BACKUP_DIR/reports/reports.$TIMESTAMP.tar.gz"
        tar -czf $REPORTS_BACKUP_FILE ./reports 2>/dev/null || true
        log_success "报告备份完成: $REPORTS_BACKUP_FILE"
    else
        log_warn "报告目录不存在，跳过备份"
    fi
}

# 备份上传文件
backup_uploads() {
    log_info "开始备份上传文件..."

    if [ -d ./uploaded_img ]; then
        UPLOADS_BACKUP_FILE="$BACKUP_DIR/uploads/uploads.$TIMESTAMP.tar.gz"
        tar -czf $UPLOADS_BACKUP_FILE ./uploaded_img 2>/dev/null || true
        log_success "上传文件备份完成: $UPLOADS_BACKUP_FILE"
    else
        log_warn "上传文件目录不存在，跳过备份"
    fi
}

# 备份日志
backup_logs() {
    log_info "开始备份日志..."

    if [ -d ./logs ]; then
        LOGS_BACKUP_FILE="$BACKUP_DIR/logs/logs.$TIMESTAMP.tar.gz"
        tar -czf $LOGS_BACKUP_FILE ./logs 2>/dev/null || true
        log_success "日志备份完成: $LOGS_BACKUP_FILE"
    else
        log_warn "日志目录不存在，跳过备份"
    fi
}

# 清理过期备份
cleanup_old_backups() {
    log_info "清理过期的备份文件（保留最近 $RETENTION_DAYS 天）..."

    find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    find $BACKUP_DIR -type d -empty -delete 2>/dev/null || true

    log_success "过期备份清理完成"
}

# 创建备份清单
create_backup_manifest() {
    MANIFEST_FILE="$BACKUP_DIR/backup_manifest.$TIMESTAMP.txt"

    cat > $MANIFEST_FILE << EOF
阿尔兹海默症诊断系统 - 备份清单
===============================
备份时间: $(date)
服务器: $HOSTNAME
备份目录: $BACKUP_DIR

备份文件列表:
EOF

    find $BACKUP_DIR -type f -name "*.$TIMESTAMP*" | while read file; do
        size=$(du -h "$file" | cut -f1)
        echo "$file ($size)" >> $MANIFEST_FILE
    done

    log_info "备份清单已创建: $MANIFEST_FILE"
}

# 上传到远程存储（可选）
upload_to_remote() {
    log_info "检查远程备份配置..."

    if [ -n "$REMOTE_BACKUP_URL" ]; then
        log_info "上传备份到远程存储..."

        case "$REMOTE_BACKUP_URL" in
            s3://*)
                if command -v aws &> /dev/null; then
                    aws s3 sync $BACKUP_DIR $REMOTE_BACKUP_URL
                    log_success "备份已上传到S3"
                else
                    log_warn "AWS CLI未安装，跳过远程上传"
                fi
                ;;
            scp://*)
                log_warn "SCP远程备份暂未实现"
                ;;
            *)
                log_warn "不支持的远程存储类型"
                ;;
        esac
    else
        log_info "未配置远程备份，跳过上传"
    fi
}

# 显示备份状态
show_backup_status() {
    echo ""
    echo "=================================="
    echo "备份状态报告"
    echo "=================================="
    echo ""

    if [ -d $BACKUP_DIR ]; then
        echo "备份目录: $BACKUP_DIR"
        echo ""
        echo "数据库备份:"
        ls -lh $BACKUP_DIR/database/ 2>/dev/null | tail -n +2 || echo "  无"
        echo ""
        echo "结果备份:"
        ls -lh $BACKUP_DIR/results/ 2>/dev/null | tail -n +2 || echo "  无"
        echo ""
        echo "报告备份:"
        ls -lh $BACKUP_DIR/reports/ 2>/dev/null | tail -n +2 || echo "  无"
        echo ""
        echo "上传文件备份:"
        ls -lh $BACKUP_DIR/uploads/ 2>/dev/null | tail -n +2 || echo "  无"
        echo ""
        echo "日志备份:"
        ls -lh $BACKUP_DIR/logs/ 2>/dev/null | tail -n +2 || echo "  无"
        echo ""

        total_size=$(du -sh $BACKUP_DIR 2>/dev/null | cut -f1)
        echo "总备份大小: $total_size"
    else
        echo "备份目录不存在"
    fi

    echo ""
    echo "=================================="
}

# 显示帮助
show_help() {
    echo "阿尔兹海默症诊断系统 - 数据备份脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help              显示帮助信息"
    echo "  -s, --status            显示备份状态"
    echo "  --cleanup               清理过期备份"
    echo "  --upload                上传到远程存储"
    echo "  --retention DAYS        设置备份保留天数（默认: 30）"
    echo ""
    echo "环境变量:"
    echo "  BACKUP_DIR              备份目录（默认: ./backups）"
    echo "  BACKUP_RETENTION_DAYS   备份保留天数（默认: 30）"
    echo "  REMOTE_BACKUP_URL       远程备份URL（可选）"
    echo ""
    echo "示例:"
    echo "  $0                      # 执行完整备份"
    echo "  $0 --status             # 显示备份状态"
    echo "  $0 --cleanup            # 清理过期备份"
    echo "  $0 --retention 7        # 设置保留7天"
}

# 主函数
main() {
    local do_cleanup=false
    local do_upload=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -s|--status)
                show_backup_status
                exit 0
                ;;
            --cleanup)
                do_cleanup=true
                shift
                ;;
            --upload)
                do_upload=true
                shift
                ;;
            --retention)
                RETENTION_DAYS="$2"
                shift 2
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done

    log_info "=================================="
    log_info "阿尔兹海默症诊断系统 - 数据备份"
    log_info "=================================="
    echo ""

    create_backup_dirs
    backup_database
    backup_results
    backup_reports
    backup_uploads
    backup_logs
    create_backup_manifest

    if [ "$do_cleanup" = true ]; then
        cleanup_old_backups
    fi

    if [ "$do_upload" = true ]; then
        upload_to_remote
    fi

    echo ""
    log_success "备份任务完成!"
    echo ""

    show_backup_status
}

main "$@"