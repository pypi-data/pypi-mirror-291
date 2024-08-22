import fire
import requests
import json
import yaml
from nufictl import __version__
from nufictl.utils import generate_random_name
from tabulate import tabulate
from nufictl.model import DeployDetail
from nufictl.config_manager import ConfigManager, ConfigCommands
from nufictl.stream_tester import StreamApiTester, StreamerCommands
from nufictl.help_texts import nufictl_help


class NufiCtl:
    """Nufictl is a command-line tool for managing CRD Npu Deployments."""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = ConfigCommands(self.config_manager)
        self.streamer_tester = StreamApiTester()
        self.streamer = StreamerCommands(self.streamer_tester)
        self.base_url = self.config_manager.config_data.get(
            self.config_manager.current_context,
            self.config_manager.config_data["default"],
        )

    def version(self):
        """Show the current version of NufiCTL."""
        print(f"Current nufictl version: {__version__}")

    def help(self):
        """Show help message."""
        print(nufictl_help)

    def ls(self):
        """List all deployments"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])

            deploys = []
            for item in items:
                name = item["metadata"]["name"]
                namespace = item["metadata"]["namespace"]
                creation_timestamp = item["metadata"]["creationTimestamp"]
                replicas = item["spec"]["replicas"]
                image = item["spec"]["template"]["spec"]["containers"][0]["image"]
                cpu = item["spec"]["template"]["spec"]["containers"][0]["resources"][
                    "requests"
                ]["cpu"]
                memory = item["spec"]["template"]["spec"]["containers"][0]["resources"][
                    "requests"
                ]["memory"]
                resources = item["spec"]["template"]["spec"]["containers"][0][
                    "resources"
                ]["limits"]
                accelerator_type = next(
                    (key for key in resources if key not in ["cpu", "memory"]), "none"
                )
                accelerator_count = resources.get(accelerator_type, "1")
                endpoint = item["endpoint"]
                available_replicas = item["status"].get("availableReplicas", 0)

                deploy = DeployDetail(
                    name,
                    namespace,
                    image,
                    cpu,
                    memory,
                    creation_timestamp,
                    replicas,
                    accelerator_type,
                    accelerator_count,
                    available_replicas,
                    endpoint,
                )
                deploys.append(deploy)

            table = [
                [
                    deploy.name,
                    deploy.namespace,
                    deploy.replicas,
                    deploy.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    deploy.accelerator_type,
                    deploy.accelerator_count,
                    deploy.endpoint,
                ]
                for deploy in deploys
            ]
            headers = [
                "Name",
                "Namespace",
                "Replicas",
                "Created",
                "Accelerator Type",
                "Accelerator Count",
                "Endpoint URL",
            ]
            print(tabulate(table, headers, tablefmt="pretty"))
        except requests.RequestException as e:
            print(f"Failed to list deployments. Error: {str(e)}")

    def create(
        self,
        name=None,
        image=None,
        cpu=None,
        memory=None,
        replicas=None,
        accelerator_type=None,
        accelerator_count=None,
    ):
        """Create a new deployment interactively."""
        name = input(f"Name [npu-deploy-example]: ") or "npu-deploy-example"
        image = input(f"Image [nginx]: ") or "nginx"
        cpu = input(f"CPU [1]: ") or "1"
        memory = input(f"Memory [1]: ") or "1"
        replicas = input(f"Replicas [1]: ") or 1
        accelerator_type = (
            input(
                f"Accelerator Type [none| nvidia.com/gpu | skt.com/aix_v1 | beta.furiosa.ai/npu ]: "
            )
            or "skt.com/aix_v1"
        )
        accelerator_count = input(f"Accelerator Count [1]: ") or 1

        payload = {
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory": memory,
            "replicas": replicas,
        }
        if accelerator_type:
            payload["acceleratorType"] = accelerator_type
        if accelerator_count:
            payload["acceleratorCount"] = accelerator_count
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                self.base_url, headers=headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            response_data = response.json()
            if (
                "response" in response_data
                and response_data["response"].get("statusCode") == 409
            ):
                message = (
                    f"Failed to create deployment. Deployment {name} already exists."
                )
            else:
                name = payload.get("name", "Unknown")
                image = payload.get("image", "Unknown")
                message = f"Successfully created {name} with image: {image}"
        except requests.RequestException as e:
            message = f"Failed to create deployment. Error: {str(e)}"
        return message

    def run(
        self,
        image,
        cpu="1",
        memory="1",
        accelerator_type="npu",
        accelerator_count=1,
    ):
        """Run a new deployment with a random name"""
        name = f"npu-deploy-{image}-{generate_random_name()}"
        payload = {"name": name, "image": image, "cpu": cpu, "memory": memory}
        if accelerator_type:
            payload["acceleratorType"] = accelerator_type
        if accelerator_count:
            payload["acceleratorCount"] = accelerator_count

        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                self.base_url, headers=headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            name = payload.get("name", "Unknown")
            image = payload.get("image", "Unknown")
            message = f"Successfully created {name} with image: {image}"
        except requests.RequestException as e:
            message = f"Failed to create deployment. Error: {str(e)}"
        print(message)
        return message

    def delete(self, name):
        """Delete a deployment.
        Args:
            --name: Name of the deployment to delete.
        """
        params = {"name": name}
        try:
            response = requests.delete(self.base_url, params=params)
            response.raise_for_status()
            message = f"Successfully deleted {name}"
        except requests.RequestException as e:
            message = f"Failed to delete deployment. Error: {str(e)}"
        return message


def main():
    nufi_ctl = NufiCtl()
    fire.Fire(
        {
            "": nufi_ctl.help,
            "help": nufi_ctl.help,
            "config": nufi_ctl.config,
            "streamer": nufi_ctl.streamer,
            "ls": nufi_ctl.ls,
            "create": nufi_ctl.create,
            "run": nufi_ctl.run,
            "delete": nufi_ctl.delete,
            "version" : nufi_ctl.version
        }
    )


if __name__ == "__main__":
    main()
