
import colorsys

import cv2
import matplotlib.image as mpimg
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

# %matplotlib inline


class Spuit:
    """
    음 뭐랄까.. 색상을 스포이드로 뽑아 줌 ? ?
    """

    def __init__(self, image_path=None, n_clusters=4, image=None):
        """
        이미지를 넣어주쎄용
        """
        if image_path is not None:
            self.image_path = image_path
            self.image = cv2.imread(image_path)
        else:
            self.image = image
            
        self.n_clusters = n_clusters
        self.percent = []
        self.rgb = []
        self.hex = []
        self.hsv_origin = []
        self.hsv = []
        self.hsv360 = []
        self.bar = []
        self.labels = []
        self.label_info = []
        self.image_color_cluster()

    def centroid_histogram(self, clt):
        # grab the number of different clusters and create a histogram
        # based on the number of pixels assigned to each cluster
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)

        # normalize the histogram, such that it sums to one
        hist = hist.astype("float")
        hist /= hist.sum()

        # return the histogram
        return hist

    def plot_colors(self, hist, centroids):
        # initialize the bar chart representing the relative frequency
        # of each of the colors
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0

        hist_zip = list(zip(hist, centroids))
        hist_zip.sort(reverse=True, key=lambda x: x[0])
        # loop over the percentage of each cluster and the color of
        # each cluster
        for (percent, color) in hist_zip:
            # plot the relative percentage of each cluster
            self.percent.append(percent)

            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX

        # return the bar chart
        return bar

    def image_color_cluster(self):
        image = self.image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        clt = KMeans(n_clusters=self.n_clusters)
        clt.fit(image)

        hist = self.centroid_histogram(clt)
        bar = self.plot_colors(hist, clt.cluster_centers_)
        self.bar = bar

        self.labels = clt.labels_

        sort_zip = list(
            zip(hist, np.unique(self.labels), clt.cluster_centers_))
        sort_zip.sort(reverse=True)

        for index, (percent, label, rgb) in enumerate(sort_zip):
            hsv_origin = colorsys.rgb_to_hsv(
                rgb[0]/255, rgb[1]/255, rgb[2]/255)
            rgb = [int(rgb[0]), int(rgb[1]), int(rgb[2])]

            self.rgb.append(rgb)
            self.hex.append('#{:02x}{:02x}{:02x}'.format(
                rgb[0], rgb[1], rgb[2]))
            self.hsv.append([int(round(hsv_origin[0]*180)),
                             int(round(hsv_origin[1]*100)), int(round(hsv_origin[2]*100))])
            self.hsv360.append([int(round(hsv_origin[0]*360)),
                                int(round(hsv_origin[1]*100)), int(round(hsv_origin[2]*100))])
            self.hsv_origin.append(
                [hsv_origin[0], hsv_origin[1], hsv_origin[2]])

            self.label_info.append({
                'percent': percent,
                'label': label,
                'rgb': rgb,
                'hex': '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]),
                'hsv': [int(round(hsv_origin[0]*180)), int(round(hsv_origin[1]*100)), int(round(hsv_origin[2]*100))],
                'hsv360': [int(round(hsv_origin[0]*360)), int(round(hsv_origin[1]*100)), int(round(hsv_origin[2]*100))],
                'hsv_origin': [hsv_origin[0], hsv_origin[1], hsv_origin[2]]
            })

        # # bar 중복제거 & 정렬
        # _, indexes = np.unique(bar[0], axis=0, return_index=True)
        # unique_rows = [bar[0][i] for i in np.sort(indexes)]
        # # 1row hsv : 114, 25.0, 94.1
        # for i in range(len(unique_rows)):
        #     self.rgb.append(unique_rows[i])
        #     self.hex.append('#{:02x}{:02x}{:02x}'.format(unique_rows[i][0], unique_rows[i][1] , unique_rows[i][2]))
        #     hsv_origin = colorsys.rgb_to_hsv(unique_rows[i][0]/255, unique_rows[i][1]/255 , unique_rows[i][2]/255)
        #     self.hsv_origin.append([hsv_origin[0], hsv_origin[1], hsv_origin[2]])
        #     self.hsv.append([hsv_origin[0]/2, hsv_origin[1], hsv_origin[2]])

    def get_image(self):
        return self.image

    def get_info(self):
        """
        이미지 전체 정보
        퍼센트로 sort desc
        """
        return self.label_info

    def get_labels(self):
        """
        이미지 라벨(클러스터링 영역)
        """
        return self.labels

    def get_percent(self):
        """
        return percent array
        """
        return self.percent

    def get_rgb(self):
        """
        return rgb array
        """
        return self.rgb

    def get_hex(self):
        """
        return hex array
        """
        return self.hex

    def get_hsv(self):
        """
        return hsv array
        """
        return self.hsv

    def get_hsv360(self):
        """
        return hsv360 array
        """
        return self.hsv360

    def get_hsv_origin(self):
        """
        return hsv_origin array
        """
        return self.hsv_origin

    def get_plt(self):
        """
        get_plt
        """
        plt.figure()
        plt.axis("off")
        plt.imshow(self.bar)
        plt.show()


# End Class=====================================================================
# if __name__ == "__main__":

#     image_path = "./test/images/jordy.jpg"
#     # image_path = "./test/images/sunflower.jpg"

#     #preview image
#     # image = mpimg.imread(image_path)
#     # plt.imshow(image)

#     spuit_image = Spuit(image_path)
#     print('get_info', spuit_image.get_info())
#     print('get_label', spuit_image.get_labels())
#     print('get_percent', spuit_image.get_percent())
#     print('get_rgb', spuit_image.get_rgb())
#     print('get_hex', spuit_image.get_hex())
#     print('get_hsv', spuit_image.get_hsv())
#     print('get_hsv360', spuit_image.get_hsv360())
#     print('get_hsv_origin', spuit_image.get_hsv_origin())
#     spuit_image.get_plt()
