import os

class UnknownMarkerException(Exception):
    pass

class MarkerNotFoundException(Exception):
    pass

marker_SOI = b'\xff\xd8'   # start of image
marker_EOI = b'\xff\xd9'   # end of image

marker_COM = b'\xff\xfe'   # comment
marker_DQT = b'\xff\xdb'   # quantization table
marker_SOF0 = b'\xff\xc0'  # baseline DCT
marker_DHT = b'\xff\xc4'   # Huffman table
marker_JFIF = b'\xff\xe0'  # JPEG File Interchange Format
marker_SOS = b'\xff\xda'   # start of scan




def parse(filename):
    """returns list of sectors of the file"""

    marks = {marker_SOS: 'Image:', marker_DQT: 'Quantization table:',
             marker_DHT: 'Huffman table:', marker_SOF0: 'baseline DCT:',
             marker_COM: 'Comment:', marker_SOI: 'Start of image:',
             marker_EOI: 'End of image:',
             marker_JFIF: 'JPEG File Interchange Format:'}

    # funcs = {marker_SOS: start_of_scan(), marker_DQT: set_quantization_table(),
    #          marker_DHT: set_huffman_table(), marker_SOF0: 'baseline DCT',
    #          marker_COM: read_comment(f, l)}
    sectors = {}

    with open(filename, 'rb') as f:
        start_mark = f.read(2)
        if start_mark != marker_SOI:
            raise MarkerNotFoundException('start marker not found')

        while(True):
            marker = f.read(2)
            length = sum(f.read(2)) - 2
            if marker not in marks.keys():
                raise UnknownMarkerException(marker)

            if marker == marker_COM:
                sector = read_comment(f,length)
            elif marker == marker_DHT:
                sector = set_huffman_table(f, length)
            elif marker == marker_SOF0:
                sector = set_base_encode_method(f, length)
            elif marker == marker_DQT:
                sector = set_quantization_table(f,length)
            elif marker == marker_SOS:
                sector = start_of_scan(f, length)
                sectors[marks[marker]] = sector
                break
            else:
                raise UnknownMarkerException(marker)
            sectors[marks[marker]] = sector
        return sectors

# все нижеследующие методы не реализованы вообщеы
def set_quantization_table(f,l):
    # первые два байта - размер
    # [0_]    Длина значений в таблице: 0 (0 — 1 байт, 1 — 2 байта)
    # [_0]    Идентификатор таблицы: 0
    # Потом заполняем таблицу zigzag order
    return f.read(l)

def set_huffman_table(f, l):
    # FF C4 00 15 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 02
    # [00 15] длина: 21 байт.
    # [0_]    класс: 0 (0 — таблица DC коэффициэнтов, 1 — таблица AC коэффициэнтов).
    # [_0]    идентификатор таблицы: 0
    # Длина кода Хаффмана: 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
    # Количество кодов:  [01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00]
    # НУЖНО САМОМУ ПОСТРОИТЬ ДЕРЕВО!
    return f.read(l)

def start_of_scan(f, l):
    # FF DA 00 0C 03 01 00 02 11 03 11 00 3F 00
    # [00 0C] Длина заголовочной части (а не всей секции): 12 байт.
    # [03]    Количество компонентов сканирования. У нас 3, по одному на Y, Cb, Cr.
    #
    # 1-й компонент:
    # [01] Номер компонента изображения: 1 (Y)
    # [0_] Идентификатор таблицы Хаффмана для DC коэффициэнтов: 0
    # [_0] Идентификатор таблицы Хаффмана для AC коэффициэнтов: 0
    #
    # 2-й компонент:
    # [02] Номер компонента изображения: 2 (Cb)
    # [1_] Идентификатор таблицы Хаффмана для DC коэффициэнтов: 1
    # [_1] Идентификатор таблицы Хаффмана для AC коэффициэнтов: 1
    #
    # 3-й компонент:
    # [03] Номер компонента изображения: 3 (Cr)
    # [1_] Идентификатор таблицы Хаффмана для DC коэффициэнтов: 1
    # [_1] Идентификатор таблицы Хаффмана для AC коэффициэнтов: 1
    f.read(l+1)
    data = f.read()[:-2]
    return data

def set_base_encode_method(f, l):
    return f.read(l)

def read_comment(f, l):
    return f.read(l)



if __name__ == '__main__':
    parse('ex.jpg')


