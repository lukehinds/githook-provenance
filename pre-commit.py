#!/usr/bin/env python                                                                    
# -*- coding: UTF-8 -*-                                                                  
#post-commit

import os
import json
import subprocess
import uuid
import pprint
from pathlib import Path
from in_toto import runlib
import in_toto.models.metadata as metadata

# TODO: this needs a better name
from sigstore_pycode import register_fulcio_key

commit_files = ['git', 'diff-index', '--cached', '--name-only', 'HEAD']

output = subprocess.check_output(commit_files, encoding='UTF-8')
output = output.replace('\r\n', ',').replace("'", '')

link_out = runlib.in_toto_run(
        # Do not record files matching these patterns.
        exclude_patterns= ['.gitignore'],
        # Do not execute any other command.
        link_cmd_args=[],
        # Do not record anything as input.
        material_list=None,
        # Use this step name.
        name='step-name',
        # Record every source file, except for exclude_patterns, as output.
        product_list=output.split(),
        # Keep file size down
        compact_json=True,
    )

private_key, payload = register_fulcio_key()
print("Fulcio root: ", str(payload))
# link file
# filename = str(uuid.uuid4())
# link_out.sign(private_key)
# link_out.dump(filename)

# add the link file below
# subprocess.run(["git", "update-index", "--add", link_file])
