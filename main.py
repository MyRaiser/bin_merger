from bin_merger import BinaryFile, Merger

x1 = BinaryFile(path='bootloader.bin')
x2 = BinaryFile(path='image1.bin')
x3 = BinaryFile(path='image2.bin')

y = Merger(
    [x1, x2, x3],
    [0x00000000, 0x00010000, 0x00020000]
    ).merge()
y.save('target.bin')