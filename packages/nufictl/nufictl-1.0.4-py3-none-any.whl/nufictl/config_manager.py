import yaml
import os
from tabulate import tabulate
from nufictl.utils import generate_random_name
from nufictl.help_texts import config_help

CONFIG_FILE = "config.yaml"


class ConfigCommands:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def help(self):
        """Show help message for config commands"""
        print(config_help)

    def ls(self):
        """List all configurations"""
        self.config_manager.ls()

    def set(self, name, url):
        """Set a configuration"""
        self.config_manager.set(name, url)

    def delete(self, name):
        """Delete a configuration"""
        self.config_manager.delete(name)

    def set_current_context(self, name=None, url=None):
        """Set the current context"""
        self.config_manager.set_current_context(name, url)

    def get_current_context(self):
        """Get the current context"""
        self.config_manager.get_current_context()

    def reset(self):
        """Reset the configuration"""


class ConfigManager:
    def __init__(self):
        self.config_data = self.load_config().get("config", {})
        self.default_url = self.config_data.get("default")
        if self.default_url is None:
            raise ValueError("default_url is not set in config.yaml")
        self.current_context = self.config_data.get("current_context", "default")
        if "default" not in self.config_data:
            self.config_data["default"] = ""
        self.save_config()

    def save_config(self):
        all_data = self.load_config()
        all_data["config"] = self.config_data
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(all_data, f)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            default_config = {"config": {"default": "", "current_context": "default"}}
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
        else:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)

    def set(self, name=None, url=None):
        print(f"set config with {name} and {url}")
        if not url:
            print("URL is required for setting configuration.")
            return
        if not name and url:
            name = generate_random_name()
            self.config_data[name] = url
        if name in self.config_data and not url:
            self.config_data[name] = url
        if name and url:
            self.config_data[name] = url
        self.save_config()
        print(f"URL {url} has been set with name {name}.")

    def ls(self):
        headers = ["Context", "Config Name", "URL"]
        table = [
            [
                "*" if self.current_context == "default" else "",
                "default",
                self.default_url,
            ]
        ]
        for name, url in self.config_data.items():
            if name in ["current_context", "default", "default"]:
                continue
            table.append(["*" if name == self.current_context else "", name, url])
        print(tabulate(table, headers, tablefmt="pretty"))

    def delete(self, name=None):
        # prevent not delete default config or current_context
        if name == "default":
            print(f"Cannot delete default context")
            return
        if name in self.config_data:
            # if target config is current_context, change current context to default
            if name == self.current_context:
                self.current_context = "default"
            del self.config_data[name]
            self.save_config()
            print(f"Configuration {name} has been deleted.")
        else:
            print("Configuration name must exist.")

    def set_current_context(self, name=None, url=None):
        if name in self.config_data.keys():
            self.current_context = name
            self.save_config()
            print(f"Current context set to {name}")
        elif url in self.config_data.values():
            name = [key for key, value in self.config_data.items() if value == url][0]
            self.current_context = name
            self.save_config()
            print(f"Current context set to {name}")
        else:
            print("Configuration name or URL must exist.")

    def get_current_context(self):
        context_url = self.config_data.get(self.current_context, self.default_url)
        print(f"Current context: {self.current_context} ({context_url})")

    def reset(self):
        confirmation = input("Are you sure you want to reset config.yaml? ([y]/n): ")
        if confirmation.lower() in ["", "y", "yes"]:
            default_config = {"default": "", "current_context": "default"}
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            self.config_data = default_config
            self.current_context = "default"
            self.save_config()
            print("config.yaml has been reset to default settings.")
        else:
            print("Reset cancelled.")
