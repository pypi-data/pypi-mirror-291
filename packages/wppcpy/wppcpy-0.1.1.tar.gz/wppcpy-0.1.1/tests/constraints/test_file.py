import os
import unittest
from wppcpy.constraints import FileConstraint, Readme, MainFile, UninstallPHP, InstallPHP

class TestFileConstraints(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_plugin'
        os.makedirs(self.test_dir, exist_ok=True)

        self.readme_path = os.path.join(self.test_dir, 'readme.txt')
        with open(self.readme_path, 'w') as f:
            f.write('Test Readme')

        self.main_file_path = os.path.join(self.test_dir, 'test_plugin.php')
        with open(self.main_file_path, 'w') as f:
            f.write('Test Main File')

        self.uninstall_path = os.path.join(self.test_dir, 'uninstall.php')
        with open(self.uninstall_path, 'w') as f:
            f.write('Test Uninstall File')

        self.install_path = os.path.join(self.test_dir, 'install.php')
        with open(self.install_path, 'w') as f:
            f.write('Test Install File')

    def tearDown(self):
        for file in [self.readme_path, self.main_file_path, self.uninstall_path, self.install_path]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.test_dir)

    def test_readme_validation(self):
        readme_constraint = Readme(self.test_dir)
        self.assertTrue(readme_constraint.validate())

    def test_main_file_validation(self):
        main_file_constraint = MainFile(self.test_dir)
        self.assertTrue(main_file_constraint.validate())

    def test_uninstall_php_validation(self):
        uninstall_constraint = UninstallPHP(self.test_dir)
        self.assertTrue(uninstall_constraint.validate())

    def test_install_php_validation(self):
        install_constraint = InstallPHP(self.test_dir)
        self.assertTrue(install_constraint.validate())

    def test_main_file_with_custom_files(self):
        custom_main_file = MainFile(self.test_dir, files=['custom_file.php', 'another_file.php'])
        for file_name in ['custom_file.php', 'another_file.php']:
            path = os.path.join(self.test_dir, file_name)
            with open(path, 'w') as f:
                f.write('Custom File Content')

        self.assertTrue(custom_main_file.validate())

        for file_name in ['custom_file.php', 'another_file.php']:
            os.remove(os.path.join(self.test_dir, file_name))
