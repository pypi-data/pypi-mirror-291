import requests
import websockets
import asyncio
import base64
import yaml
import os
from PIL import Image
from pydantic import BaseModel
from nufictl.help_texts import stream_help
from io import BytesIO
from tabulate import tabulate
from tqdm import tqdm

CONFIG_FILE = "config.yaml"


class PipelineRequest(BaseModel):
    pipeline_id: str


class StreamerCommands:
    def __init__(self, stream_api_tester):
        self.stream_api_tester = stream_api_tester

    def help(self):
        """Show help message for streamer commands."""
        print(stream_help)

    def set_url(self, url):
        """Set the server URL."""
        if url:
            self.stream_api_tester.set_url(url)
        else:
            print("URL is required to set the server.")

    def get_url(self):
        """Get the server URL."""
        self.stream_api_tester.get_url()

    def get_pipelines(self):
        """Show pipelines."""
        self.stream_api_tester.get_pipelines()

    def select_pipeline(self, pipeline_name):
        """Set a specific pipeline."""
        if pipeline_name:
            self.stream_api_tester.select_pipeline(pipeline_name)
        else:
            print("Pipeline name is required to select a pipeline.")

    def test_stream(self):
        """Prompt the user for a video file path and send the video to the websocket."""
        video_path = (
            input("Enter the video path [/tmp/video/yoga.mp4]: ")
            or "/tmp/video/yoga.mp4"
        )
        self.stream_api_tester.test_stream(video_path)


class StreamApiTester:
    def __init__(self):
        self.config_data = self.load_config()  # Load the entire config
        self.server_config = self.config_data.get("server", {})
        self.server_url = self.server_config.get("server_url", "http://localhost:8000")
        self.pipeline_name = self.server_config.get("pipeline_name", None)
        self.websocket_url = self.server_config.get("websocket_url", None)

    def save_config(self):
        self.config_data["server"] = self.server_config
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(self.config_data, f)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            print(f"{CONFIG_FILE} not found. Creating a new one with default settings.")
            default_config = {
                "config": {
                    "current_context": "default",
                    "default": "http://localhost/api/deployments",
                },
                "server": {
                    "pipeline_name": None,
                    "server_url": "http://localhost:8000",
                    "websocket_url": None,
                },
            }
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
        else:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)

    def save_config(self):
        all_data = self.load_config()
        all_data["server"] = self.server_config
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(all_data, f)

    def set_url(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"

        self.server_url = url
        self.server_config["server_url"] = self.server_url
        self.save_config()
        print(f"Server URL set to: {url}")

    def get_url(self):
        print(f"Current streamer server URL: {self.server_url}")

    def send_video(self, video_path):
        """Send a video file to the server with progress bar."""
        try:
            file_size = os.path.getsize(video_path)
            with open(video_path, "rb") as f, tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Uploading"
            ) as pbar:
                response = requests.post(
                    f"{self.stream_api_tester.server_url}/upload_video",
                    files={"file": f},
                    headers={"Content-Type": "multipart/form-data"},
                    stream=True,
                )

                pbar.update(file_size)

            if response.status_code == 200:
                print("Video file uploaded successfully.")
            else:
                print(
                    f"Failed to upload video file. Server responded with status code {response.status_code}."
                )

        except Exception as e:
            print(f"An error occurred while uploading the video file: {str(e)}")

    def get_pipelines(self):
        try:
            response = requests.get(f"{self.server_url}/pipelines")
            response.raise_for_status()
            pipelines = response.json()

            table_data = []
            for pipeline_name, pipeline_command in pipelines.items():
                steps = pipeline_command.split("!")
                parsed_steps = [step.strip().split(" ")[0] for step in steps]

                table_data.append([pipeline_name, parsed_steps[0]])

                for step in parsed_steps[1:]:
                    table_data.append(["", step])

                table_data.append(["", ""])

            headers = ["Pipeline Name", "Pipeline Steps"]
            table = tabulate(table_data, headers, tablefmt="pretty")

            lines = table.split("\n")
            final_lines = []
            for i, line in enumerate(lines):
                if (
                    i > 2
                    and lines[i].startswith("| ")
                    and not lines[i].startswith("|                      ")
                ):
                    final_lines.append(
                        "+----------------------+---------------------------------------+"
                    )
                final_lines.append(line)

            table_with_borders = "\n".join(final_lines)
            print(table_with_borders)

        except requests.RequestException as e:
            print(f"Failed to get pipelines. Error: {str(e)}")

    def select_pipeline(self, pipeline_name):
        try:
            response = requests.post(
                f"{self.server_url}/pipelines/select",
                json={"pipeline_id": pipeline_name},
            )
            response.raise_for_status()
            result = response.json()

            clean_server_url = self.server_url.replace("http://", "").replace(
                "https://", ""
            )
            websocket_url = f"ws://{clean_server_url}/ws"

            self.server_config["pipeline_name"] = pipeline_name
            self.server_config["websocket_url"] = websocket_url
            self.save_config()

            print(f"Pipeline selected: {result['message']}")
            print(f"WebSocket URL set to: {websocket_url}")
        except requests.RequestException as e:
            print(f"Failed to select pipeline. Error: {str(e)}")

    async def send_video(self, websocket_url, video_path):
        output_dir = "output_frames"
        os.makedirs(output_dir, exist_ok=True)

        async with websockets.connect(websocket_url) as websocket:
            cap = Image.open(video_path)
            frame_number = 0
            total_frames = cap.n_frames

            with tqdm(total=total_frames, desc="Streaming Video", unit="frame") as pbar:
                while True:
                    try:
                        cap.seek(frame_number)
                        frame = cap.convert("RGB")
                        buffer = BytesIO()
                        frame.save(buffer, format="JPEG")
                        frame_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
                        await websocket.send(frame_data)
                        response = await websocket.recv()

                        # Save the frame in the specified directory
                        output_path = os.path.join(
                            output_dir, f"output_{frame_number}.jpg"
                        )
                        with open(output_path, "wb") as f:
                            f.write(base64.b64decode(response))

                        frame_number += 1
                        pbar.update(1)

                    except EOFError:
                        break

    def test_stream(self, video_path):
        if not self.pipeline_name or not self.websocket_url:
            print(
                "Pipeline name or Websocket URL is not set. Please select a pipeline first."
            )
            return

        try:
            print(
                f"Video streaming to {self.pipeline_name} {self.websocket_url} started."
            )
            asyncio.run(self.send_video(self.websocket_url, video_path))
            print("Video streaming completed.")
        except Exception as e:
            print(f"An error occurred during video streaming: {e}")
