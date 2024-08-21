import argparse
import os.path
import json

from metaloop.client.mds import MDS


def parse_args():
    parser = argparse.ArgumentParser(description='export and download data from metaloop')
    parser.add_argument('--api_addr', required=True, help='address of metaloop API')
    parser.add_argument('--user_token', required=True, help='user token used to access metaloop API')
    parser.add_argument('--train_dataset_ids', required=True, help='IDs of training dataset to export')
    parser.add_argument('--test_dataset_ids', default='', help='IDs of test dataset to export')
    parser.add_argument('--online_dataset_ids', default='', help='IDs of online dataset to export')
    parser.add_argument('--output_path', default='', help='local path to store downloaded data')
    parser.add_argument('--only_json', default=False, help='only output.json,not dataset data')
    return parser.parse_args()


def get_data(mds_client, dataset_ids, flag='train',only_json=False):
    if not dataset_ids:
        return

    output_path = os.path.join(args.output_path, flag)
    if not os.path.exists(output_path):
        os.makedirs(output_path, 0o0755, True)
    else:
        print(f'{output_path} exists, skip download data')
        return

    mds_client.export_annotated_data(dataset_ids.split(','), output_path,only_json=only_json)
    if os.path.exists(os.path.join(output_path, 'output.json')):
        if only_json:
            os.rename(os.path.join(output_path, 'output.json'),os.path.join(output_path, 'input.json'))
        else:
            file_out = open(os.path.join(output_path, 'input.json'), 'w')
            with open(os.path.join(output_path, 'output.json'), 'r') as f:
                for line in f:
                    data = json.loads(line)
                    data['url_image'] = os.path.join(output_path, data['url_image'])
                    json.dump(data, file_out, ensure_ascii=False)
                    file_out.write('\n')
            file_out.close()
            os.remove(os.path.join(output_path, 'output.json'))


def main(args):
    mds_client = MDS(args.user_token, args.api_addr)
    if args.only_json == 'true':
        args.only_json = True
    else:
        args.only_json = False

    get_data(mds_client, args.train_dataset_ids, 'train',args.only_json)
    get_data(mds_client, args.test_dataset_ids, 'test',args.only_json)
    get_data(mds_client, args.online_dataset_ids, 'online',args.only_json)


if __name__ == '__main__':
    args = parse_args()
    main(args)
