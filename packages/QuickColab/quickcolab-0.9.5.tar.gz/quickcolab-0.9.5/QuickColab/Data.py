#from google.colab import drive
#from google.colab import userdata

class Colab:
    """
    提供 Google Colab 相關操作的工具類。

    這個類包含了一系列靜態方法，用於在 Google Colab 環境中進行常見操作，
    如掛載 Google Drive、讀寫 Colab Secrets 和環境變量等。

    Methods:
        mount_drive(): 掛載 Google Drive 到 Colab 環境。
        read_secret(secret_name: str) -> str | None: 讀取 Colab Secret。
        set_secret(secret_name: str, secret_value: str): 設置 Colab Secret。
        read_variable(variable_name: str) -> str | None: 讀取環境變量。
        set_variable(variable_name: str, variable_value: str): 設置環境變量。
    """

    @staticmethod
    def mount_drive():
        """
        將 Google Drive 掛載到 Colab 環境。

        This method mounts the user's Google Drive to the '/content/drive' path in the Colab environment,
        allowing access to files stored in Google Drive.
        """
        drive.mount('/content/drive')
    
    @staticmethod
    def read_secret(secret_name: str) -> str | None:
        """
        讀取指定的 Colab Secret。

        Args:
            secret_name (str): 要讀取的 Secret 名稱。

        Returns:
            str | None: Secret 的值，如果不存在或發生錯誤則返回 None。

        Raises:
            Exception: 如果在讀取過程中發生錯誤，會捕獲並打印錯誤信息。
        """
        try:
            return userdata.get(secret_name)
        except Exception as e:
            print(f"讀取 Secret '{secret_name}' 時發生錯誤: {str(e)}")
            return None

    @staticmethod
    def set_secret(secret_name: str, secret_value: str):
        """
        設置指定的 Colab Secret。

        Args:
            secret_name (str): 要設置的 Secret 名稱。
            secret_value (str): Secret 的值。

        Raises:
            Exception: 如果在設置過程中發生錯誤，會捕獲並打印錯誤信息。
        """
        try:
            userdata.set(secret_name, secret_value)
            print(f"Secret '{secret_name}' 已成功設置")
        except Exception as e:
            print(f"設置 Secret '{secret_name}' 時發生錯誤: {str(e)}")

    @staticmethod
    def read_variable(variable_name: str) -> str | None:
        """
        讀取指定的環境變量。

        Args:
            variable_name (str): 要讀取的環境變量名稱。

        Returns:
            str | None: 環境變量的值，如果不存在則返回 None。
        """
        return os.environ.get(variable_name)

    @staticmethod
    def set_variable(variable_name: str, variable_value: str):
        """
        設置指定的環境變量。

        Args:
            variable_name (str): 要設置的環境變量名稱。
            variable_value (str): 環境變量的值。

        Note:
            設置的環境變量只在當前 Colab 運行時有效，不會永久保存。
        """
        os.environ[variable_name] = str(variable_value)
        print(f"環境變量 '{variable_name}' 已成功設置")
