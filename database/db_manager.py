"""数据库管理模块"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_path: str = "documents.db"):
        """初始化数据库管理器"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库和表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建主表: documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,  -- 属性(收文/发文/档案/资料/销毁)
                creation_year TEXT,      -- 成文年度
                document_number TEXT,    -- 文号
                issuing_agency TEXT,     -- 发文机关
                title TEXT NOT NULL,     -- 标题
                document_date TEXT,      -- 成文日期
                registration_date TEXT,  -- 登记日期
                security_level TEXT NOT NULL,  -- 密级
                confidentiality_period TEXT,   -- 保密期限
                is_original TEXT,        -- 是否原件
                copies_count INTEGER,    -- 份数
                copy_number TEXT,        -- 份号
                page_count INTEGER,      -- 页数
                remarks TEXT,            -- 备注
                attachment_path TEXT,    -- 附件路径
                mark_color TEXT,         -- 标记颜色
                mark_content TEXT,       -- 标记内容
                mark_date TEXT,          -- 标记日期
                receive_category TEXT,   -- 收文类别
                receive_serial_number INTEGER,  -- 收文流水号
                receive_number TEXT,     -- 收文编号
                receive_source TEXT,     -- 接受来源
                handle_status TEXT,      -- 收文办理状态
                main_recipient TEXT,     -- 主送机关
                abstract TEXT,           -- 摘要
                draft_opinion TEXT,      -- 拟办意见
                leader_instruction TEXT, -- 领导批示
                distribution_record TEXT, -- 分发记录
                urge_record TEXT,        -- 催办记录
                handle_result TEXT,      -- 办理结果
                issue_code TEXT,         -- 发文机关代字
                cc_agency TEXT,          -- 抄送机关
                attachment_description TEXT, -- 附件说明
                drafter TEXT,            -- 拟稿人
                approver TEXT,           -- 签发人
                retention_period TEXT,   -- 保管期限
                archive_category TEXT,   -- 档案分类
                item_number TEXT,        -- 件号
                archive_number TEXT,     -- 档号
                material_category TEXT,  -- 资料分类
                material_number TEXT,    -- 资料编号
                destruction_batch TEXT,  -- 销毁批次
                destruction_number TEXT, -- 销毁编号
                destruction_copies INTEGER, -- 销毁份数
                destruction_copy_number TEXT, -- 销毁份号
                original_appraisal TEXT, -- 原件鉴定
                created_at TEXT DEFAULT CURRENT_TIMESTAMP, -- 创建时间
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP  -- 更新时间
            )
        ''')
        
        # 创建日记表: diary
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diary_date TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建操作日志表: operation_log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_time TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                document_id INTEGER,
                document_title TEXT,
                operation_detail TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建配置表: config
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_key TEXT UNIQUE NOT NULL,
                config_value TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询语句"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = self.dict_factory
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """执行更新语句(INSERT, UPDATE, DELETE)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_row_id = cursor.lastrowid
        conn.close()
        return last_row_id
    
    def dict_factory(self, cursor, row):
        """将查询结果转换为字典格式"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    def get_all_documents(self, category: Optional[str] = None, security_level: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取所有文档记录"""
        query = "SELECT * FROM documents WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if security_level:
            query += " AND security_level = ?"
            params.append(security_level)
        
        query += " ORDER BY created_at DESC"
        
        return self.execute_query(query, tuple(params))
    
    def add_document(self, document_data: Dict[str, Any]) -> int:
        """添加文档记录"""
        # 构建插入语句
        columns = []
        values = []
        placeholders = []
        
        for key, value in document_data.items():
            if hasattr(self, '_get_column_name') and self._is_valid_column(key):
                columns.append(key)
                values.append(value)
                placeholders.append('?')
        
        query = f"INSERT INTO documents ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        return self.execute_update(query, tuple(values))
    
    def _is_valid_column(self, column_name: str) -> bool:
        """检查列名是否有效"""
        valid_columns = [
            'category', 'creation_year', 'document_number', 'issuing_agency', 'title',
            'document_date', 'registration_date', 'security_level', 'confidentiality_period',
            'is_original', 'copies_count', 'copy_number', 'page_count', 'remarks',
            'attachment_path', 'mark_color', 'mark_content', 'mark_date',
            'receive_category', 'receive_serial_number', 'receive_number', 'receive_source',
            'handle_status', 'main_recipient', 'abstract', 'draft_opinion',
            'leader_instruction', 'distribution_record', 'urge_record', 'handle_result',
            'issue_code', 'cc_agency', 'attachment_description', 'drafter', 'approver',
            'retention_period', 'archive_category', 'item_number', 'archive_number',
            'material_category', 'material_number', 'destruction_batch', 'destruction_number',
            'destruction_copies', 'destruction_copy_number', 'original_appraisal'
        ]
        return column_name in valid_columns


# 单例模式的数据库管理器
db_manager = DatabaseManager()