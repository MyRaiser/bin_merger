from bin_merger import BinaryFile, Merger

x1 = BinaryFile(path='bootloader.bin')
x2 = BinaryFile(path='funflash.bin')
x3 = BinaryFile(path='entryinit.bin')

y = Merger(
    [x1, x2, x3],
    [0x00000000, 0x0003D800, 0x0003E000]
    ).merge()
y.save('target.bin')