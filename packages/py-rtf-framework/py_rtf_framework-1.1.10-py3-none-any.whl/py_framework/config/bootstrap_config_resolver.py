from .base_config_resolver import BaseConfigResolver


class BootstrapConfigResolver(BaseConfigResolver):
    """启动配置解析器"""
    base_dir: str

    def __init__(self, base_dir: str = './'):
        super().__init__('bootstrap')
        self.base_dir = base_dir if base_dir.endswith('/') else base_dir + '/'
        # 开始装载配置
        self.load_config()

    def load_config(self):
        self.load_config_from_yml(self.base_dir + 'bootstrap.yml')
