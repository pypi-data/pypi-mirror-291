import os
import pandas as pd

from ..template.community_report import COMMUNITY_REPORT_PROMPT
from ..llm.send import ChatLLM, ModelArgs
from . import df_ops
from ..utils.save import parquet_table_load, parquet_table_save


def create_final_community_reports(
    final_nodes_output: pd.DataFrame,
    final_relationship_output: pd.DataFrame,
    query_output_dir: str,
    community_report_send_to: ChatLLM,
    community_report_llm_args: ModelArgs,
    save: bool = True,
    try_load: bool = True,
):
    fn_name = "create_final_community_reports"
    if try_load and os.path.exists(
        os.path.join(query_output_dir, f"{fn_name}.parquet")
    ):
        return parquet_table_load(query_output_dir, fn_name)
    nodes = df_ops.prepare_community_reports_nodes(
        final_nodes_output,
    )
    edges = df_ops.prepare_community_reports_edges(
        final_relationship_output,
    )

    community_hierarchy = df_ops.restore_community_hierarchy(nodes)
    local_contexts = df_ops.prepare_community_reports(
        node_df=nodes,
        edge_df=edges,
        claim_df=None,
    )
    dataset = df_ops.create_community_reports(
        community_report_send_to=community_report_send_to,
        local_contexts=local_contexts,
        nodes=nodes,
        community_hierarchy=community_hierarchy,
        strategy={
            "extraction_prompt": COMMUNITY_REPORT_PROMPT,
            "max_report_length": 2000,
            "max_input_length": 8000,
        },
        community_report_llm_args=community_report_llm_args,
    )

    '''
    Causing error:    
    '''
    dataset = df_ops.window(
        dataset, **{"to": "id", "operation": "uuid", "column": "community"}
    )

    if save:
        parquet_table_save(query_output_dir, fn_name, dataset)
    return dataset
