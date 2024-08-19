import os
import shutil
from pypers.utils.img import Convert as convert, \
    Generate as generate
from pypers.utils import img
from pypers.utils.utils import rename_file
from . import BaseHandler

class GBDImage(BaseHandler):

    # self.img_files {'123': [{'ori': _}, {'ori: _'}], '234': [{'ori': _}]}
    def process(self, data_file, appnum):
        if not data_file:
            return
        st13 = data_file.get('st13', None)
        if not st13:
            return
        doc = data_file.get('doc')
        data = data_file.get('imgs', [])
        if not data:
            return
        _faded = []
        _corrupt = []
        _cropped = []
        logos = []
        # can have multiple images
        for idx, files in enumerate(data):
            if not files.get('ori', None):
                # Skip images that failed to download
                continue
            img_ori = os.path.join(self.extraction_dir, files['ori'])
            if not os.path.exists(img_ori):
                continue
            img_name, img_ext = os.path.splitext(os.path.basename(img_ori))

            # cv2 cannot work with gif => transform to png
            # convert gif to png
            # ------------------
            img_ori = convert.from_gif(img_ori)

            # convert whatever the whatever-hi.%img_ext%
            # --------------------------------------------
            try:
                img_hgh = convert.to_hgh(img_ori, '%s-hi' % (img_name),
                                         img_ext='.png')
            except Exception as e:
                _corrupt.append(appnum)
                continue

            # cropping image
            # --------------
            # -1: no change
            # 0: cropped
            # 1: faded
            # 2: corrupt
            try:
                result = img.crop(img_hgh, img_hgh)
                if result == 0:
                    _cropped.append(appnum)
                elif result == 1:
                    _faded.append(appnum)
                    continue
                elif result == 2:
                    _corrupt.append(appnum)
                    continue
            except Exception as e:
                _corrupt.append(appnum)
                continue


            # check if it is a zero-size image
            if os.stat(img_hgh).st_size == 0:
                _corrupt.append(appnum)
                continue

            # high image resize after crop
            # ----------------------------
            try:
                generate.high(img_hgh)
            except Exception as e:
                _corrupt.append(appnum)
                continue

            # high image generated => get its crc
            # -----------------------------------
            crc = img.get_crc(img_hgh)

            # rename high to use crc
            img_hgh = rename_file(img_hgh, '%s-hi' % crc)

            # generating thumbnail
            # --------------------
            try:
                img_thm = generate.thumbnail(img_hgh, crc)
            except Exception as e:
                _corrupt.append(appnum)
                self.logger.error('cannot generate thumbnail for %s' % img_ori)
                continue

            # update the
            data[idx]['crc'] = crc

            data[idx]['ori'] = os.path.relpath(img_ori, self.extraction_dir)
            self.backup.store_img_ori(img_ori, st13, crc, hard=False)
            data[idx]['thum'] = os.path.relpath(img_thm, self.extraction_dir)
            self.backup.store_img_gbd(img_thm, st13, hard=True)
            data[idx]['high'] = os.path.relpath(img_hgh, self.extraction_dir)
            self.backup.store_img_gbd(img_hgh, st13, hard=False)

            doc['img_files'].append({
                'crc': crc,
                'img': img_hgh
            })
            logos.append(crc)
        gbd_file = doc['local_path_gbd']
        self.backup.store_doc_gbd_to_s3(gbd_file, st13, logos, hard=False)
