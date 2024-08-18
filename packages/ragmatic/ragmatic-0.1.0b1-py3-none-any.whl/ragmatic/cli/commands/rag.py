import click
from logging import getLogger

from ragmatic.cli.configuration.tools import (
    load_config,
    merge_defaults,
    MasterConfig,
    get_action_config_factory,
    ActionConfigFactory
)
from ragmatic.actions.rag import RagActionConfig, RagAction
from ..configuration._types import RagAgentComponentConfig
from ..configuration.presets.preset_factory import get_preset


logger = getLogger(__name__)


@click.command('rag-query')
@click.option('--query', type=str, required=True)
@click.option('--config', type=click.Path(exists=True))
@click.option('--preset', type=click.Choice(['local_docs', 'pycode']), default='local_docs')
@click.option('--var', '-v', type=str, multiple=True, help="Variables to override in the preset, in key=var format")
def rag_cmd(config: click.Path, query: str, preset: str, var: list):
    vars = dict(v.split('=') for v in var)
    preset_data = get_preset(preset)
    preset_config = preset_data.get_config(**vars)
    config: MasterConfig = load_config(config) if config else preset_config
    if config != preset_config:
        config = merge_defaults(config, preset_data, **vars)
    cmd_config = config.rag_query_command
    rag_agent_component_config: RagAgentComponentConfig =\
        config.components.rag_agents[cmd_config.rag_agent]
    rag_action_config = RagActionConfig(
        **dict(
            document_source=cmd_config.document_source,
            query=query,
            rag_agent=rag_agent_component_config.model_dump()
        )
    )
    config_factory: ActionConfigFactory = get_action_config_factory("rag", config)
    rag_action_config = config_factory.dereference_action_config(rag_action_config)

    print(RagAction(rag_action_config).execute())
