"""
This script runs the RasaHost application using a development server.
"""

import os

current_dir = os.path.dirname(os.path.realpath(__file__))


def train():
    import rasa
    domain = os.path.join(current_dir, "sample2/domain.yml")
    config = os.path.join(current_dir, "sample2/config.yml")
    training_files = os.path.join(current_dir, "sample2/data")
    output_model = os.path.join(current_dir, "sample2/models/")
    rasa.train(domain, config, training_files, output_model)


def get_agent():
    from rasa.core.agent import Agent
    from rasa.core.utils import read_endpoint_config
    model_path = os.path.join(current_dir, "sample2/models/20230828-111342-metal-note.tar.gz")
    action_endpoint_conf = read_endpoint_config(os.path.join(current_dir, "sample2/endpoints.yml"),
                                                endpoint_type="action_endpoint")
    agent = Agent.load(model_path, action_endpoint=action_endpoint_conf)
    return agent


if __name__ == '__main__':
    from RasaHost import host
    from rasa_sdk.executor import ActionExecutor
    import rasa
    from rasa.core.agent import Agent
    from sample2 import actions

    executor = ActionExecutor()
    executor.register_package(actions)
    host.set_data_path(os.path.join(current_dir, "sample2"))
    # train()
    host.agent = get_agent()
    host.run()
