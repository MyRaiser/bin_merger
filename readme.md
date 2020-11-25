# bin_merger
## Sample
Assume i want to merge 3 .bin file:

- `bootloader.bin`
- `image1.bin`
- `image2.bin`

and they start from address:

- 0x00000000
- 0x00010000
- 0x00020000

*Notice that if one .bin is too large to fit in the space, part of the content could be overwritten by next .bin.*

*e.g. if parameter is [x1,x2,x3], priority x3 > x2 > x1*

the output .bin file named as: `target.bin`

the code should be:

```py
from bin_merger import BinaryFile, Merger

x1 = BinaryFile('bootloader.bin')
x2 = BinaryFile('image1.bin')
x3 = BinaryFile('image2.bin')

y = Merger(
    [x1, x2, x3],
    [0x00000000, 0x00010000, 0x00020000]
    ).merge()
y.save('target.bin')
```
