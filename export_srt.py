import xml.etree.ElementTree as ET
import datetime
import sys


class MyProduce():
    text = ''
    start = None
    end = None

    def __lt__(self, obj):
        return self.start_time() < obj.start_time()

    def start_time(self):
        return self.start

    def end_time(self):
        return self.end


def export_srt(input_mlt:str) -> str:
    tree = ET.parse(input_mlt)
    root = tree.getroot()
    
    elem_map = {}
    for child in root:
        if 'id' in child.attrib.keys():
            elem_map[child.attrib['id']] = child


    producer_info = []
    for key in elem_map:
        elem = elem_map[key]

        if 'playlist' != elem.tag:
            continue

        playlist = elem
        basedate = datetime.datetime(1900, 1, 1)
        for child in playlist:
            if child.tag == 'entry':
                my_produce = MyProduce()
                producer_id = child.attrib['producer']
                if 'producer' in child.attrib:
                    producer = elem_map[producer_id]
                    filters = producer.findall(".//filter//property[@name='argument']")
                    for idx, f in enumerate(filters):
                        if idx > 0:
                            my_produce.text += '\n'
                        if f.text:
                            my_produce.text += f.text
                    my_produce.start = basedate
                    
                    out_date = datetime.datetime.strptime(child.attrib['out'], '%H:%M:%S.%f')
                    in_date = datetime.datetime.strptime(child.attrib['in'], '%H:%M:%S.%f')
                    
                    # FIXME: figure out why should I add delta
                    prod_out_date = datetime.datetime.strptime(producer.attrib['out'], '%H:%M:%S.%f')
                    prod_max_date = datetime.datetime.strptime('04:00:00.000', '%H:%M:%S.%f')
                    prod_delta = prod_max_date - prod_out_date
                    delta = out_date - in_date + datetime.timedelta(milliseconds=int(prod_delta.microseconds / 1000))
                    basedate += delta

                    my_produce.end = basedate
                    
                    if len(my_produce.text) > 0:
                        producer_info.append(my_produce)
                else:
                    out_date = datetime.datetime.strptime(child.attrib['out'], '%H:%M:%S.%f')
                    in_date = datetime.datetime.strptime(child.attrib['in'], '%H:%M:%S.%f')
                    delta = out_date - in_date
                    basedate += delta
            
            elif child.tag == 'blank':
                len_date = datetime.datetime.strptime(child.attrib['length'], '%H:%M:%S.%f')
                default_date = datetime.datetime(1900, 1, 1)
                delta = len_date - default_date
                basedate += delta
            
    producer_info.sort()

    result_text = ''
    for idx, prod in enumerate(producer_info):
        result_text += f'{idx + 1}\n'
        result_text += f"{prod.start_time().strftime('%H:%M:%S,%f')[:-3]} --> {prod.end_time().strftime('%H:%M:%S,%f')[:-3]}\n"
        result_text += f"{prod.text}\n\n"
    
    return result_text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:\n')
        print('\tpython export_srt.py MLT_FILE')
        exit(0)
    
    input_mlt = sys.argv[1]

    srt_text = export_srt(input_mlt)
    print(srt_text)