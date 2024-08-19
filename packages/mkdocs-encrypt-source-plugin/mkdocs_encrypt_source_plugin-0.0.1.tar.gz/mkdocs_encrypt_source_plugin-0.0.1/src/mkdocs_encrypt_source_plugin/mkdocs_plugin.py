import os
# pip dependency
from cryptography.fernet import Fernet
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.exceptions import PluginError
from mkdocs.config.config_options import Type
from mkdocs.config.base import Config
# local
from . import decrypt_markdown, KEY_ENVIRONMENT_VARIABLE


SKIP_FLAG = "encrypt-source-plugin-skip-file"

class PlaceholderPluginConfig(Config):
    """
    The plugin config, that will be parsed from the settings supplied in `mkdocs.yaml`
    """
    # The environment variable containing the encryption key
    key_environment_variable = Type(str, default=KEY_ENVIRONMENT_VARIABLE)
    # Enable this to see how many encrypted blobs were found on each site
    verbose = Type(bool, default=False)


class EncryptPlugin(BasePlugin[PlaceholderPluginConfig]):
    def on_config(self, config: MkDocsConfig, **kwargs) -> MkDocsConfig:
        """
        Called once when the config is loaded.
        It will make modify the config and initialize this plugin.
        """
        self.logger = get_plugin_logger(__name__)

        password = os.getenv(self.config.key_environment_variable)
        if not password:
            raise PluginError(f"[encrypt-source] The enviroment variable '{self.config.key_environment_variable}' containing the decryption key is not set or empty")

        try:
            self.fernet_cipher = Fernet(password.encode())
        except Exception as ex:
            raise PluginError(f"There seems to be an issue with the decryption key '{password}'. Are you sure it is correct? Exception: {ex}")

        return config

    def on_page_markdown(self, markdown, page, config, files):
        """
        The page_markdown event is called after the page's markdown is loaded from file and can be used to alter the Markdown source text. The metadata has been stripped off and is available as page.meta at this point.
        See: https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
        """

        markdown, counter_success, counter_error = decrypt_markdown(markdown, self.fernet_cipher, lambda message: self.logger.error(f"Failed to decrypt data on page {page.file.src_path}: {message}"))
        if self.config.verbose and counter_success + counter_error > 0:
            self.logger.info(f"Decrypted {counter_success}/{counter_success+counter_error} blobs on page {page.file.src_path}")

        return markdown
