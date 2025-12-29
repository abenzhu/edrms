"""配置管理模块"""
import json
import os
from typing import Any, Dict


class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_file: str = "app_config.json"):
        """初始化配置管理器"""
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # 默认配置
        default_config = {
            "app_title": "XX单位收文档案管理系统",
            "full_org_code": "X001",  # 全宗号
            "default_password": "123",
            "super_password": "admin123",
            "font_size": 12,
            "data_path": "./data",
            "backup_path": "./backup",
            "template_path": "./templates",
            "export_path": "./export",
            "attachment_path": "./attachments",
            "default_open_path": "./attachments",
            "word_template_path": "./templates/word",
            "excel_template_path": "./templates/excel",
            "json_path": "./json",
            "backup_retain_count": 10,
            "auto_backup_on_startup": True,
            "auto_backup_on_exit": True,
            "window_width": 1200,
            "window_height": 800,
            "list_column_widths": {},
            "list_column_order": {},
            "visible_columns": {},
            "row_height": 30,
            "font_scale": 1.0
        }
        
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict[str, Any] = None):
        """保存配置"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        self.config[key] = value
        self.save_config()
    
    def update(self, updates: Dict[str, Any]):
        """批量更新配置"""
        self.config.update(updates)
        self.save_config()


# 单例模式的配置管理器
config_manager = ConfigManager()