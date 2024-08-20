'''
Function:
    Implementation of CCNet
Author:
    Zhenchao Jin
'''
import torch
import torch.nn as nn
from ..base import BaseSegmentor
try:
    from mmcv.ops import CrissCrossAttention
except:
    CrissCrossAttention = None
from ...backbones import BuildActivation, BuildNormalization


'''CCNet'''
class CCNet(BaseSegmentor):
    def __init__(self, cfg, mode):
        super(CCNet, self).__init__(cfg, mode)
        align_corners, norm_cfg, act_cfg, head_cfg = self.align_corners, self.norm_cfg, self.act_cfg, cfg['head']
        # build criss-cross attention
        self.conv_before_cca = nn.Sequential(
            nn.Conv2d(head_cfg['in_channels'], head_cfg['feats_channels'], kernel_size=3, stride=1, padding=1, bias=False),
            BuildNormalization(placeholder=head_cfg['feats_channels'], norm_cfg=norm_cfg),
            BuildActivation(act_cfg),
        )
        self.cca = CrissCrossAttention(head_cfg['feats_channels'])
        self.conv_after_cca = nn.Sequential(
            nn.Conv2d(head_cfg['feats_channels'], head_cfg['feats_channels'], kernel_size=3, stride=1, padding=1, bias=False),
            BuildNormalization(placeholder=head_cfg['feats_channels'], norm_cfg=norm_cfg),
            BuildActivation(act_cfg),
        )
        # build decoder
        self.decoder = nn.Sequential(
            nn.Conv2d(head_cfg['in_channels']+head_cfg['feats_channels'], head_cfg['feats_channels'], kernel_size=3, stride=1, padding=1, bias=False),
            BuildNormalization(placeholder=head_cfg['feats_channels'], norm_cfg=norm_cfg),
            BuildActivation(act_cfg),
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
        # feed to cca
        feats = self.conv_before_cca(backbone_outputs[-1])
        for _ in range(self.cfg['head']['num_recurrence']):
            feats = self.cca(feats)
        feats = self.conv_after_cca(feats)
        # feed to decoder
        feats = torch.cat([backbone_outputs[-1], feats], dim=1)
        seg_logits = self.decoder(feats)
        # forward according to the mode
        if self.mode == 'TRAIN':
            loss, losses_log_dict = self.customizepredsandlosses(
                predictions=seg_logits, targets=targets, backbone_outputs=backbone_outputs, losses_cfg=self.cfg['losses'], img_size=img_size,
            )
            return loss, losses_log_dict
        return seg_logits