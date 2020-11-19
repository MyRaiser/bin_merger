class BinaryFile():
    '''
    从硬盘中读取一个bin，提供显示、对比方法
    '''
    def __init__(self, *, binary=None, path=None, bytes_in_word=4):
        '''
        Args:
            bytes_in_word: 一个字中包含byte的个数
            binary: bytes
        '''

        if path is None:
            if bin is None:
                raise ValueError('You should either state path or bin')
            else:
                if type(binary) == bytes:
                    self.binary = binary
                elif type(binary) == list:
                    self.binary = bytes(binary)
                else:
                    raise ValueError('Incorrect type of binary.')
        else:
            with open(path, 'rb') as f:
                self.binary = f.read()
        
        self.bytes_in_word = bytes_in_word

    def __len__(self):
        return len(self.binary)

    def byte_list(self):
        return BinaryFile.split_by_byte(self.binary)

    # def word_list(self, order='LE'):
    #     '''
    #     Args:
    #         order: 'LE' or 'BE'
    #     '''
    #     return BinaryFile.split_by_word(self.bin, order, bytes_in_word = self.bytes_in_word)

    @staticmethod
    def split_by_byte(x:bytes):
        return [item for item in x]

    # @staticmethod
    # def split_by_word(x: bytes, order='LE', *, bytes_in_word=4):
    #     if order == 'LE':
    #         pass
    #     elif order == 'BE':
    #         pass
    #     else:
    #         raise ValueError("Incorrect order.(should be 'LE' or 'BE')")
    
    def hexdump(self, typ='byte', *, convert=False, order='LE'):
        '''
        Args:
            typ: 'byte' or 'word'
            convert: 是否转化为字符并打印。Windows terminal 默认用UTF-16LE打印会不正常。
            order: 'LE' or 'BE'
        '''
        if typ == 'byte':
            dump_list = []
            for index, item in enumerate(self.byte_list()):
                line = ["{:08X}".format(index), "{:02X}".format(item)]
                if convert:
                    line.append(chr(item))
                dump_list.append(line)
                print(*line)
                
        elif typ == 'word':
            dump_list = []
            len_bin = len(self.byte_list())
            for index in range(0, len_bin, self.bytes_in_word):
                if order == 'BE':
                    item_list = ["{:02X}".format(self.binary[index + j]) for j in range(self.bytes_in_word)]
                elif order == 'LE':
                    item_list = ["{:02X}".format(self.binary[index + j]) for j in reversed(range(self.bytes_in_word))]
                line = ["{:08X}".format(index)] + item_list
                if convert:
                    chr_list = [chr(self.bin[index + j]) for j in range(self.bytes_in_word)]
                    line +=  chr_list 
                print(*line)    
        else:
            raise ValueError('Incorrect type.')

    def save(self, path):
        '''
            save to path.
        '''
        with open(path, 'wb') as f:
            f.write(self.binary)
            

        

class Merger():
    def __init__(self, images: list, start_addrs: list, *, fill=0x00):
        '''
        Args:
            images: list of BinaryFile, the bin behind has higher priority
            fill: fill with this value if all bins doesn't take this byte

            in the final .bin, every bin occupies [start_addr, len(bin))
        '''
        self.images = images
        self.start_addrs = start_addrs
        self.fill = fill

    def merge(self):
        len_target = max(*[(self.start_addrs[i] + len(self.images[i])) for i in range(len(self.images))])
        # 用默认值初始化
        target_list = [self.fill for i in range(len_target)]

        # 合并
        for index, image in enumerate(self.images):
            start = self.start_addrs[index]
            end = start + len(image)
            target_list[start:end] = image.byte_list()

        return BinaryFile(binary=target_list)


# with open('bootloader.bin','rb') as f:
#     x = f.read()
#     strr = ''
#     # valid = []
#     #     for i in range(ord('a'), ord('z') + 1):
#     #         valid.append(i)
#     #     for i in range(ord('A'), ord('Z') + 1):
#     #         valid.append(i)
#     #     for i in range(ord('0'), ord('9') + 1):
#     #         valid.append(i)
#     #     valid.append(ord('['))
#     #     valid.append(ord(']'))
#     #     if item in valid:
#     for index, item in enumerate(x):
#         strr += chr(item)
#         print("{:08x}".format(index), "{:02x}".format(item), chr(item))
#     print(x)# 会因为意外的终止符提前结束打印？
#     print(strr)

if __name__ == "__main__":

    x1 = BinaryFile(path='target.bin')
    x2 = BinaryFile(path='boot.bin')
    print(len(x1),len(x2))
    for i in range(len(x1)):
        if x1.binary[i] != x2.binary[i]:
            print("{:08X}".format(i),x1.binary[i],x2.binary[i])
