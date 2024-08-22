# help_texts.py

nufictl_help = """nufictl is a command-line tool for managing CRD Npu Deployments.
Usage:
    nufictl ls
    nufictl create with sequential user input
    nufictl run --image=IMAGE [--cpu=CPU] [--memory=MEMORY] [--accelerator_type=TYPE] [--accelerator_count=COUNT]
    nufictl delete --name=NAME
    nufictl config set URL
    nufictl config ls
    nufictl config delete NAME_or_URL
    nufictl config set current-context NAME_or_URL
    nufictl config get current-context
    nufictl config reset
    nufictl streamer server [url]
    nufictl streamer get : show pipelines
    nufictl streamer set [pipeline_name] : set pipeline
    nufictl streamer test [pipeline_name] [video_path] : send video file to websocket and get result
"""

config_help = """
Manage configuration for NufiCTL.

Available actions:
    set: Set a new URL configuration.
    ls: List all configurations.
    delete: Delete a configuration by name or URL.
    set-current-context: Set the current context by name or URL.
    get-current-context: Get the current context.
    reset: Reset config.yaml to default settings.

Usage:
    nufictl config set URL
    nufictl config set NAME URL
    nufictl config ls
    nufictl config delete [NAME]
    nufictl config set-current-context [NAME] or [URL]
    nufictl config get-current-context
    nufictl config reset
"""

stream_help = """

Test the created nufi stream.

Usage:
    nufictl streamer server [url]
    nufictl streamer get : show pipelines
    nufictl streamer set [pipeline_name] : set pipeline
    nufictl streamer test [pipeline_name] [video_path] : send video file to websocket and get result
    
"""
