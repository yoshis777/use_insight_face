import os
import pprint

import insightface
import numpy as np
import PIL.Image


from file import File
from util import Util


def read_image(file_path):
    image = PIL.Image.open(file_path).convert("RGB")
    image = np.array(image)
    image = image[:, :, [2, 1, 0]]  # RGB to BGR
    return image


def compute_sim(feat1, feat2):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))


def compare_faces(known_faces, unknown_faces):
    similarity = -1.0
    for known_face in known_faces:
        for unknown_face in unknown_faces:
            result = compute_sim(known_face, unknown_face)
            if result > similarity:
                similarity = result
    return similarity


def get_index_with_highest_similarity(known_faces, unknown_face):
    def compare_face(known_face):
        if known_face is None:
            return -1.0
        return compare_faces(known_face, unknown_face)
    similarity_list = list(map(compare_face, known_faces))
    highest_similarity_index = Util.get_max_index(similarity_list)

    return {'index': highest_similarity_index, 'similarity': similarity_list[highest_similarity_index]}


class Recognizer:
    def __init__(self):
        self.face_analysis = insightface.app.FaceAnalysis()
        self.face_analysis.prepare(ctx_id=0, det_size=(640, 640))

    def analysis_face(self, target_image_path, only_one_face=False):
        image = read_image(target_image_path)
        faces = self.face_analysis.get(image)

        def embed_face(face):
            return face.embedding
        embedded_faces = list(map(embed_face, faces))
        if not embedded_faces:
            return None
        if only_one_face and not len(embedded_faces) == 1:
            # 分類済の画像内で顔が複数検知される場合、別人物の画像を認証する可能性があるため省く
            return None
        return embedded_faces

    def compare(self):
        known_images = File.get_filenames_containing_subdir(os.path.join(os.environ['SORTED_FOLDER']))
        unknown_images = File.get_filenames(os.path.join(os.environ['UNKNOWN_FOLDER'], os.environ['TARGET_EXT']))[
                            :int(os.environ['PROCESSING_NUM'])]
        pprint.pprint(unknown_images)

        known_faces = list(map(self.analysis_face, known_images, [True] * len(unknown_images)))

        for unknown_image in unknown_images:
            unknown_face = self.analysis_face(unknown_image)
            if unknown_face is None:
                File.move_file(unknown_image,
                               os.path.join(os.environ['UNIDENTIFIED_FOLDER']),
                               'cannot find faces in')
                continue
            result = get_index_with_highest_similarity(known_faces, unknown_face)
            max_index = result['index']
            similarity = result['similarity']
            if similarity < float(os.environ['THRESHOLD']):
                File.move_file(unknown_image,
                               os.path.join(os.path.join(os.environ['THRESHOLD_FOLDER'])),
                               'out of threshold[{0}]'.format(similarity))
                continue

            recognized_image = known_images[max_index]
            recognized_name = File.get_containing_dirname(recognized_image)
            File.move_file(unknown_image,
                           os.path.join(os.environ['SORTED_FOLDER'], recognized_name),
                           'ok {0}[{1}]'.format(recognized_name, similarity))
