import math
import asyncio
from tqdm.asyncio import tqdm as tqdm_async
from graphgen.models import NetworkXStorage, OpenAIModel, JsonKVStorage
from graphgen.utils import logger, yes_no_loss_entropy
from graphgen.templates import STATEMENT_JUDGEMENT_PROMPT


async def judge_statement( # pylint: disable=too-many-statements
        trainee_llm_client: OpenAIModel,
        graph_storage: NetworkXStorage,
        rephrase_storage: JsonKVStorage,
        re_judge: bool = False,
        max_concurrent: int = 1000) -> NetworkXStorage:
    """
    Get all edges and nodes and judge them

    :param trainee_llm_client: judge the statements to get comprehension loss
    :param graph_storage: graph storage instance
    :param rephrase_storage: rephrase storage instance
    :param re_judge: re-judge the relations
    :param max_concurrent: max concurrent
    :return:
    """

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _judge_single_relation(
        edge: tuple,
    ):
        async with semaphore:
            source_id, target_id, edge_data = edge[0], edge[1], edge[2]

            # ▼▼▼▼▼ ここからが修正箇所 ▼▼▼▼▼
            logger.debug("--- Start Judging Relation: {} -> {} ---", source_id, target_id)

            if (not re_judge) and "loss" in edge_data and edge_data["loss"] is not None:
                logger.info("Edge {} -> {} already judged, loss: {}, skip", source_id, target_id, edge_data["loss"])
                return source_id, target_id, edge_data

            description = edge_data.get("description", "")
            logger.debug("  - Original Description: '{}'", description)
            if not description:
                logger.warning("  - Description is empty for relation {} -> {}. Skipping.", source_id, target_id)
                edge_data["loss"] = -math.log(0.1)
                await graph_storage.update_edge(source_id, target_id, edge_data)
                return source_id, target_id, edge_data

            try:
                descriptions = await rephrase_storage.get_by_id(description)
                logger.debug("  - Fetched rephrased data from storage: {}", descriptions)

                if not descriptions:
                    logger.warning(
                        "  - No rephrased data found for relation '{}' -> '{}'. Using default loss.",
                        source_id, target_id
                    )
                    edge_data["loss"] = -math.log(0.1)
                    await graph_storage.update_edge(source_id, target_id, edge_data)
                    return source_id, target_id, edge_data

                judgements = []
                gts = [gt for _, gt in descriptions]
                for i, (desc_text, gt) in enumerate(descriptions):
                    prompt = STATEMENT_JUDGEMENT_PROMPT['TEMPLATE'].format(statement=desc_text)
                    logger.debug("  - [Loop {}] Prompt to LLM: '{}'", i, prompt)

                    judgement_response = await trainee_llm_client.generate_topk_per_token(prompt)
                    logger.debug("  - [Loop {}] LLM Raw Response: {}", i, judgement_response)

                    if not judgement_response:
                        logger.warning(
                            "LLM returned no valid tokens for relation '{}' -> '{}'. Prompt: '{}'. Skipping this rephrase.",
                            source_id, target_id, prompt
                        )
                        continue  # この言い換え文の評価をスキップして次のループへ

                    if not judgement_response[0].top_candidates:
                        logger.warning(
                            "LLM response for relation '{}' -> '{}' has no top_candidates. Skipping this rephrase.",
                            source_id, target_id
                        )
                        continue  # この言い換え文の評価をスキップ

                    judgements.append(judgement_response[0].top_candidates)

                logger.debug("  - Data for loss calculation: judgements={}, gts={}", judgements, gts)
                loss = yes_no_loss_entropy(judgements, gts)

                logger.info("  - SUCCESS: Judged relation {} -> {} | Loss: {}", source_id, target_id, loss)

                edge_data["loss"] = loss
            except Exception as e:
                logger.error(
                    "  - FAILURE: Error judging relation {} -> {}. Error Type: {}. Error: {}",
                    source_id, target_id, type(e).__name__, e, exc_info=True
                )
                logger.info("  - Assigning default loss 0.1")
                edge_data["loss"] = -math.log(0.1)
            
            logger.debug("--- End Judging Relation: {} -> {} ---", source_id, target_id)
            # ▲▲▲▲▲ ここまでが修正箇所 ▲▲▲▲▲

            await graph_storage.update_edge(source_id, target_id, edge_data)
            return source_id, target_id, edge_data

    edges = await graph_storage.get_all_edges()
    
    # 実行前にリスト化して tqdm で正しく進捗表示
    edge_list = list(edges)
    results = []
    for result in tqdm_async(
            asyncio.as_completed([_judge_single_relation(edge) for edge in edge_list]),
            total=len(edge_list),
            desc="Judging relations"
    ):
        results.append(await result)

    async def _judge_single_entity(
        node: tuple,
    ):
        async with semaphore:
            node_id, node_data = node[0], node[1]
            
            # ▼▼▼▼▼ ここからが修正箇所 ▼▼▼▼▼
            logger.debug("--- Start Judging Entity: {} ---", node_id)

            if (not re_judge) and "loss" in node_data and node_data["loss"] is not None:
                logger.info("Node {} already judged, loss: {}, skip", node_id, node_data["loss"])
                return node_id, node_data

            description = node_data.get("description", "")
            logger.debug("  - Original Description: '{}'", description)
            if not description:
                logger.warning("  - Description is empty for entity {}. Skipping.", node_id)
                node_data["loss"] = -math.log(0.1)
                await graph_storage.update_node(node_id, node_data)
                return node_id, node_data

            try:
                descriptions = await rephrase_storage.get_by_id(description)
                logger.debug("  - Fetched rephrased data from storage: {}", descriptions)

                if not descriptions:
                    logger.warning(
                        "  - No rephrased data found for entity '{}'. Using default loss.",
                        node_id
                    )
                    node_data["loss"] = -math.log(0.1)
                    await graph_storage.update_node(node_id, node_data)
                    return node_id, node_data

                judgements = []
                gts = [gt for _, gt in descriptions]
                for i, (desc_text, gt) in enumerate(descriptions):
                    prompt = STATEMENT_JUDGEMENT_PROMPT['TEMPLATE'].format(statement=desc_text)
                    logger.debug("  - [Loop {}] Prompt to LLM: '{}'", i, prompt)

                    judgement_response = await trainee_llm_client.generate_topk_per_token(prompt)
                    logger.debug("  - [Loop {}] LLM Raw Response: {}", i, judgement_response)
                    
                    if not judgement_response:
                        logger.warning(
                            "LLM returned no valid tokens for entity '{}'. Prompt: '{}'. Skipping this rephrase.",
                            node_id, prompt
                        )
                        continue

                    if not judgement_response[0].top_candidates:
                        logger.warning(
                            "LLM response for entity '{}' has no top_candidates. Skipping this rephrase.",
                            node_id
                        )
                        continue

                    judgements.append(judgement_response[0].top_candidates)

                logger.debug("  - Data for loss calculation: judgements={}, gts={}", judgements, gts)
                loss = yes_no_loss_entropy(judgements, gts)

                logger.info("  - SUCCESS: Judged entity {} | Loss: {}", node_id, loss)

                node_data["loss"] = loss
            except Exception as e:
                logger.error(
                    "  - FAILURE: Error judging entity {}. Error Type: {}. Error: {}",
                    node_id, type(e).__name__, e, exc_info=True
                )
                logger.info("  - Assigning default loss 0.1")
                node_data["loss"] = -math.log(0.1)
            
            logger.debug("--- End Judging Entity: {} ---", node_id)
            # ▲▲▲▲▲ ここまでが修正箇所 ▲▲▲▲▲

            await graph_storage.update_node(node_id, node_data)
            return node_id, node_data

    nodes = await graph_storage.get_all_nodes()
    
    # 実行前にリスト化して tqdm で正しく進捗表示
    node_list = list(nodes)
    results = []
    for result in tqdm_async(
            asyncio.as_completed([_judge_single_entity(node) for node in node_list]),
            total=len(node_list),
            desc="Judging entities"
    ):
        results.append(await result)

    return graph_storage


async def skip_judge_statement(
        graph_storage: NetworkXStorage,
        max_concurrent: int = 1000
):
    """
    Skip the judgement of the statement
    :param graph_storage: graph storage instance
    :param max_concurrent: max concurrent
    :return:
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def _skip_single_relation(
        edge: tuple,
    ):
        async with semaphore:
            source_id, target_id, edge_data = edge[0], edge[1], edge[2]

            if "loss" in edge_data and edge_data["loss"] is not None:
                # ログフォーマットを修正
                logger.info("Edge {} -> {} already judged, loss: {}, skip", source_id, target_id, edge_data["loss"])
                return source_id, target_id, edge_data

            edge_data["loss"] = -math.log(0.1)
            await graph_storage.update_edge(source_id, target_id, edge_data)
            return source_id, target_id, edge_data

    edges = await graph_storage.get_all_edges()
    edge_list = list(edges)
    results = []
    for result in tqdm_async(
            asyncio.as_completed([_skip_single_relation(edge) for edge in edge_list]),
            total=len(edge_list),
            desc="Skipping judgement of relations"
    ):
        results.append(await result)

    async def _skip_single_entity(
        node: tuple,
    ):
        async with semaphore:
            node_id, node_data = node[0], node[1]

            if "loss" in node_data and node_data["loss"] is not None:
                # ログフォーマットを修正
                logger.info("Node {} already judged, loss: {}, skip", node_id, node_data["loss"])
                return node_id, node_data

            node_data["loss"] = -math.log(0.1)
            await graph_storage.update_node(node_id, node_data)
            return node_id, node_data

    nodes = await graph_storage.get_all_nodes()
    node_list = list(nodes)
    results = []
    for result in tqdm_async(
            asyncio.as_completed([_skip_single_entity(node) for node in node_list]),
            total=len(node_list),
            desc="Skipping judgement of entities"
    ):
        results.append(await result)

    return graph_storage
