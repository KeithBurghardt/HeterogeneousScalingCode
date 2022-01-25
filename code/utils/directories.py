import os


def make_dir(path):
    if os.path.exists(path):
        return
    os.mkdir(path)


def prepare_dir(path):
    files = os.listdir(path)
    if not files:
        with open(os.path.join(path, '123.txt'), 'w') as f:
            f.write('')
    if len(files) == 1:
        return
    if len(files) >= 2:
        if '123.txt' in files:
            os.remove(os.path.join(path, '123.txt'))


class Directory:
    def __init__(self, field_of_study):
        self.directory_root = ['/data/libo/hezihao/institutions_scaling/',
                               "C:/Users/hezh/Documents/OneDrive/2018USC-ISI/institution_scaling"][0]

        self.field_of_study = {'physics': 'physics',
                               'cs': 'computer_science',
                               'math': 'mathematics',
                               'sociology': 'sociology'}[field_of_study]

        self.directory_data = os.path.join(self.directory_root, 'data', self.field_of_study)
        self.directory_papers = os.path.join(self.directory_data, 'papers')
        self.directory_mag_data = os.path.join(self.directory_data, 'mag_data')
        self.directory_institutions = os.path.join(self.directory_data, 'institutions')

        self.directory_results = os.path.join(self.directory_root, 'results', self.field_of_study)
        self.directory_dataset_description = os.path.join(self.directory_results, 'dataset_description')
        self.directory_scaling_with_institution_size = os.path.join(self.directory_results, 'scaling_with_institution_size')
        self.directory_scaling_with_collaborations = os.path.join(self.directory_results, 'scaling_with_collaborations')
        self.directory_urn_model = os.path.join(self.directory_results, 'urn_model')
        self.directory_collab_of_institutions = os.path.join(self.directory_dataset_description, 'collab_of_institutions')
        self.directory_institution_description = os.path.join(self.directory_dataset_description, 'institution_description')
        self.directory_author_collab = os.path.join(self.directory_dataset_description, 'author_collab')

        self.directory_figures = os.path.join(self.directory_root, 'figures', self.field_of_study)

        self.directories = [self.directory_data,
                            self.directory_papers,
                            self.directory_mag_data,
                            self.directory_institutions,
                            self.directory_results,
                            self.directory_dataset_description,
                            self.directory_scaling_with_institution_size,
                            self.directory_scaling_with_collaborations,
                            self.directory_urn_model,
                            self.directory_collab_of_institutions,
                            self.directory_institution_description,
                            self.directory_author_collab,
                            self.directory_figures,
                            ]

    def refresh(self):
        for directory in self.directories:
            make_dir(directory)
            prepare_dir(directory)
