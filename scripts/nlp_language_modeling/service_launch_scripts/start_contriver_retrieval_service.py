# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
"""

from nemo.collections.nlp.modules.common.megatron.retrieval_services.contriever_server import ContriverRetrievalServer
from nemo.collections.nlp.modules.common.tokenizer_utils import get_nmt_tokenizer
from nemo.core.config import hydra_runner


def get_tokenizer(args):
    tokenizer = get_nmt_tokenizer(
        library=args.library,
        model_name=args.type,
        tokenizer_model=args.model,
        vocab_file=args.vocab_file,
        merges_file=args.merge_file,
        delimiter=args.delimiter,
    )
    if not hasattr(tokenizer, "pad_id"):
        tokenizer.add_special_tokens({'pad_token': '<pad>'})
    elif hasattr(tokenizer, "pad_id") and (tokenizer.pad_id is None or tokenizer.pad_id < 0):
        tokenizer.add_special_tokens({'pad_token': '<pad>'})
    return tokenizer


@hydra_runner(config_path="conf", config_name="contriver_service")
def main(cfg) -> None:
    tokenizer = get_tokenizer(cfg.tokenizer)

    server = ContriverRetrievalServer(cfg.service.filepath, tokenizer, cfg.service.max_answer_length,)
    server.run("0.0.0.0", cfg.service.port)


if __name__ == "__main__":
    main()  # noqa pylint: disable=no-value-for-parameter
