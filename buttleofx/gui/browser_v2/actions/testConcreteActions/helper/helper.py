import os

def touch(file_path):
    open(file_path, 'a').close()

def create_sequence(path, seq_name='seq', seq_length=3, sep='_',
                    extension='.jpg'):
    file_count = 9 if seq_length > 9 else seq_length
    for i in range(file_count):
        filename = seq_name + sep + '00' + str(i) + extension
        file_path = os.path.join(path, filename)
        touch(file_path)

