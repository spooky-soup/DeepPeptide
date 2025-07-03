from ....ProSST.prosst.structure.get_sst_seq import SSTPredictor
import argparse
import pathlib
import os
from tqdm import tqdm
from hashlib import md5
import torch


def hash_aa_string(string):
    return md5(string.encode()).digest().hex()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('struc_dir',
                        type=pathlib.Path,
                        help='Path to folder with structures (.pdb)')

    parser.add_argument('output_dir',
                        type=pathlib.Path,
                        help="output directory for extracted representations"
                        )

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    predictor = SSTPredictor(structure_vocab_size=2048)

    pdb_paths = os.listdir(path=args.struc_dir)

    for pdb in tqdm(pdb_paths):
        prot_id = pdb.split('/')[-1].split('.')[0]
        print(prot_id)
        if os.path.isfile(f'{args.output_dir}/{prot_id}.pt'):
                print("Already processed sequence")
                continue
        pred = predictor.predict_from_pdb(pdb)
        toks = pred['2048_sst_seq']
        out = torch.cat(toks, dim=1).cpu()
        print(out)
        # set nan to zeros
        out[out!=out] = 0.0
        res = out.transpose(0,1)[1:-1]
        seq_embedding = res[:,0]
        output_file = open(f'{args.output_dir}/{prot_id}.pt', 'wb')
        torch.save(seq_embedding, output_file)
        output_file.close()
