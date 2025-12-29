"""主程序入口"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QToolBar, QStatusBar, QMessageBox, QInputDialog, QLineEdit, QPushButton, QLabel, QFrame, QDialog
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QFont, QIcon

from config.config import config_manager
from database.db_manager import db_manager


class LoginWindow(QDialog):
    """登录窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("登录 - 公文和档案管理系统")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("公文和档案管理系统")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("请输入密码")
        layout.addWidget(self.password_input)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.login)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 回车键登录
        self.password_input.returnPressed.connect(self.login)
    
    def login(self):
        """登录验证"""
        password = self.password_input.text()
        
        if password == config_manager.get("default_password") or password == config_manager.get("super_password"):
            self.accept_login()
        else:
            QMessageBox.warning(self, "错误", "密码错误，请重试！")
            self.password_input.clear()
    
    def accept_login(self):
        """接受登录"""
        self.accept()


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.config = config_manager
        self.db = db_manager
        self.login_accepted = False
        self.init_ui()
    
    def init_ui(self):
        """初始化主界面"""
        # 设置窗口标题
        self.setWindowTitle(self.config.get("app_title", "公文和档案管理系统"))
        
        # 设置窗口大小
        width = self.config.get("window_width", 1200)
        height = self.config.get("window_height", 800)
        self.resize(width, height)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 添加标签页
        tab_names = [
            "全部文书", "收文(全部)", "收文(在办)", "收文(办结)", 
            "发文", "档案", "资料", "销毁", "日记", "数据统计"
        ]
        
        for name in tab_names:
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.addWidget(QLabel(f"标签页: {name}"))
            self.tab_widget.addTab(tab, name)
        
        main_layout.addWidget(self.tab_widget)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
        
        # 显示窗口
        self.show()
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = self.addToolBar("工具栏")
        toolbar.setMovable(False)
        
        # 新增收文按钮
        add_receive_action = QAction("新增收文▼", self)
        add_receive_action.triggered.connect(self.add_receive_document)
        toolbar.addAction(add_receive_action)
        
        # 新增发文按钮
        add_issue_action = QAction("新增发文▼", self)
        add_issue_action.triggered.connect(self.add_issue_document)
        toolbar.addAction(add_issue_action)
        
        # 新增档案按钮
        add_archive_action = QAction("新增档案▼", self)
        add_archive_action.triggered.connect(self.add_archive_document)
        toolbar.addAction(add_archive_action)
        
        # 新增资料按钮
        add_material_action = QAction("新增资料▼", self)
        add_material_action.triggered.connect(self.add_material_document)
        toolbar.addAction(add_material_action)
        
        # 新增销毁按钮
        add_destruction_action = QAction("新增销毁▼", self)
        add_destruction_action.triggered.connect(self.add_destruction_document)
        toolbar.addAction(add_destruction_action)
        
        # 新增日记按钮
        add_diary_action = QAction("新增日记▼", self)
        add_diary_action.triggered.connect(self.add_diary_entry)
        toolbar.addAction(add_diary_action)
        
        # 批量编辑按钮
        batch_edit_action = QAction("批量编辑▼", self)
        batch_edit_action.triggered.connect(self.batch_edit)
        toolbar.addAction(batch_edit_action)
        
        # 打印稿纸按钮
        print_template_action = QAction("打印稿纸▼", self)
        print_template_action.triggered.connect(self.print_template)
        toolbar.addAction(print_template_action)
        
        # 添加分隔符
        toolbar.addSeparator()
        
        # 清空按钮
        clear_action = QAction("清空", self)
        clear_action.triggered.connect(self.clear_search)
        toolbar.addAction(clear_action)
        
        # 查询框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入查询关键词")
        self.search_input.setMaximumWidth(200)
        toolbar.addWidget(self.search_input)
        
        # 查询按钮
        search_action = QAction("查询", self)
        search_action.triggered.connect(self.search_documents)
        toolbar.addAction(search_action)
        
        # 高级查询按钮
        advanced_search_action = QAction("高级查询▼", self)
        advanced_search_action.triggered.connect(self.advanced_search)
        toolbar.addAction(advanced_search_action)
        
        # 表格导出按钮
        export_action = QAction("表格导出▼", self)
        export_action.triggered.connect(self.export_documents)
        toolbar.addAction(export_action)
        
        # 添加分隔符
        toolbar.addSeparator()
        
        # 字体缩小按钮
        font_smaller_action = QAction("字体-", self)
        font_smaller_action.triggered.connect(self.font_smaller)
        toolbar.addAction(font_smaller_action)
        
        # 字体放大按钮
        font_larger_action = QAction("字体+", self)
        font_larger_action.triggered.connect(self.font_larger)
        toolbar.addAction(font_larger_action)
        
        # 设置按钮
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    # 工具栏功能方法
    def add_receive_document(self):
        """新增收文"""
        QMessageBox.information(self, "提示", "新增收文功能")
    
    def add_issue_document(self):
        """新增发文"""
        QMessageBox.information(self, "提示", "新增发文功能")
    
    def add_archive_document(self):
        """新增档案"""
        QMessageBox.information(self, "提示", "新增档案功能")
    
    def add_material_document(self):
        """新增资料"""
        QMessageBox.information(self, "提示", "新增资料功能")
    
    def add_destruction_document(self):
        """新增销毁"""
        QMessageBox.information(self, "提示", "新增销毁功能")
    
    def add_diary_entry(self):
        """新增日记"""
        QMessageBox.information(self, "提示", "新增日记功能")
    
    def batch_edit(self):
        """批量编辑"""
        QMessageBox.information(self, "提示", "批量编辑功能")
    
    def print_template(self):
        """打印稿纸"""
        QMessageBox.information(self, "提示", "打印稿纸功能")
    
    def search_documents(self):
        """查询文档"""
        keyword = self.search_input.text()
        QMessageBox.information(self, "提示", f"查询文档功能: {keyword}")
    
    def advanced_search(self):
        """高级查询"""
        QMessageBox.information(self, "提示", "高级查询功能")
    
    def export_documents(self):
        """导出文档"""
        QMessageBox.information(self, "提示", "导出文档功能")
    
    def clear_search(self):
        """清空查询"""
        self.search_input.clear()
    
    def font_smaller(self):
        """字体缩小"""
        current_font = self.font()
        current_size = current_font.pointSize()
        if current_size > 6:
            current_font.setPointSize(current_size - 1)
            self.setFont(current_font)
            self.config.set("font_size", current_size - 1)
    
    def font_larger(self):
        """字体放大"""
        current_font = self.font()
        current_size = current_font.pointSize()
        if current_size < 30:
            current_font.setPointSize(current_size + 1)
            self.setFont(current_font)
            self.config.set("font_size", current_size + 1)
    
    def show_settings(self):
        """显示设置"""
        QMessageBox.information(self, "提示", "显示设置功能")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建登录窗口
    login_window = LoginWindow()
    
    # 显示登录窗口并等待登录
    if login_window.exec() == QDialog.Accepted:
        # 登录成功，显示主窗口
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    else:
        # 登录失败或取消，退出程序
        sys.exit(1)


if __name__ == "__main__":
    main()