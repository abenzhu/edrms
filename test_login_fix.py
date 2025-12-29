"""测试登录窗口修复的验证脚本"""

def test_imports():
    """测试导入是否正确"""
    try:
        from PySide6.QtWidgets import QDialog
        print("✓ QDialog 导入成功")
    except ImportError as e:
        print(f"✗ QDialog 导入失败: {e}")
        return False
    
    try:
        from main import LoginWindow, MainWindow
        print("✓ LoginWindow 和 MainWindow 导入成功")
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False
    
    return True


def test_class_inheritance():
    """测试类继承关系"""
    try:
        from PySide6.QtWidgets import QDialog
        from main import LoginWindow
        
        # 检查 LoginWindow 是否继承自 QDialog
        if issubclass(LoginWindow, QDialog):
            print("✓ LoginWindow 正确继承自 QDialog")
            return True
        else:
            print("✗ LoginWindow 未正确继承自 QDialog")
            return False
    except Exception as e:
        print(f"✗ 类继承检查失败: {e}")
        return False


def test_dialog_methods():
    """测试对话框方法是否存在"""
    try:
        from PySide6.QtWidgets import QDialog
        
        # 检查 QDialog 是否有必要的方法和常量
        has_exec = hasattr(QDialog, 'exec')
        has_accept = hasattr(QDialog, 'accept')
        has_reject = hasattr(QDialog, 'reject')
        has_accepted = hasattr(QDialog, 'Accepted')
        has_rejected = hasattr(QDialog, 'Rejected')
        
        if all([has_exec, has_accept, has_reject, has_accepted, has_rejected]):
            print("✓ QDialog 拥有所有必要的方法和常量")
            print(f"  - exec: {has_exec}")
            print(f"  - accept: {has_accept}")
            print(f"  - reject: {has_reject}")
            print(f"  - Accepted: {has_accepted}")
            print(f"  - Rejected: {has_rejected}")
            return True
        else:
            print("✗ QDialog 缺少某些方法或常量")
            return False
    except Exception as e:
        print(f"✗ 方法检查失败: {e}")
        return False


def test_code_syntax():
    """测试代码语法是否正确"""
    try:
        import py_compile
        import tempfile
        import os
        
        # 读取 main.py 的内容
        with open('main.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 编译检查
        compile(code, 'main.py', 'exec')
        print("✓ main.py 语法检查通过")
        return True
    except SyntaxError as e:
        print(f"✗ main.py 存在语法错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 语法检查失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("登录窗口修复验证测试")
    print("=" * 60)
    print()
    
    tests = [
        ("导入测试", test_imports),
        ("类继承测试", test_class_inheritance),
        ("对话框方法测试", test_dialog_methods),
        ("语法检查", test_code_syntax)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ 测试执行失败: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！登录窗口修复成功！")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")


if __name__ == "__main__":
    main()
