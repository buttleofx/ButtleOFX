
def touch(file_path):
    # try:
    #     if os.path.exists(file_path):
    #         raise
    # except:
    #     print(File already )
    print('create_file')
    open(file_path, 'a').close()
