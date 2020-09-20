import threading
import gdb
import sys
import argparse
import time
import logging


def loop_for_ever():
    raise Exception('while loop for ever!!!!!')


def main(labels):
    try:
        timer = threading.Timer(60.0, loop_for_ever)
        timer.setDaemon(True)
        timer.start()

        for lbl in labels:
            gdb.execute(
                'break {}'.format(lbl), to_string=True)
            print('***************' * 2)
            print("breaking in label: {}".format(lbl))
            time.sleep(2)
            out = gdb.execute('run < input.txt')

            while True:
                try:
                    gdb.execute('nexti')
                except Exception:
                    out = gdb.execute('info registers', to_string=True)
                    print(out)
                    break
    except Exception as ex:
        print(ex)
    else:
        timer.cancel()
    finally:
        gdb.execute('quit')
        gdb.write('q')


def check_parameters(argv):
    arg_parser = argparse.ArgumentParser(
        prog='gdb_execution.py',
        description='List the labels of a assembley files',
        usage='%(prog)s [options] -l '
    )
    arg_parser.add_argument(
        '--labels', '-l', type=str, help='list of labels like: print_array,main_asm,...', required=True)
    args = arg_parser.parse_args()

    return str(args.labels).split(',')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(
        "\nfor every assembly file you have please insert main label of that file please follow the rules below.")
    print('\nenter labels like: label1,label2,... \n \n')
    labels = input('Insert labels: ')
    labels = labels.split(',')
    if len(labels) == 0:
        raise Exception('enter at least one label')
    else:
        main(labels)
