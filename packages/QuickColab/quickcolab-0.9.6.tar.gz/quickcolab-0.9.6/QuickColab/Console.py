import subprocess
import shlex,json,os,sys
from typing import Callable, Any
class Console:
    """A class that provides various console-related utility methods."""
    #@staticmethod
    #def run_command(cmd):
        #process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output, error = process.communicate()
        #if process.returncode != 0:
            #raise subprocess.CalledProcessError(process.returncode, cmd, output, error)
        #return output.decode('utf-8')
    @staticmethod
    def pipinstall(*args) -> Callable[[], str]:
        # 保存已安装库的路径
        progress_file = 'pip_install_progress.json'
        
        # 尝试读取已安装库的状态
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                installed_packages = json.load(f)
        else:
            installed_packages = []

        def inner_run_command(b):
            for package in args:
                # 如果包已经安装过，则跳过
                if package in installed_packages:
                    print(f"'{package}' 已安装，跳过。")
                    continue

                # 安装包
                print(f"正在安装 '{package}'...")
                os.system("pip install " + str(package))
                installed_packages.append(package)

                # 保存当前进度
                with open(progress_file, 'w') as f:

                    print(f"安装 '{package}'完成")
                    json.dump(installed_packages, f)

        return inner_run_command
   
    @staticmethod
    def aptinstall(*args) -> Callable[[], str]:
        # 保存已安装库的路径
        progress_file = 'apt_install_progress.json'
        
        # 尝试读取已安装库的状态
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                installed_packages = json.load(f)
        else:
            installed_packages = []

        def inner_run_command(b):
            for package in args:
                # 如果包已经安装过，则跳过
                if package in installed_packages:
                    print(f"'{package}' 已安装，跳过。")
                    continue

                # 安装
                print(f"正在安装 '{package}'...")
                os.system("apt install " + str(package)+" -y")
                installed_packages.append(package)

                # 保存当前进度
                with open(progress_file, 'w') as f:
                    print(f"安装 '{package}'完成")
                    json.dump(installed_packages, f)

        return inner_run_command
    
    @staticmethod
    def print(text: str) -> Callable[[Any], None]:
        """
        Returns a function that prints the given text.

        Args:
            text (str): The text to be printed.

        Returns:
            Callable[[Any], None]: A function that prints the text.
        """
        def inner_print(b):
            print(text)
        return inner_print

# Example of usage:
# command_function = QuickColabConsole.run_command("ls -l")
# output = command_function()  # This will execute the command and return the output
# print(output)

    @staticmethod
    def update_apt() -> Callable[[], None]:
        """
        Returns a function that updates the apt package lists.

        Returns:
            Callable[[], None]: A function that updates apt package lists.
        """
        def update():
            try:
                subprocess.check_call(['sudo', 'apt-get', 'update'])
                print("Successfully updated apt package lists")
            except subprocess.CalledProcessError as e:
                print("Error updating apt package lists")
                print(f"Error message: {e}")
        return update

    @staticmethod
    def ls(path: str = '.', options: str = '-al') -> Callable[[Any], str]:
        """
        Returns a function that lists directory contents.

        Args:
            path (str): The path to list. Defaults to current directory.
            options (str): The options for the ls command. Defaults to '-al'.

        Returns:
            Callable[[Any], str]: A function that executes the ls command.
        """
        def inner_ls(b):
            return Console.run_command(f"ls {options} {shlex.quote(path)}")
        return inner_ls

    @staticmethod
    def rm(path: str, recursive: bool = False, force: bool = False) -> Callable[[], str]:
        """
        Returns a function that removes files or directories.

        Args:
            path (str): The path to remove.
            recursive (bool): Whether to remove directories and their contents recursively.
            force (bool): Whether to ignore nonexistent files and never prompt.

        Returns:
            Callable[[], str]: A function that executes the rm command.
        """
        options = '-r ' if recursive else ''
        options += '-f ' if force else ''
        def inner_rm(b):
            return Console.run_command(f"rm {options}{shlex.quote(path)}")
        return inner_rm

    @staticmethod
    def cp(source: str, destination: str, recursive: bool = False) -> Callable[[Any], str]:
        """
        Returns a function that copies files or directories.

        Args:
            source (str): The source path.
            destination (str): The destination path.
            recursive (bool): Whether to copy directories recursively.

        Returns:
            Callable[[Any], str]: A function that executes the cp command.
        """
        options = '-r' if recursive else ''
        def inner_cp():
            return Console.run_command(f"cp {options} {shlex.quote(source)} {shlex.quote(destination)}")
        return inner_cp

    @staticmethod
    def mv(source: str, destination: str) -> Callable[[Any], str]:
        """
        Returns a function that moves files or directories.

        Args:
            source (str): The source path.
            destination (str): The destination path.

        Returns:
            Callable[[Any], str]: A function that executes the mv command.
        """
        def inner_mv(b):
            return Console.run_command(f"mv {shlex.quote(source)} {shlex.quote(destination)}")
        return inner_mv

    @staticmethod
    def mkdir(destination: str) -> Callable[[Any], str]:
        """
        Returns a function that moves files or directories.

        Args:
            source (str): The source path.
            destination (str): The destination path.

        Returns:
            Callable[[Any], str]: A function that executes the mv command.
        """
        def inner_mkdir(b):
            return Console.run_command(f"mv -p {shlex.quote(destination)}")
        return inner_mkdir
    @staticmethod    
    def run_command(*arg) -> Callable[[], str]:
        
        def inner_run_command(b):
            for i in arg:
                print("start!")
                os.system(str(i))

                print("finish!")

        return inner_run_command

    