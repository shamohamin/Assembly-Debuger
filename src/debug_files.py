from src.patterns import PATTERNS
import pathlib
import os
import re
import logging
import subprocess
from subprocess import TimeoutExpired
import threading
# import gdb


class Debug:
    def __init__(self, files):
        self.files = files
        self.content = []
        self.file_to_be_debug = ''
        self.directory_of_file_to_be_debug = ''
        self.stack_label_patterns = [PATTERNS[key] for key in PATTERNS.keys(
        ) if key in ["add_esp", "pusha_pattern", "push_pattern", "sub_esp", "popa_pattern", "pop_pattern", "ret_pattern", 'mov_esp']]
        self.loop_patterns = [PATTERNS[key]
                              for key in PATTERNS.keys() if key in ["loop_pattern"]]
        self.content_index = None
        self.logger = None

    def __get_content(self, file):
        self.content, index = [], 1
        with open(file, 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                if re.search(PATTERNS['comment_pattern'], line.strip()):
                    continue
                self.content.append({
                    'content': str(line).rstrip(),
                    'line_number': index
                })
                index += 1

    def __set_debug_file(self, file):

        file_name = pathlib.Path(file).name
        self.directory_of_file_to_be_debug = os.path.join(
            os.path.dirname(__file__), 'temp', os.path.splitext(file_name)[0])
        self.file_to_be_debug = os.path.join(
            self.directory_of_file_to_be_debug, file_name)

        path_log_file = os.path.join(os.path.dirname(
            __file__), 'log', '{}.log'.format(os.path.splitext(file_name)[0]))

        logging.basicConfig(filename=path_log_file,
                            format='Time: %(asctime)s --- Level: %(levelname)s ---- message:  %(message)s',
                            filemode='w', datefmt='%Y-%m-%d %I:%M:%S %p')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        if not self.file_to_be_debug or not self.directory_of_file_to_be_debug:
            raise FileNotFoundError('this file: {} or directory: {} did not exists'.format(
                self.file_to_be_debug, self.directory_of_file_to_be_debug))

        # with open(self.file_to_be_debug, "w") as file:
        #     pass

    def __stack_checker(self):
        stack = []
        for line in self.content:
            line = str(line['content']).strip()
            if re.search(PATTERNS['pusha_pattern'], line):
                stack.append(line)
            if re.search(PATTERNS['push_pattern'], line):
                stack.append(line)
            if re.search(PATTERNS['popa_pattern'], line):
                if stack[-1] == "pusha":
                    stack.pop()
                else:
                    raise Exception(
                        "pusha and popa arent match check popa or pusha")
            if re.search(PATTERNS['pop_pattern'], line):
                if len(stack) != 0:
                    stack.pop()
                else:
                    raise Exception(
                        'Stack clearation was not complete please check ret keyboard and push pops.')
            if re.search(PATTERNS['add_esp'], line):
                splited = (line.split(',')[-1]).strip()
                number = re.findall(r'^\d+', splited)[0]
                num_of_pops = int(int(number) / 4)
                for _ in range(num_of_pops):
                    if stack[-1] != "pusha":
                        stack.pop()
                    else:
                        raise Exception(
                            'Stack clearation was not complete please check ret keyboard and push pops.')
            if re.search(PATTERNS['sub_esp'], line):
                splited = (line.split(',')[-1]).strip()
                number = re.findall(r'^\d+', splited)[0]
                num_of_pops = int(int(number) / 4)
                for _ in range(num_of_pops):
                    stack.push(line)
            print(stack)

        if len(stack) != 0:
            raise Exception(
                "Stack clearation was not complete please check ret keyboard and push pops.")

    def __write_pre_file(self):
        with open(self.file_to_be_debug, "a+") as file:
            flag, counter = False, 0
            for index, content in enumerate(self.content):
                file.write(content['content'] +
                           " ; line_number: " + str(content['line_number']) + '\n')
                if re.search(PATTERNS['segment_text'], content['content'].strip()):
                    for i_cont, i in enumerate(self.content[index + 1:]):
                        file.write(i['content'] +
                                   "; line_number:{}".format(
                                       str(i['line_number'])))
                        if re.search(PATTERNS['label_pattern'], i['content'].strip()):
                            flag = True
                            counter = i_cont
                            self.content_index = i_cont + index + 1
                            break
                        file.write('\n')
                if flag:
                    for con in self.content[counter + index + 1:]:
                        for pattern in self.stack_label_patterns:
                            if re.search(pattern, con['content'].strip()):
                                file.write(con['content'] +
                                           "; line_number:{}".format(
                                               str(con['line_number'])))
                                break
                        file.write('\n')
                    break

    def __loop_detection(self, content):
        file_data = []
        with open(self.file_to_be_debug, 'r') as file:
            file_data = file.readlines()

        for line in content:
            for pattern in self.loop_patterns:
                if re.search(pattern, line['content'].strip()):
                    label = None
                    splited = line['content'].strip().split(' ')
                    for split in splited:
                        if not (split == '' or re.search('^(?:loop|jmp)$', split.strip())):
                            label = split
                            break

                    if label:
                        print(label)

                        def jump_checker(content, label):
                            f = False
                            for index, con in enumerate(content):
                                con = str(con['content']).strip()
                                if re.search(pattern=f'{label}:$', string=con):
                                    for offset, loop_content in enumerate(content[index + 1:]):
                                        if re.search(r'^ret$', loop_content['content'].strip()):
                                            f = True
                                            file_data[loop_content['line_number'] - 1] = \
                                                loop_content['content'] + '; line_number:{}'.format(
                                                loop_content['line_number'])
                                            break
                                        file_data[loop_content['line_number']
                                                  ] = loop_content['content'] + '; line_number:{}'.format(loop_content['line_number'])

                                        if re.search(r'end_loop\d*$', loop_content['content'].strip()):
                                            f = True
                                            break
                                        elif re.search(PATTERNS['condition_pattern'], loop_content['content'].strip()):
                                            # /////////////// finding you know
                                            jump_checker(
                                                content[offset:], loop_content['content'].strip().split(' ')[-1])
                                        elif re.search(r'^(?:loop|jmp)\s+', loop_content['content'].strip()):
                                            f = True
                                            break
                                        file_data[loop_content['line_number']] += '\n'
                                if f:
                                    break
                        jump_checker(content, label)

        with open(self.file_to_be_debug, "w") as file:
            file.writelines(file_data)

    def __place_counter_and_incrementor(self):
        file_data = []
        with open(self.file_to_be_debug, 'r') as file:
            file_data = file.readlines()
        print("*" * 20)
        for content in self.content[self.content_index + 1:]:
            essential = str(str(content['content']).strip()).split(';')
            print(content)
            for es in essential:
                if re.search(r'^essential', str(es).strip()):
                    file_data[content['line_number'] - 1] = content['content'] + \
                        '; line_number:{} \n'.format(
                            str(content['line_number']))
            if re.search(PATTERNS['label_pattern'], content['content'].strip()) or re.search(PATTERNS['loop_pattern'], content['content'].strip()):
                file_data[content['line_number'] - 1] = content['content'] + \
                    '; line_number:{} \n'.format(
                    str(content['line_number']))
            # if re.search(PATTERNS['ret_pattern'], content['content'].strip()):
            #     file_data.append(' ')
            #     file_data[content['line_number']] = content['content'] + \
            #         '; line_number:{} \n'.format(
            #         str(content['line_number']))

        # file_data.append('\tret\n')
        with open(self.file_to_be_debug, 'w') as file:
            file.writelines(file_data)

    def __compiling_files(self):
        file_data = []
        for content in self.content[self.content_index + 1:]:
            with open(self.file_to_be_debug, 'r') as file:
                file_data = file.readlines()
            hold = content['content'] + \
                '; line_number:{}\n'.format(
                str(content['line_number']))
            print(hold)
            print(file_data)
            if hold in file_data:
                continue
            # print(hold in file_data)
            # break
            file_data[content['line_number']] = hold
            with open(self.file_to_be_debug, 'w') as file:
                file.writelines(file_data)

            proc = subprocess.Popen(
                ['make'], cwd=self.directory_of_file_to_be_debug, stdout=subprocess.PIPE)

            try:
                outs, errs = proc.communicate(timeout=15)
                if errs is None:
                    self.logger.info(
                        'compiling using makefile here is output -> %s' % str(outs.decode('utf-8')).replace('\n', '\t'))
                else:
                    self.logger.info(
                        'compiling using makefile here is output -> %s' % errs.decode('utf-8'))
                print('*' * 20)
                print(outs.decode('utf-8'), errs)
            except TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
                print(outs, errs)
                self.logger.critical(
                    'compiling was not ok here is message -> %s' % errs)

            proc = subprocess.Popen(
                ['make', 'run'], cwd=self.directory_of_file_to_be_debug, stdout=subprocess.PIPE)

            try:
                outs, errs = proc.communicate(timeout=10)
                if errs is None:
                    self.logger.info(
                        'compiling using makefile here is output -> %s' % str(outs.decode('utf-8')).replace('\n', '\t'))
                else:
                    self.logger.info(
                        'compiling using makefile here is output -> %s' % errs.decode('utf-8'))
                print('*' * 20)
                print(outs.decode('utf-8'), errs)
            except TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
                print(outs, errs)
                self.logger.critical(
                    'compiling was not ok here is message -> %s' % errs)

    def __filter_file(self):
        pass

    def __handling_subprocess_output(self, data, err, step='execution'):
        if err is not None:
            self.logger.critical('{} was not successfull err is: {}'.format(
                step, str(err.decode('utf-8'))))
        else:
            self.logger.info('{} was not successfull err is: {}'.format(
                step, str(data.decode('utf-8'))).replace('\n', '\t'))

    def send_keys_to_subprocces(self, input_func, keys):
        input_func.write(bytes(keys, 'utf-8'))
        input_func.flush()

    def execute(self):
        try:

            print(self.files)
            print(self.files[-1])
            # index = 0
            # for file in self.files:
            # if file == "/home/amin/Documents/asm_debuger/src/asm_src/merge.asm":
            # print('*' * 20)
            # print(file)
            # self.__get_content(file)
            # self.__set_debug_file(file)
            # self.logger.info('starting stack checker.')
            # self.__stack_checker()
            # self.logger.info('stack was ok :))')
            # self.logger.info('starting writing pre headers.')
            # self.__write_pre_file()
            # self.logger.info('writing pre headers is over.')
            # self.logger.info('checking loops')
            # self.__loop_detection(self.content)
            # self.logger.info('cheking and putting loop is over.')
            # self.logger.info('placing essetials and jump, labels.')
            # self.__place_counter_and_incrementor()
            # self.logger.info(
            #     'placing essetials and jump, labels is over.')
            # self.logger.info("heading to compiling files.")
            # self.__compiling_files()
            # print('everything is ok')
        except Exception as ex:
            self.logger.critical(ex.args[0])
            print(ex.args[0])
