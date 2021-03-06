import os
from shutil import copyfile

cvtl_method_list = ['lbptop','biwoof']
dbtype = ['smic', 'casme2', 'samm']
dbmeta_fn = ['smic-3classes', 'casme2-5classes', 'samm-5classes']

def main():
    feat_type = 'lbptop'
    version = 1 # starting from 1
    data_dir = os.path.join('..', 'dataset', 'v_{}'.format(version))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for i, dbname in enumerate(dbtype):
        subjectDir = os.path.join(data_dir, dbname) # like "dataset/v_1/smic"
        if not os.path.exists(subjectDir):
            os.makedirs(subjectDir)
        feat_dir = os.path.join('..', 'dataset', '{}_db'.format(feat_type), dbname)
        file_path = os.path.join('..', 'dataset', 'benchmark_db', '{}.csv'.format(dbmeta_fn[i]))
        meta_dict = {'subject':[],'filename':[],'emotion':[]}
        with open(file_path,'r') as f:
            for textline in f:
                texts = textline.strip('\n').split(',')
                meta_dict['subject'].append(texts[0])
                meta_dict['filename'].append(texts[1])
                meta_dict['emotion'].append(int(texts[5]))
        subjects = list(set(meta_dict['subject']))
        subjects.sort()
        sampleN = len(meta_dict['filename'])
        sub_f = open(os.path.join(subjectDir, 'subName.txt'), 'w')
        for subject in subjects:
            # open the training/val/test list file
            file_path = os.path.join(subjectDir, '{}_train.txt'.format(subject))
            train_f = open(file_path,'w')
            file_path = os.path.join(subjectDir, '{}_test.txt'.format(subject))
            test_f = open(file_path,'w')
            sub_f.write('{}\n'.format(subject))
            # traverse each item
            for j in range(0,sampleN):
                file_name = '{}_{}.csv'.format(meta_dict['subject'][j], meta_dict['filename'][j])
                file_path = os.path.join(subjectDir, file_name)
                filePath_src = os.path.join(feat_dir, file_name)
                if meta_dict['subject'][j] == subject:
                    test_f.write('{} {}\n'.format(filePath_src, meta_dict['emotion'][j]))
                    # copyfile(filePath_src, file_path)
                else:
                    train_f.write('{} {}\n'.format(filePath_src, meta_dict['emotion'][j]))
                    # copyfile(filePath_src, file_path)
            print('The subject: {}.'.format(subject))
            train_f.close()
            test_f.close()
        sub_f.close()

if __name__ == '__main__':
    main()