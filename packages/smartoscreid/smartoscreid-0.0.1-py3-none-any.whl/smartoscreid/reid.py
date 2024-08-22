import torch
from PIL import Image
from smartoscreid import torchreid
from smartoscreid.torchreid import metrics
from smartoscreid.torchreid.data.transforms import build_transforms

class REID:
    def __init__(self, 
                 reid_model:str = "resnet50", 
                 pretrained_weight:str = ""
                 ):
        self.use_gpu = torch.cuda.is_available()
        self.model = torchreid.models.build_model(
            name=reid_model,
            num_classes=1,  # human
            loss='softmax',
            pretrained=True,
            use_gpu=self.use_gpu
        )
        if len(pretrained_weight) > 0:
            torchreid.utils.load_pretrained_weights(self.model, pretrained_weight)
        if self.use_gpu:
            self.model = self.model.cuda()
        _, self.transform_te = build_transforms(
            height=256, width=128,
            random_erase=False,
            color_jitter=False,
            color_aug=False
        )
        self.dist_metric = 'cosine'
        self.model.eval()

    def _extract_features(self, input):
        self.model.eval()
        return self.model(input)

    def _features(self, imgs):
        f = []
        for img in imgs:
            img = Image.fromarray(img.astype('uint8')).convert('RGB')
            img = self.transform_te(img)
            img = torch.unsqueeze(img, 0)
            if self.use_gpu:
                img = img.cuda()
            features = self._extract_features(img)
            features = features.data.cpu()  # tensor shape=1x2048
            f.append(features)
        f = torch.cat(f, 0)
        return f

    def compute_distance(self, qf, gf):
        distmat = metrics.compute_distance_matrix(qf, gf, self.dist_metric)
        return distmat.numpy()