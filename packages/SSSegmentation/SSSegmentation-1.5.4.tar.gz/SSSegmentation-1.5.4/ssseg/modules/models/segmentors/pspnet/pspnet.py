'''
Function:
    Implementation of PSPNet
Author:
    Zhenchao Jin
'''
import copy
import torch.nn as nn
from ..base import BaseSegmentor
from .ppm import PyramidPoolingModule


'''PSPNet'''
class PSPNet(BaseSegmentor):
    def __init__(self, cfg, mode):
        super(PSPNet, self).__init__(cfg, mode)
        align_corners, norm_cfg, act_cfg, head_cfg = self.align_corners, self.norm_cfg, self.act_cfg, cfg['head']
        # build pyramid pooling module
        ppm_cfg = {
            'in_channels': head_cfg['in_channels'], 'out_channels': head_cfg['feats_channels'], 'pool_scales': head_cfg['pool_scales'],
            'align_corners': align_corners, 'norm_cfg': copy.deepcopy(norm_cfg), 'act_cfg': copy.deepcopy(act_cfg),
        }
        self.ppm_net = PyramidPoolingModule(**ppm_cfg)
        # build decoder
        self.decoder = nn.Sequential(
            nn.Dropout2d(head_cfg['dropout']),
            nn.Conv2d(head_cfg['feats_channels'], cfg['num_classes'], kernel_size=1, stride=1, padding=0)
        )
        # build auxiliary decoder
        self.setauxiliarydecoder(cfg['auxiliary'])
        # freeze normalization layer if necessary
        if cfg.get('is_freeze_norm', False): self.freezenormalization()
    '''forward'''
    def forward(self, x, targets=None):
        img_size = x.size(2), x.size(3)
        # feed to backbone network
        backbone_outputs = self.transforminputs(self.backbone_net(x), selected_indices=self.cfg['backbone'].get('selected_indices'))
        # feed to pyramid pooling module
        ppm_out = self.ppm_net(backbone_outputs[-1])
        # feed to decoder
        seg_logits = self.decoder(ppm_out)
        # forward according to the mode
        if self.mode == 'TRAIN':
            loss, losses_log_dict = self.customizepredsandlosses(
                predictions=seg_logits, targets=targets, backbone_outputs=backbone_outputs, losses_cfg=self.cfg['losses'], img_size=img_size,
            )
            return loss, losses_log_dict
        return seg_logits