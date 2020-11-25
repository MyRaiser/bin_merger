from bin_merger import BinaryFile, Merger

x1 = BinaryFile('bootloader.bin')
x2 = BinaryFile('funflash.bin')
x3 = BinaryFile('entryinit.bin')

y = Merger(
    [x1, x2, x3],
    [0x00000000, 0x0003D800, 0x0003E000],
    fill=0xff
).merge()
y.save('target.bin')
y.compare(BinaryFile('boot.bin'))
