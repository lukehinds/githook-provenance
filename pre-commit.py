#!/usr/bin/env python                                                                    
# -*- coding: UTF-8 -*-                                                                  
#post-commit

import base64
import binascii
import os
import json
import subprocess
import shutil
import uuid
import pprint
from pathlib import Path
from in_toto import runlib
import in_toto.models.metadata as metadata

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

# TODO: this needs a better name
from sigstore_pycode import register_fulcio_key

commit_files = ['git', 'diff-index', '--cached', '--name-only', 'HEAD']

output = subprocess.check_output(commit_files, encoding='UTF-8')
output = output.replace('\r\n', ',').replace("'", '')

# rewrite the below for IET6
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

private_key, email, payload = register_fulcio_key()

signed = json.loads(str(link_out))

signature = private_key.sign(
        str(signed['signed']).encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
)

signature_decoded = (binascii.b2a_hex(signature).decode())

root_cert = payload[0]
client_cert = payload[1]

signed['signatures'].append({
    'key_id': email,
    'signature': signature_decoded,
    'client_cert': client_cert,
    'root_cert': root_cert
})

tag =  ['git', 'rev-parse', '--short', 'HEAD']
output = subprocess.check_output(tag, encoding='UTF-8')

link_filename = 'link_' + output.strip('\n') + '.link'

print(link_filename)
with open(link_filename, 'w') as outfile:
    json.dump(signed, outfile)

subprocess.run(["git", "update-index", "--add", link_filename])
